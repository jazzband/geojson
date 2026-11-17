import unittest
from io import StringIO

import geojson


class FeaturePropertiesTest(unittest.TestCase):
    def test_geojson_type_in_properties_is_preserved(self):
        source = ('{"type": "Feature", "geometry": null, "id": 1, '
                  '"properties": {"type": "Feature"}}')
        for decode, payload in ((geojson.loads, source),
                                (geojson.load, StringIO(source))):
            with self.subTest(decoder=decode.__name__):
                feature = decode(payload)
                self.assertIsInstance(feature, geojson.Feature)
                self.assertIs(type(feature.properties), dict)
                self.assertEqual(feature.properties, {"type": "Feature"})
