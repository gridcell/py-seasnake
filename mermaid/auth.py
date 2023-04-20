import datetime
import http.server
import os
import socketserver
import threading
import urllib.parse
import webbrowser
from typing import Optional

import jwt

PORT = 10000
AUTH0_DOMAIN = "datamermaid.auth0.com"
REDIRECT_URI = f"http://localhost:{PORT}/callback"
RESPONSE_TYPE = "token"
SCOPE = "openid,profile,email"

if str(os.environ.get("ENV")).lower() in ("local", "dev"):
    CLIENT_ID = "4AHcVFcwxHb7p1VFB9sFWG52WL7pdNm5"
    AUDIENCE = "https://dev-api.datamermaid.org"
else:
    CLIENT_ID = "f0WJPG2LHzAX3KLU0LwdmVOvtDo7jiu6"
    AUDIENCE = "https://api.datamermaid.org"


class MermaidAuth:
    """
    A class for handling authentication and access token management for the Mermaid API.

    The MermaidAuth class is responsible for managing the process of obtaining and storing
    access tokens for use with the Mermaid API. It checks if the stored token is expired,
    and if so, initiates an authentication process to obtain a new token.

    Attributes:
        AUTH_FILE (str): The name of the file where the access token is stored.

    Example usage:

        mermaid_auth = MermaidAuth()
        access_token = mermaid_auth.request_token()
    """

    AUTH_FILE = ".auth"

    def __init__(self):
        self.token = None
        self.httpd = None
        self.server_thread = None

    def _token_expired(self, token: str) -> bool:
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            expiration_time = payload.get("exp", None)
            if expiration_time:
                expiration_date = datetime.datetime.utcfromtimestamp(expiration_time)
                if expiration_date > datetime.datetime.utcnow():
                    return False
            return True
        except jwt.DecodeError:
            return True

    def request_token(self, force_refresh: bool = False) -> str:
        """
        Request an access token for the API.

        This method retrieves a MERMAID API access token from storage, if available and 
        not expired, and returns it. If the token is not available or has expired, or if
        force_refresh is set to True, a new token will be requested by opening a browser
        window to the MERMAID login page. Once the user has logged in, the new a access
        token will be retrieved and store it for future use.

        Args:
            force_refresh (bool, optional): Whether to force a token refresh even if a 
            valid token exists. Defaults to False.

        Returns:
            str: The access token for the API.
        """
        token = self._load_token()
        if not force_refresh and token and not self._token_expired(token):
            return token

        self._start_server()
        self._open_auth_page()
        self.server_thread.join()

        self._write_token(self.token)

        return self.token

    def _write_token(self, token: str):
        with open(self.AUTH_FILE, "w") as f:
            f.write(token)

    def _load_token(self) -> Optional[str]:
        try:
            with open(self.AUTH_FILE, "r") as f:
                return f.read()
        except Exception:
            return None

    def _start_server(self):
        self.httpd = socketserver.TCPServer(
            ("localhost", PORT), self.CallbackRequestHandler
        )
        self.httpd.mermaid_auth = self
        self.server_thread = threading.Thread(target=self.httpd.serve_forever)
        self.server_thread.start()

    def _stop_server(self):
        def shutdown_server(httpd):
            httpd.shutdown()

        shutdown_thread = threading.Thread(target=shutdown_server, args=(self.httpd,))
        shutdown_thread.start()
        self.httpd.server_close()
        # self.server_thread.join()

    def _open_auth_page(self):
        url = (
            f"https://{AUTH0_DOMAIN}/authorize?"
            f"client_id={CLIENT_ID}&"
            f"redirect_uri={REDIRECT_URI}&"
            f"response_type={RESPONSE_TYPE}&"
            f"audience={AUDIENCE}&"
            f"scope={SCOPE}"
        )
        webbrowser.open(url)

    class CallbackRequestHandler(http.server.SimpleHTTPRequestHandler):
        html_js = """
            <html>
            <head>
                <title>Mermaid Auth</title>
                <script>
                function onLoad() {
                    var fragment = window.location.hash.substr(1);
                    if (fragment) {
                    var xhr = new XMLHttpRequest();
                    xhr.open("GET", "/token?" + fragment);
                    xhr.send();
                    xhr.onload = function () {
                        var msg = '';
                        if (xhr.status == 200) {
                        msg = "You have successfully logged in. You can close this window.";
                        } else {
                        msg = "An error occurred during the login process. Please try again.";
                        }
                        document.getElementById("message").innerHTML = msg;
                    };
                    }
                }
                </script>
            </head>
            <body onload="onLoad()">
                <h1 id="message">Processing...</h1>
            </body>
            </html>
        """
        html = """<html><head><title>Mermaid Auth</title></head><body><h1>{}</h1></body></html>"""

        def log_message(self, format, *args):
            pass

        def do_GET(self):
            try:
                if "token" in self.path:
                    query = urllib.parse.urlparse(self.path).query
                    params = dict(urllib.parse.parse_qsl(query))
                    if "access_token" in params:
                        self.server.mermaid_auth.token = params["access_token"]
                        message = "You have successfully logged in. You can close this window."
                    else:
                        message = "An error occurred during the login process. Please try again."
                    self._process_page(self.html.format(message))
                    self.server.mermaid_auth._stop_server()
                else:
                    self._process_page(self.html_js)
            except Exception as e:
                print(e)
                self.server.mermaid_auth._stop_server()

        def _process_page(self, html: str):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                bytes(
                    html,
                    "utf8",
                )
            )


if __name__ == "__main__":
    mermaid_auth = MermaidAuth()
    token = mermaid_auth.request_token()
    if token:
        print(f"JWT token: {token}")
    else:
        print("Failed to obtain token.")
