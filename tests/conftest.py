import pytest
import pandas as pd


@pytest.fixture
def dataframe():
    return pd.DataFrame({
        "name": ["New York", "Los Angeles", "Chicago"],
        "population": [8_336_817, 3_979_576, 2_693_976]
    })


@pytest.fixture
def geo_dataframe():
    return pd.DataFrame({
        "name": ["New York", "Los Angeles", "Chicago"],
        "latitude": [40.7128, 34.0522, 41.8781],
        "longitude": [-74.0060, -118.2437, -87.6298]
    })