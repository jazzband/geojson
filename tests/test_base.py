"""
Tests for geojson/base.py
"""

import unittest

import geojson


class OperatorOverloadingTestCase(unittest.TestCase):
    """
    Tests for operator overloading
    """

    def setUp(self):
        self.coords = (12, -5)
        self.point = geojson.Point(self.coords)

    def test_setattr(self):
        new_coords = (27, 42)
        self.point.coordinates = new_coords
        self.assertEqual(self.point['coordinates'], new_coords)

    def test_getattr(self):
        self.assertEqual(self.point['coordinates'], self.point.coordinates)

    def test_delattr(self):
        del self.point.coordinates
        self.assertFalse(hasattr(self.point, 'coordinates'))
