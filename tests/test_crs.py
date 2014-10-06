import unittest

import geojson


class CRSTest(unittest.TestCase):

    def setUp(self):
        self.crs = geojson.crs.Named(
            properties={
                "name": "urn:ogc:def:crs:EPSG::3785",
            }
        )

    def test_crs_repr(self):
        actual = repr(self.crs)
        expected = ('{"properties": {"name": "urn:ogc:def:crs:EPSG::3785"},'
                    ' "type": "name"}')
        self.assertEqual(actual, expected)

    def test_crs_encode(self):
        actual = geojson.dumps(self.crs, sort_keys=True)
        expected = ('{"properties": {"name": "urn:ogc:def:crs:EPSG::3785"},'
                    ' "type": "name"}')
        self.assertEqual(actual, expected)

    def test_crs_decode(self):
        dumped = geojson.dumps(self.crs)
        actual = geojson.loads(dumped)
        self.assertEqual(actual, self.crs)
