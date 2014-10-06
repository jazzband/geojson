# -*- coding: utf-8 -*-
"""
Tests for geojson/base.py
"""

import unittest

import geojson


class TypePropertyTestCase(unittest.TestCase):
    def test_type_property(self):
        json_str = ('{"type": "Feature",'
                    ' "geometry": null,'
                    ' "id": 1,'
                    ' "properties": {"type": "é"}}')
        geojson_obj = geojson.loads(json_str)
        self.assertTrue(isinstance(geojson_obj, geojson.GeoJSON))
        self.assertTrue("type" in geojson_obj.properties)

        json_str = ('{"type": "Feature",'
                    ' "geometry": null,'
                    ' "id": 1,'
                    ' "properties": {"type": null}}')
        geojson_obj = geojson.loads(json_str)
        self.assertTrue(isinstance(geojson_obj, geojson.GeoJSON))
        self.assertTrue("type" in geojson_obj.properties)

        json_str = ('{"type": "Feature",'
                    ' "geometry": null,'
                    ' "id": 1,'
                    ' "properties": {"type": "meow"}}')
        geojson_obj = geojson.loads(json_str)
        self.assertTrue(isinstance(geojson_obj, geojson.GeoJSON))
        self.assertTrue("type" in geojson_obj.properties)


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
