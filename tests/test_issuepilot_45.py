import json
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

    def test_custom_decoder_receives_the_geojson_object_hook(self):
        hooks = []

        class HookAwareDecoder(json.JSONDecoder):
            def __init__(self, *, object_hook=None, **kwargs):
                hooks.append(object_hook)
                super().__init__(object_hook=object_hook, **kwargs)

        source = '{"type": "Point", "coordinates": [1, 2]}'
        for decode, payload in ((geojson.loads, source),
                                (geojson.load, StringIO(source))):
            with self.subTest(decoder=decode.__name__):
                self.assertIsInstance(decode(payload, cls=HookAwareDecoder), geojson.Point)
                self.assertEqual(hooks[-1], geojson.GeoJSON.to_instance)
