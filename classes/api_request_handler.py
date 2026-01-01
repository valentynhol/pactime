import json

import requests

import constants
from classes.exceptions import AuthFailedException


class APIRequestHandler:
    def __init__(self, auth_token: str | None):
        self._auth_token = auth_token
        self.player_id = None
        self.username = None
        self.email = None

        self.session = requests.Session()

        if auth_token:
            self.session.headers.update({
                "Authorization": f"Bearer {auth_token}"
            })

    @staticmethod
    def get_lobby_list():
        r = requests.get(f"{constants.API_BASE_URL}/lobbies")
        r.raise_for_status()
        return r.json()

    def create_lobby(self, gm_short_name):
        r = self.session.post(
            f"{constants.API_BASE_URL}/lobbies",
            json={
                "name": f"{self.username}'s lobby",
                "gmShortName": gm_short_name,
            }
        )
        self._handle_response(r)
        return r.json()

    def delete_lobby(self, code):
        r = self.session.delete(
            f"{constants.API_BASE_URL}/lobbies",
            json={"lobbyCode": code}
        )
        self._handle_response(r)

    def join_lobby(self, code):
        r = self.session.post(
            f"{constants.API_BASE_URL}/lobbies/join",
            json={"lobbyCode": code}
        )
        self._handle_response(r)
        return r.json()

    def leave_lobby(self, code):
        r = self.session.post(
            f"{constants.API_BASE_URL}/lobbies/leave",
            json={"lobbyCode": code}
        )
        self._handle_response(r)

    def start_lobby(self, code, game_map):
        r = self.session.post(
            f"{constants.API_BASE_URL}/lobbies/start",
            json={
                "lobbyCode": code,
                "gameMap": json.dumps(game_map)
            }
        )
        self._handle_response(r)

    @staticmethod
    def get_allowed_game_modes():
        r = requests.get(f"{constants.API_BASE_URL}/game-modes")
        r.raise_for_status()
        return r.json()

    def get_player_info(self):
        r = self.session.get(f"{constants.API_BASE_URL}/players")
        self._handle_response(r)

        data = r.json()
        self.player_id = data["id"]
        self.username = data["username"]
        self.email = data["email"]

    def update_player_username(self):
        r = self.session.patch(
            f"{constants.API_BASE_URL}/players",
            json={
                "username": self.username
            }
        )
        self._handle_response(r)

    @staticmethod
    def _handle_response(response: requests.Response):
        if response.status_code in (401, 403):
            raise AuthFailedException()
        response.raise_for_status()