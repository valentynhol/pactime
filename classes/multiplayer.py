import json
import os
import threading
from collections.abc import Callable
from queue import Queue
from typing import Tuple, List
from urllib.parse import quote

import requests
from websocket import create_connection

import constants
from classes.game import MiniView, Game
from constants import USERDATA_FILE


class MultiplayerGameWrapper:
    main_menu = None
    gm_class = None
    game_map = None
    lobby_code = None
    username = None
    ws = None
    remote_views = {}
    mini_views_gui = []
    ws_thread = None
    running = False
    gui_queue = None
    lobby_game_ended = False

    def __init__(self, main_menu):
        self.main_menu = main_menu
        self.gui_queue = Queue()

    def create(self, gm_class):
        self.gm_class = gm_class
        self.username = MultiplayerGameWrapper._get_username()

        payload = {
            "name": self.username + "'s lobby",
            "hostUsername": self.username,
            "gmShortName": gm_class.gm_short,
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

    def join(self, lobby_code):
        self.lobby_code = lobby_code
        self.username = MultiplayerGameWrapper._get_username()

        payload = {
            "lobbyCode": self.lobby_code,
            "username": self.username
        }

        r = requests.post(f"{constants.API_BASE_URL}/lobbies/join", json=payload)
        r.raise_for_status()

        self.connect_ws()

        data = r.json()

        for gm_class in Game.__subclasses__():
            if gm_class.gm_short == data["modeShort"]:
                self.gm_class = gm_class
                break

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

    def get_lobby_list(self) -> List[Tuple[str, Callable]]:
        r = requests.get(f"{constants.API_BASE_URL}/lobbies")
        r.raise_for_status()

        data = r.json()
        data_btns = []

        for lobby in data:
            data_btns.append((f'{lobby["code"]} {len(lobby["players"])}/5', lambda: self.join(lobby["code"])))

        return data_btns

    def start_game(self, game_map):
        if not self.lobby_code or not self.username:
            return

        payload = {
            "code": self.lobby_code,
            "gameMap": json.dumps(game_map)
        }

        r = requests.post(f"{constants.API_BASE_URL}/lobbies/start", json=payload)
        r.raise_for_status()

    def play(self, connected_players):
        if not self.gm_class or not self.game_map:
            raise ValueError("Game not initialized")

        game = self.gm_class(self.main_menu, self.game_map)
        game.game_window_init()

        self.mini_views_gui = MiniView.init_mini_views(game)

        idx = 0
        for player in connected_players:
            if player == self.username:
                continue

            self.mini_views_gui[idx][1].config(text=player)
            self.remote_views[player] = MiniView(self.mini_views_gui[idx][2], self.game_map)
            idx += 1

        while not game.process == "game_ended":
            game.game_window_update()
            self._process_gui_queue()

            self._send_game_state_update(game)

        self._send_game_state_update(game)

        while not self.lobby_game_ended:
            game.game_window_update()
            self._process_gui_queue()

        return None # game.result()

    def connect_ws(self):
        if not self.lobby_code:
            return

        encoded_username = quote(self.username)
        ws_url = f"{constants.API_WS_URL}/lobbies/{self.lobby_code}?user={encoded_username}"
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

    def _send_game_state_update(self, game):
        if self.ws:
            update = {
                "type": "STATE_UPDATE",
                "username": self.username,
                "state": MiniView.get_state(game)
            }
            self.ws.send(json.dumps(update))

    @staticmethod
    def _get_username():
        username = None
        if os.path.isfile(USERDATA_FILE):
            with open(USERDATA_FILE) as json_file:
                data = json.load(json_file)
            username = data.get('username')

        return username

    def _process_gui_queue(self):
        while not self.gui_queue.empty():
            callback = self.gui_queue.get_nowait()
            callback()

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
        msg_type = data["type"]

        if msg_type == "PLAYER_LIST_CHANGED":
            players = data["lobby"]["players"]
            self.main_menu.gui_queue.put(lambda: self.main_menu.update_lobby_gui(players))
        elif msg_type == "STATE_UPDATE":
            username = data["username"]
            if username != self.username and username in self.remote_views.keys():
                self.gui_queue.put(lambda: self.remote_views[username].apply_state(data["state"]))
        elif msg_type == "COUNTDOWN":
            self.main_menu.gui_queue.put(lambda: self.main_menu.multiplayer_countdown(data["number"]))
        elif msg_type == "GAME_START":
            connected_players = data["connectedPlayers"]
            self.game_map = json.loads(data["gameMap"])
            self.main_menu.gui_queue.put(lambda: self.play(connected_players))
        elif msg_type == "GAME_END":
            pass
