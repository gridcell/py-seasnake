import base64
import os
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd
from pandas import DataFrame

from ..base import MermaidBase
from ..base import requires_token  # noqa: F401

CACHE_DIR = Path(os.getcwd(), ".cache")


class BaseSummary(MermaidBase):
    """
    Base class for MERMAID sample method summary classes.
    """

    def _get_created_on(self, url: str) -> Optional[str]:
        response = self.fetch(
            url, params={"limit": 1}, headers={"Authorization": f"Bearer {self.token}"}
        )
        record = (response.get("results") or [None])[0]
        return None if record is None else record.get("created_on")

    def get_cache_file_paths(self, url: str) -> Tuple[Path, Path]:
        """
        Generates cache file paths for the given URL.

        Args:
            url (str): The URL to generate cache file paths for.

        Returns:
            Tuple[Path, Path]: A tuple containing the paths for the cache file and cache index file.
        """
        cache_key = self._cache_key(url)
        cache_file = Path(CACHE_DIR, f"{cache_key}.tar.gz")
        cache_index_file = Path(CACHE_DIR, f"{cache_key}.idx")
        return cache_file, cache_index_file

    def to_cache(self, url: str, df: DataFrame) -> DataFrame:
        """
        Caches the given DataFrame to a file with gzip compression.

        Args:
            url (str): The URL associated with the DataFrame.
            df (DataFrame): The DataFrame to cache.

        Returns:
            DataFrame
        """

        url = self.get_full_url(url)

        if df is None or df.empty or "created_on" not in df.columns:
            return df

        if Path(CACHE_DIR).exists() is False:
            os.makedirs(CACHE_DIR)

        created_on = df.iloc[0]["created_on"]

        cache_file, cache_idx_file = self.get_cache_file_paths(url)
        with open(cache_idx_file, "w") as f:
            f.write(created_on)

        df.to_pickle(
            cache_file, compression={"method": "gzip", "compresslevel": 1, "mtime": 1}
        )

        return df

    def read_cache(self, url: str) -> Optional[DataFrame]:
        """
        Reads the cached DataFrame for the given URL, if it exists and is up to date.

        Args:
            url (str): The URL associated with the cached DataFrame.

        Returns:
            Optional[DataFrame]
        """

        url = self.get_full_url(url)

        cache_file, cache_idx_file = self.get_cache_file_paths(url)
        created_on = self._get_created_on(url)

        if Path(cache_file).exists() is False or Path(cache_idx_file).exists() is False:
            return None

        with open(cache_idx_file, "r") as f:
            cached_created_on = f.read()

        return (
            None
            if cached_created_on != created_on
            else pd.read_pickle(
                cache_file,
                compression={"method": "gzip", "compresslevel": 1, "mtime": 1},
            )
        )

    def _cache_key(self, url) -> str:
        return base64.b64encode(bytes(f"{url}", "utf-8")).decode("utf-8")
