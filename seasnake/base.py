import math
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd
import requests
from pandas import DataFrame
from requests.adapters import HTTPAdapter, Retry


PROJECT_STATUS_OPEN = 90
PROJECT_STATUS_TEST = 80
PROJECT_STATUS_LOCKED = 10
MERMAID_API_URL = "https://api.datamermaid.org/v1"
MAX_THREADS = 6
MAX_RETRIES = 5
Retry.DEFAULT_BACKOFF_MAX = 30


def requires_token(func):
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, "token"):
            raise Exception("Class does not have a `self.token` attribute")
        return func(self, *args, **kwargs)

    return wrapper


class MermaidBase:
    REQUEST_LIMIT = 1000

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

        with requests.Session() as session:
            retries = Retry(
                total=MAX_RETRIES, backoff_factor=1, status_forcelist=[502, 503, 504]
            )

            session.mount("https://", HTTPAdapter(max_retries=retries))
            method = method.upper()
            if method == "GET":
                request_method = session.get  # type: ignore
            elif method == "POST":
                request_method = session.post  # type: ignore
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
        num_threads: Optional[int] = None,
    ):
        query_params = query_params or {}
        result = self.fetch(
            url, payload, params=query_params, headers=headers, method=method
        )
        total_records = result.get("count") or 0
        num_calls = math.ceil(total_records / self.REQUEST_LIMIT) - 1
        yield from result.get("results") or []

        if num_threads is None:
            cpu_count = os.cpu_count() or 1
            num_threads = min(
                (1 if cpu_count <= 1 else cpu_count - 1) * 2, MAX_THREADS
            )

        if num_calls >= 5 and num_threads > 1:
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = []
                for n in range(num_calls):
                    query_params["page"] = n + 2
                    futures.append(
                        executor.submit(
                            self.fetch,
                            url,
                            payload,
                            params=query_params,
                            headers=headers,
                            method=method,
                        )
                    )

                for future in as_completed(futures):
                    yield from future.result().get("results") or []
        else:
            for n in range(num_calls):
                query_params["page"] = n + 2
                result = self.fetch(
                    url, payload, params=query_params, headers=headers, method=method
                )
                yield from result.get("results") or []

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
