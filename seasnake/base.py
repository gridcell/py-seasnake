from typing import Any, Dict, Generator, List, Optional, Tuple, Union

import requests
import pandas as pd
from pandas import DataFrame

PROJECT_STATUS_OPEN = 90
PROJECT_STATUS_TEST = 80
PROJECT_STATUS_LOCKED = 10
MERMAID_API_URL = "https://api.datamermaid.org/v1"


def requires_token(func):
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, "token"):
            raise Exception("Class does not have a `self.token` attribute")
        return func(self, *args, **kwargs)

    return wrapper


class MermaidBase:
    def __init__(self, token: Optional[str] = None):
        self.token = token

    def fetch(
        self,
        url: str,
        payload: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        method: str = "GET",
    ) -> Dict[str, Any]:
        _headers = {"Content-Type": "application/json", "User-Agent": "python"}
        _headers |= headers or {}
        payload = payload or {}

        if not url.startswith("http"):
            url = f"{MERMAID_API_URL}{url}"

        method = method.upper()
        if method == "GET":
            request_method = requests.get  # type: ignore
        elif method == "POST":
            request_method = requests.post  # type: ignore
        else:
            raise requests.RequestException(f"Unsupported method: {method}")

        resp = request_method(
            url,
            data=payload,
            params=params,
            headers=_headers,
        )
        if resp.status_code != 200:
            raise Exception(f"Error fetching data: {resp.text}")

        return resp.json()

    def fetch_list(
        self,
        url: str,
        query_params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        method: str = "GET",
    ) -> Generator[Dict[str, Any], None, None]:
        query_params = query_params or {}
        while True:
            result = self.fetch(
                url, payload, params=query_params, headers=headers, method=method
            )

            yield from result.get("results") or []
            if result["next"] is None:
                break
            url = result["next"]

    def data_frame_from_url(
        self,
        url,
        query_params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        method: str = "GET",
        columns: Optional[Union[List[str], Tuple[str]]] = None,
        rename_columns: Optional[Dict[str, str]] = None,
        requires_auth: bool = True,
    ) -> DataFrame:
        headers = headers or {}
        query_params = query_params or {}

        if "limit" not in query_params:
            query_params["limit"] = 1000

        if requires_auth and "Authorization" not in headers:
            headers["Authorization"] = f"Bearer {self.token}"

        data = list(
            self.fetch_list(
                url,
                query_params=query_params,
                payload=payload,
                headers=headers,
                method=method,
            )
        )
        if not data:
            return DataFrame()

        df = DataFrame(data)

        if rename_columns:
            df = df.rename(columns=rename_columns)

        if columns:
            df = DataFrame(df[columns])

        return df

    def flatten(
        self, df: DataFrame, column: str, prefix: Optional[str] = None
    ) -> DataFrame:
        prefix = prefix or column
        return df.join(
            pd.json_normalize(df[column].tolist()).add_prefix(f"{prefix}.")
        ).drop([column], axis=1)
