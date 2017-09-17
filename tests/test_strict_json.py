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
        self._raises_on_dump({
            "type": "Point",
            "coordinates": (float("nan"), 1.0),
        })

    def test_encode_inf(self):
        """
        Ensure Error is raised when encoding inf or -inf
        """
        self._raises_on_dump({
            "type": "Point",
            "coordinates": (float("inf"), 1.0),
        })

        self._raises_on_dump({
            "type": "Point",
            "coordinates": (float("-inf"), 1.0),
        })

    def _raises_on_dump(self, unstrict):
        with self.assertRaises(ValueError):
            geojson.dumps(unstrict)

    def test_decode_nan(self):
        """
        Ensure Error is raised when decoding NaN
        """
        self._raises_on_load('{"type": "Point", "coordinates": [1.0, NaN]}')

    def test_decode_inf(self):
        """
        Ensure Error is raised when decoding Infinity or -Infinity
        """
        self._raises_on_load(
            '{"type": "Point", "coordinates": [1.0, Infinity]}')

        self._raises_on_load(
            '{"type": "Point", "coordinates": [1.0, -Infinity]}')

    def _raises_on_load(self, unstrict):
        with self.assertRaises(ValueError):
            geojson.loads(unstrict)
