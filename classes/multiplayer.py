import json
import os
import threading
import typing
from collections.abc import Callable
from queue import Queue
from urllib.parse import quote

import requests
from websocket import create_connection

import constants
from classes.game import Game
from classes.gui.pages.game_start_countdown import GameStartCountdown
from classes.gui.pages.lobby_page import LobbySubmenu
from classes.gui.pages.multiplayer_game_page import MultiplayerGamePage
from classes.gui.pages.scoreboard_page import ScoreboardPage
from constants import USERDATA_FILE

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.game_window import GameWindow


class MultiplayerGameWrapper:
    def __init__(self, window: 'GameWindow'):
        self._window = window
        self.gui_queue = Queue()

        self._lobby_code: typing.Optional[str] = None
        self._username: typing.Optional[str] = None
        self._player_list: list[str] = []

        self._game_page: typing.Optional[MultiplayerGamePage] = None
        self._game_map: typing.Optional[dict] = None
        self.gm_class: typing.Optional[type[Game]] = None

        self._ws = None
        self._ws_thread = None
        self._running = False
        self.lobby_game_ended = False

        self.countdown_page: typing.Optional[GameStartCountdown] = None
        self.lobby_page: typing.Optional[LobbySubmenu] = None

        # noinspection PyTypeChecker
        self._window.after(0, self._process_gui_queue)

    def __del__(self):
        self.disconnect_ws()

    def create(self, gm_class):
        self.gm_class = gm_class
        self._username = MultiplayerGameWrapper._get_username()

        payload = {
            "name": self._username + "'s lobby",
            "hostUsername": self._username,
            "gmShortName": gm_class.gm_short,
        }

        r = requests.post(f"{constants.API_BASE_URL}/lobbies", json=payload)
        r.raise_for_status()

        data = r.json()
        self._lobby_code = data["code"]

        self.connect_ws()

        return data["name"], data["code"], self._username, data["players"]

    def delete(self):
        if not self._lobby_code:
            return

        payload = {
            "lobbyCode": self._lobby_code,
        }

        self.disconnect_ws()
        r = requests.delete(f"{constants.API_BASE_URL}/lobbies", json=payload)
        r.raise_for_status()

        self._lobby_code = None

    def join(self, lobby_code):
        self._lobby_code = lobby_code
        self._username = MultiplayerGameWrapper._get_username()

        payload = {
            "lobbyCode": self._lobby_code,
            "username": self._username
        }

        r = requests.post(f"{constants.API_BASE_URL}/lobbies/join", json=payload)
        r.raise_for_status()

        self.connect_ws()

        data = r.json()

        for gm_class in Game.__subclasses__():
            if gm_class.gm_short == data["modeShort"]:
                self.gm_class = gm_class
                break

        return data["name"], data["code"], self._username, data["players"]

    def leave(self):
        if not self._lobby_code or not self._username:
            return

        payload = {
            "lobbyCode": self._lobby_code,
            "username": self._username
        }

        self.disconnect_ws()

        r = requests.post(f"{constants.API_BASE_URL}/lobbies/leave", json=payload)
        r.raise_for_status()

        self._lobby_code = None

    def get_lobby_list(self) -> list[tuple[str, Callable]]:
        r = requests.get(f"{constants.API_BASE_URL}/lobbies")
        r.raise_for_status()

        data = r.json()
        data_btns = []

        for lobby in data:
            data_btns.append((
                f'{lobby["code"]} {len(lobby["players"])}/{constants.LOBBY_MAX_PLAYERS}',
                lambda code=lobby["code"]: self._window.open_lobby_submenu(self.join(code))
            ))

        return data_btns

    def start_game(self, game_map):
        if not self._lobby_code or not self._username:
            return

        payload = {
            "code": self._lobby_code,
            "gameMap": json.dumps(game_map)
        }

        r = requests.post(f"{constants.API_BASE_URL}/lobbies/start", json=payload)
        r.raise_for_status()

    def play(self, connected_players):
        if not self.gm_class or not self._game_map:
            raise ValueError("Game not initialized")
        if self.countdown_page:
            self.countdown_page = None

        self._player_list = connected_players
        self._window.close_submenus()
        connected_players.remove(self._username)
        self._game_page = self._window.open_page(
            lambda: MultiplayerGamePage(self._window, self._game_map, self.gm_class, connected_players),
            remember=False,
            can_return=False
        )
        self._game_page.game_start()

        # noinspection PyTypeChecker
        self._window.after(0, self._send_game_state_update)

    def _countdown(self, num: int):
        if not self.countdown_page:
            self._window.start_multiplayer_countdown()

        self.countdown_page.update_cd(num)

    def connect_ws(self):
        if not self._lobby_code:
            return

        encoded_username = quote(self._username)
        ws_url = f"{constants.API_WS_URL}/lobbies/{self._lobby_code}?user={encoded_username}"
        self._ws = create_connection(ws_url)

        hello = {
            "type": "HELLO",
            "username": self._username
        }
        self._ws.send(json.dumps(hello))

        self._start_ws_listener()

    def disconnect_ws(self):
        self._running = False
        if self._ws:
            try:
                self._ws.close()
            except:
                pass
            self._ws = None

    def _send_game_state_update(self):
        if self._ws and self._game_page:
            update = {
                "type": "STATE_UPDATE",
                "username": self._username,
                "state": self._game_page.state
            }
            self._ws.send(json.dumps(update))

            if not self._game_page.is_game_over:
                # noinspection PyTypeChecker
                self._window.after(30, self._send_game_state_update)
            else:
                game_end_msg = {
                    "type": "GAME_END",
                    "stats": self._game_page.stats
                }
                self._ws.send(json.dumps(game_end_msg))

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

        # noinspection PyTypeChecker
        self._window.after(30, self._process_gui_queue)

    def _start_ws_listener(self):
        self._running = True

        def run():
            while self._running:
                try:
                    msg = self._ws.recv()
                    data = json.loads(msg)
                except:
                    break

                self._handle_ws_message(data)

        self._ws_thread = threading.Thread(target=run, daemon=True)
        self._ws_thread.start()

    def _handle_ws_message(self, data: dict):
        msg_type = data["type"]

        if msg_type == "PLAYER_LIST_CHANGED":
            players = data["lobby"]["players"]
            self.gui_queue.put(lambda: self.lobby_page.update_player_list(self._username, players) if self.lobby_page else None)
        elif msg_type == "STATE_UPDATE":
            username = data["username"]
            if username != self._username and username in self._player_list:
                self.gui_queue.put(lambda: self._game_page.update_mini_view(username, data["state"]))
        elif msg_type == "COUNTDOWN":
            self.gui_queue.put(lambda: self._countdown(data["number"]))
        elif msg_type == "GAME_START":
            connected_players = data["connectedPlayers"]
            self._game_map = json.loads(data["gameMap"])
            self.gui_queue.put(lambda: self.play(connected_players))
        elif msg_type == "GAME_END":
            self.gui_queue.put(
                lambda: self._window.open_page(
                    lambda: ScoreboardPage(self._window, self._username, data["results"])
                )
            )
