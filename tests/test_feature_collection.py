import unittest

import geojson

class FeatureCollectionsTest(unittest.TestCase):

    def test_to_instance_converts_nested_features(self):
        """to_instance() should convert dict features to Feature objects in FeatureCollection."""
        
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
        self.assertTrue(isinstance(obj, geojson.FeatureCollection))
        self.assertTrue(isinstance(obj.features[0], geojson.Feature))
        self.assertTrue(obj.is_valid)
