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

    def test_feature_collection_from_dict(self):
        """FeatureCollection should initialize properly from a dictionary (#82)."""
        feature_collection_dict = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"foo": "bar"},
                    "geometry": {
                        "type": "Point",
                        "coordinates": [0.0, 0.0],
                    },
                },
            ],
        }
        fc = geojson.FeatureCollection(feature_collection_dict)
        self.assertTrue(isinstance(fc, geojson.FeatureCollection))
        self.assertEqual(len(fc.features), 1)
        self.assertTrue(isinstance(fc.features[0], geojson.Feature))
        self.assertTrue(fc.is_valid)

