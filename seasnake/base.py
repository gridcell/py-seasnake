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
    """
    Decorator that checks whether the class has a `token`
    attribute before executing a method that requires
    authorization.

    Args:
        func: A method that requires authorization.

    Returns:
        The decorated function.

    Raises:
        Exception: If the `token` attribute is not present in the class.
    """

    def wrapper(self, *args, **kwargs):
        if not hasattr(self, "token"):
            raise Exception("Class does not have a `self.token` attribute")
        return func(self, *args, **kwargs)

    return wrapper


class MermaidBase:
    """
    Base class for the Mermaid API client.

    Attributes:
        REQUEST_LIMIT (int): The maximum number of records to retrieve in a single request.
        token (Optional[str]): The access token for the Mermaid API.
    """

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
        """
        Sends an API request.

        Args:
            url (str): The URL for the API endpoint.
            payload (Optional[Dict[str, Any]]): The payload to include in the request.
                Defaults to None.
            params (Optional[Dict[str, Any]]): The query parameters to include in the request.
                Defaults to None.
            headers (Optional[Dict[str, str]]): The headers to include in the request.
                Defaults to None.
            method (str): The HTTP method to use for the request. Defaults to "GET".

        Returns:
            A dictionary containing the response from the API.

        Raises:
            requests.RequestException: If an error occurs while sending the request.
            Exception: If the response status code is not 200.
        """

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
        """
        Sends multiple requests to the Mermaid API and returns a generator of results.

        Args:
            url (str): The URL for the API endpoint.
            query_params (Optional[Dict[str, Any]]): The query parameters to include
                in the request. Defaults to None.
            payload (Optional[Dict[str, Any]]): The payload to include in the request.
                Defaults to None.
            headers (Optional[Dict[str, str]]): The headers to include in the request.
                Defaults to None.
            method (str): The HTTP method to use for the request. Defaults to "GET".
            num_threads (Optional[int]): The number of threads to use for making requests.
                Defaults to None.

        Yields:
            A generator of dictionaries containing records from the API.

        Raises:
            Exception: If the response status code is not 200.
        """

        query_params = query_params or {}
        result = self.fetch(
            url, payload, params=query_params, headers=headers, method=method
        )
        total_records = result.get("count") or 0
        num_calls = math.ceil(total_records / self.REQUEST_LIMIT) - 1
        yield from result.get("results") or []

        if num_threads is None:
            cpu_count = os.cpu_count() or 1
            num_threads = min((1 if cpu_count <= 1 else cpu_count - 1) * 2, MAX_THREADS)

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
        """Returns a pandas DataFrame from the data retrieved from a Mermaid API endpoint.

        Args:
            url (str): The URL for the API endpoint.
            query_params (Optional[Dict[str, Any]]): The query parameters to include
                in the request. Defaults to None.
            payload (Optional[Dict[str, Any]]): The payload to include in the request.
                Defaults to None.
            headers (Optional[Dict[str, Any]]): The headers to include in the request.
                Defaults to None.
            method (str): The HTTP method to use for the request. Defaults to "GET".
            columns (Optional[Union[List[str], Tuple[str]]]): The columns to include in the
                resulting DataFrame. Defaults to None.
            rename_columns (Optional[Dict[str, str]]): A dictionary of old and new column names
                to rename the columns in the resulting DataFrame. Defaults to None.
            requires_auth (bool): Whether authorization is required to access the API
                endpoint. Defaults to True.

        Returns:
            DataFrame

        Raises:
            Exception: If the response status code is not 200.
        """

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
