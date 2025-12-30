import secrets
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import constants


class GoogleAuthHandler:
    def __init__(self):
        self.jwt = None
        self.state = secrets.token_urlsafe(16)
        self._server = None
        self._thread = None

    def start(self):
        self._server = HTTPServer(("localhost", 0), AuthCallbackHandler)
        self._server.expected_state = self.state
        self._server.jwt = None

        port = self._server.server_address[1]
        webbrowser.open(f"{constants.API_BASE_URL}/auth/google/login?port={port}&state_nonce={self.state}")

        self._thread = threading.Thread(
            target=self._server.handle_request,
            daemon=True
        )
        self._thread.start()

    def is_finished(self):
        return self._server.jwt is not None

    def get_result(self):
        return self._server.jwt

    def cancel(self):
        if self._server:
            self._server.server_close()


class AuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        qs = parse_qs(urlparse(self.path).query)

        token = qs.get("token", [None])[0]
        state = qs.get("state_nonce", [None])[0]

        if token and state == self.server.expected_state:
            self.server.jwt = token
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                b"""<body style="background-color: black">\n"""
                b"""    <h1 style="color: purple; font: bold 60px Arial">Pactime</h1>\n"""
                b"""    <div style="border: 5px solid purple; background-color: black; padding: 20px">\n"""
                b"""        <p style="color: purple; font: bold 30px Arial; text-align: center">Login successful. You can close this tab.</p>\n"""
                b"""    </div>\n"""
                b"""</body>"""
            )

        else:
            self.send_response(400)
            self.end_headers()