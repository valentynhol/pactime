import json
import threading
import requests
from websocket import create_connection

import constants


class MultiplayerGameWrapper:
    main_menu = None
    gm_class = None
    game_map = None
    lobby_code = None
    username = None
    ws = None
    remote_states = {}
    ws_thread = None
    running = False

    def __init__(self, main_menu):
        self.main_menu = main_menu

    def create(self, gm_class, game_map, username):
        self.gm_class = gm_class
        self.game_map = game_map
        self.username = username

        payload = {
            "name": username + "'s lobby",
            "hostUsername": username,
            "gmShortName": gm_class.gm_short,
            #"mapJson": game_map,
        }

        r = requests.post(f"{constants.API_BASE_URL}/lobbies", json=payload)
        r.raise_for_status()

        data = r.json()
        self.lobby_code = data["code"]

        self.connect_ws()

        return data["name"], data["code"], data["players"]

    def delete(self):
        if not self.lobby_code:
            return

        payload = {
            "lobbyCode": self.lobby_code,
        }

        self.disconnect_ws()
        r = requests.delete(f"{constants.API_BASE_URL}/lobbies", json=payload)
        r.raise_for_status()

        self.lobby_code = None

    def join(self, lobby_code, username):
        self.lobby_code = lobby_code
        self.username = username

        payload = {
            "lobbyCode": self.lobby_code,
            "username": username
        }

        r = requests.post(f"{constants.API_BASE_URL}/lobbies/join", json=payload)
        r.raise_for_status()

        self.connect_ws()

        data = r.json()
        return data["name"], data["code"], data["players"]

    def leave(self):
        if not self.lobby_code or not self.username:
            return

        payload = {
            "lobbyCode": self.lobby_code,
            "username": self.username
        }

        self.disconnect_ws()

        r = requests.post(f"{constants.API_BASE_URL}/lobbies/leave", json=payload)
        r.raise_for_status()

        self.lobby_code = None

    @staticmethod
    def get_lobby_list() -> dict:
        r = requests.get(f"{constants.API_BASE_URL}/lobbies")
        r.raise_for_status()

        data = r.json()
        data_btns = {}

        for lobby in data:
            data_btns[lobby["code"]] = f'{lobby["name"]} {lobby["code"]} {len(lobby["players"])}/5'

        return data_btns

    def play(self):
        if not self.gm_class or not self.game_map:
            raise ValueError("Game not initialized")

        game = self.gm_class(self.game_map)
        game.game_window_init()

        if self.ws:
            msg = {"type": "GAME_START", "username": self.username}
            self.ws.send(json.dumps(msg))

        while not game.process == "game_ended":
            game.game_window_update()

            if self.ws:
                update = {
                    "type": "STATE_UPDATE",
                    "username": self.username,
                    "state": game.get_state()
                }
                self.ws.send(json.dumps(update))

            for username, state in self.remote_states.items():
                game.apply_remote_state(username, state)

        if self.ws:
            msg = {"type": "GAME_END", "username": self.username}
            self.ws.send(json.dumps(msg))

        return game.result()

    def connect_ws(self):
        if not self.lobby_code:
            return

        ws_url = f"{constants.API_WS_URL}/lobbies/{self.lobby_code}"
        self.ws = create_connection(ws_url)

        hello = {
            "type": "HELLO",
            "username": self.username
        }
        self.ws.send(json.dumps(hello))

        self._start_ws_listener()

    def disconnect_ws(self):
        self.running = False
        if self.ws:
            try:
                self.ws.close()
            except:
                pass
            self.ws = None

    def _start_ws_listener(self):
        self.running = True

        def run():
            while self.running:
                try:
                    msg = self.ws.recv()
                except Exception:
                    break

                if not msg:
                    continue

                try:
                    data = json.loads(msg)
                except:
                    continue

                self._handle_ws_message(data)

        self.ws_thread = threading.Thread(target=run, daemon=True)
        self.ws_thread.start()

    def _handle_ws_message(self, data: dict):
        print(data)
        msg_type = data.get("type")

        if msg_type == "PLAYER_LIST_CHANGED":
            players = data["lobby"]["players"]
            self.main_menu.gui_queue.put(lambda: self.main_menu.update_lobby_gui(players))
        elif msg_type == "STATE_UPDATE":
            username = data["username"]
            if username != self.username:  # ignore own updates
                self.remote_states[username] = data["state"]
        elif msg_type == "MAP_UPDATE":
            pass
        elif msg_type == "GAME_START":
            pass

        elif msg_type == "GAME_END":
            pass
