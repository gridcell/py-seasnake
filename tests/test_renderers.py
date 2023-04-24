import json

import pytest

from seasnake.renderers import to_geojson

def test_to_geojson(geo_dataframe):
    geojson_str = to_geojson(geo_dataframe)
    geojson = json.loads(geojson_str)
    assert geojson is not None
    assert geojson["features"][1]["geometry"]["coordinates"] == [-118.2437, 34.0522]


def test_to_geojson_empty(dataframe):
    with pytest.raises(ValueError):
        to_geojson(dataframe)
 