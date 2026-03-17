

def test_to_instance_converts_nested_features():
    """to_instance() should convert dict features to Feature objects in FeatureCollection."""
    import geojson

    feature_collection_dict = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"foo": "bar"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]],
                },
            },
        ],
    }

    obj = geojson.GeoJSON.to_instance(feature_collection_dict)
    assert isinstance(obj, geojson.FeatureCollection)
    assert isinstance(obj.features[0], geojson.Feature)
    assert obj.is_valid
