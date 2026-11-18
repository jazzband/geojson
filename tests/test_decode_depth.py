import json
import unittest
from io import StringIO

import geojson


class DecoderDepthTests(unittest.TestCase):
    def test_foreign_member_nesting_keeps_json_decoder_depth_support(self):
        # JSON nesting limits vary between Python runtimes.
        for depth in (1100, 600, 200):
            nested = "[" * depth + '"leaf"' + "]" * depth
            payload = ('{"type":"Feature","geometry":null,"properties":{},'
                       '"extra":' + nested + '}')
            try:
                reference = json.loads(
                    payload, object_hook=geojson.GeoJSON.to_instance)
            except RecursionError:
                continue
            break
        else:
            self.fail("The JSON decoder could not decode the control input")
        self.assertIsInstance(reference, geojson.Feature)
        for decode, data in ((geojson.loads, payload),
                             (geojson.load, StringIO(payload))):
            with self.subTest(decoder=decode.__name__):
                try:
                    feature = decode(data)
                except RecursionError:
                    self.fail("GeoJSON rejected nesting accepted by JSON")
                self.assertIsInstance(feature, geojson.Feature)
                value = feature["extra"]
                for _ in range(depth):
                    self.assertIsInstance(value, list)
                    value = value[0]
                self.assertEqual(value, "leaf")

    def test_feature_properties_and_sibling_objects_keep_their_context(self):
        properties = {"type": "Point", "coordinates": [1, 2]}
        payload = json.dumps({
            "first": {"type": "Feature", "geometry": None,
                      "properties": properties},
            "properties": {"type": "Point", "coordinates": [3, 4]},
        })
        result = geojson.loads(payload)
        self.assertIsInstance(result["first"], geojson.Feature)
        self.assertIs(type(result["first"].properties), dict)
        self.assertEqual(result["first"].properties, properties)
        self.assertIsInstance(result["properties"], geojson.Point)
