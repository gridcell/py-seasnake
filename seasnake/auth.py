import datetime
import time
import webbrowser
from typing import Optional

import jwt
import requests

AUTH0_DOMAIN = "datamermaid.auth0.com"
RESPONSE_TYPE = "token"
SCOPE = "openid,profile,email"
CLIENT_ID = "gFlPNhqS1h8QR3THF8R9fVePQudzGcKD"
AUDIENCE = "https://api.datamermaid.org"


class MermaidAuth:
    """
    A class for handling authentication and access token management for the Mermaid API.

    The MermaidAuth class is responsible for managing the process of obtaining and storing
    access tokens for use with the Mermaid API. It checks if the stored token is expired,
    and if so, initiates an authentication process to obtain a new token.

    Attributes:
        auth_file (str): The name of the file where the access token is stored.

    Example usage:

        mermaid_auth = MermaidAuth()
        token = mermaid_auth.get_token()
    """

    auth_file = ".auth"

    def _token_expired(self, token: Optional[str]) -> bool:
        if not token:
            return True

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

    def _write_token(self, token: str):
        with open(self.auth_file, "w") as f:
            f.write(token)

    def _load_token(self) -> Optional[str]:
        try:
            with open(self.auth_file, "r") as f:
                return f.read()
        except Exception:
            return None

    def get_token(self) -> Optional[str]:
        client_id = CLIENT_ID
        domain = AUTH0_DOMAIN
        audience = AUDIENCE

        token = self._load_token()
        if self._token_expired(token) is False:
            return token

        response = requests.post(
            f"https://{domain}/oauth/device/code",
            data={"client_id": client_id, "audience": audience},
        )

        json_response = response.json()
        user_code = json_response["user_code"]
        verification_uri = json_response["verification_uri"]
        webbrowser.open(f"{verification_uri}?user_code={user_code}")

        # Poll the token endpoint until a token is obtained or the timeout is reached
        start_time = time.time()
        timeout = json_response["expires_in"]

        while True:
            # Wait for a short time before polling again
            time.sleep(3)

            # Make a request to the token endpoint using the device code
            response = requests.post(
                f"https://{domain}/oauth/token",
                data={
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    "client_id": client_id,
                    "device_code": json_response["device_code"],
                },
            )

            # If the request is successful, extract the access token and break out of the loop
            if response.status_code == 200:
                json_response = response.json()
                access_token = json_response["access_token"]
                self._write_token(access_token)
                return access_token

            # If the timeout is reached, exit the loop and inform the user
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                print("Timeout reached. Please try again.")
                break

        return None


if __name__ == "__main__":
    mermaid_auth = MermaidAuth()
    token = mermaid_auth.get_token()
    if token:
        print(f"JWT token: {token}")
    else:
        print("Failed to obtain token.")
