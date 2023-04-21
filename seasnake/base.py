import json
import os
import urllib.request
from typing import Any, Dict, Generator, List, Optional, Tuple, Union

import pandas as pd
from pandas import DataFrame

PROJECT_STATUS_OPEN = 90
PROJECT_STATUS_TEST = 80
PROJECT_STATUS_LOCKED = 10

if str(os.environ.get("ENV")).lower() == "local":
    MERMAID_API_URL = "http://localhost:8080/v1"
elif str(os.environ.get("ENV")).lower() == "dev":
    MERMAID_API_URL = "https://dev-api.datamermaid.org/v1"
else:
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
        headers: Optional[Dict[str, str]] = None,
        method: str = "GET",
    ):
        _headers = {"Content-Type": "application/json", "User-Agent": "python"}
        _headers |= headers or {}
        payload = payload or {}

        if not url.startswith("http"):
            url = f"{MERMAID_API_URL}{url}"

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            method=method,
            headers=_headers,
        )
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read())

    def fetch_list(
        self,
        url: str,
        query_params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        method: str = "GET",
    ) -> Generator[Dict[str, Any], None, None]:
        query_params = query_params or {}
        url = f"{url}?{'&'.join(f'{k}={v}' for k, v in query_params.items())}"
        while True:
            result = self.fetch(url, payload, headers=headers, method=method)
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

        df = DataFrame(
            self.fetch_list(
                url,
                query_params=query_params,
                payload=payload,
                headers=headers,
                method=method,
            )
        )

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
