"""
GeoJSON produces and consumes only strict JSON. NAN and Infinity are not
permissible values according to the JSON specification.
"""
import unittest

import geojson


class StrictJsonTest(unittest.TestCase):
    def test_encode_nan(self):
        """
        Ensure Error is raised when encoding nan
        """
        unstrict = {
            "type": "Point",
            "coordinates": (float("nan"), 1.0),
        }
        self.assertRaises(ValueError, geojson.dumps, unstrict)

    def test_encode_inf(self):
        """
        Ensure Error is raised when encoding inf or -inf
        """
        unstrict = {
            "type": "Point",
            "coordinates": (float("inf"), 1.0),
        }
        self.assertRaises(ValueError, geojson.dumps, unstrict)

        unstrict = {
            "type": "Point",
            "coordinates": (float("-inf"), 1.0),
        }
        self.assertRaises(ValueError, geojson.dumps, unstrict)

    def test_decode_nan(self):
        """
        Ensure Error is raised when decoding NaN
        """
        unstrict = '{"type": "Point", "coordinates": [1.0, NaN]}'
        self.assertRaises(ValueError, geojson.loads, unstrict)

    def test_decode_inf(self):
        """
        Ensure Error is raised when decoding Infinity or -Infinity
        """
        unstrict = '{"type": "Point", "coordinates": [1.0, Infinity]}'
        self.assertRaises(ValueError, geojson.loads, unstrict)

        unstrict = '{"type": "Point", "coordinates": [1.0, -Infinity]}'
        self.assertRaises(ValueError, geojson.loads, unstrict)
