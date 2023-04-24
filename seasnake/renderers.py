import json
from typing import Optional

from pandas import DataFrame


def to_geojson(df: DataFrame, x_key: str = "longitude", y_key: str = "latitude") -> Optional[str]:
    """Converts a DataFrame to GeoJSON.

    Args:
        df (DataFrame): The DataFrame to convert.
        x_key (str, optional): The key in the DataFrame that contains the longitude.
            Defaults to "longitude".
        y_key (str, optional): The key in the DataFrame that contains the
            latitude. Defaults to "latitude".

    Returns:
        Optional[str]: The GeoJSON representation of the DataFrame.
    
    Examples:
    ```
    from seasnake import MermaidAuth, FishBeltTransect, to_geojson  
    
    auth = MermaidAuth()
    fish_belt = FishBeltTransect(token=auth.get_token())
    project_id = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
    geojson = to_geojson(fish_belt.sample_events(project_id))
    print(geojson)
    ```

    """

    if df.empty:
        return None

    if x_key not in df.columns or y_key not in df.columns:
        raise ValueError(f"DataFrame must contain columns '{x_key}' and '{y_key}'.")

    features = []
    for _, row in df.iterrows():
        properties = {col: row[col] for col in df.columns}
        geometry = {
            "type": "Point",
            "coordinates": [row[x_key], row[y_key]]
        }
        feature = {
            "type": "Feature",
            "properties": properties,
            "geometry": geometry
        }
        features.append(feature)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return json.dumps(geojson, ensure_ascii=False)
