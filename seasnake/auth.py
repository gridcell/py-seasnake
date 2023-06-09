import datetime
import keyring
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

    Authenication is performed using [Device Authorization Grant](https://oauth.net/2/grant-types/device-code/)
    type, and requires input from the user.

    Example usage:

        mermaid_auth = MermaidAuth()
        token = mermaid_auth.get_token()
    """

    AUTH_CODE_URL = f"https://{AUTH0_DOMAIN}/oauth/device/code"
    AUTH_TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"

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
        try:
            keyring.set_password("system", "seasnake", token)
        except Exception:
            pass

    def _load_token(self) -> Optional[str]:
        try:
            token = keyring.get_password("system", "seasnake")
            return token
        except Exception:
            return None

    def clear_token(self):
        """
        Delete stored Mermaid API access token.
        """
        keyring.delete_password("system", "seasnake")

    def get_token(self, store: bool=False) -> Optional[str]:
        """
        Get an access token for the Mermaid API.
        Args:
            store (bool, optional): Store token to keyring service ([more info](https://github.com/jaraco/keyring)). Defaults to False.

        Returns:
            Optional[str]: Access token
        """
        client_id = CLIENT_ID
        audience = AUDIENCE

        token = self._load_token()
        if self._token_expired(token) is False:
            return token

        response = requests.post(
            self.AUTH_CODE_URL,
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
                self.AUTH_TOKEN_URL,
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
                if store:
                    self._write_token(access_token)
                else:
                    self.clear_token()
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
