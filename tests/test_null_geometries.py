import unittest

import geojson


class NullGeometriesTest(unittest.TestCase):

    def test_null_geometry_explicit(self):
        feature = geojson.Feature(
            id=12,
            geometry=None,
            properties={'foo': 'bar'}
        )
        actual = geojson.dumps(feature, sort_keys=True)
        expected = ('{"geometry": null, "id": 12, "properties": {"foo": '
                    '"bar"}, "type": "Feature"}')
        self.assertEqual(actual, expected)

    def test_null_geometry_implicit(self):
        feature = geojson.Feature(
            id=12,
            properties={'foo': 'bar'}
        )
        actual = geojson.dumps(feature, sort_keys=True)
        expected = ('{"geometry": null, "id": 12, "properties": {"foo": '
                    '"bar"}, "type": "Feature"}')
        self.assertEqual(actual, expected)
