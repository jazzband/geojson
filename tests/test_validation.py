# -*- coding: utf-8 -*-
"""
Tests for geojson/validation
"""

import unittest

import geojson

is_valid = geojson.is_valid
YES = 'yes'
NO = 'no'


class TestValidationGeometry(unittest.TestCase):

    def test_invalid_geometry_with_validate(self):
        self.assertRaises(
            ValueError, geojson.Point, (10, 20, 30), validate=True)

    def test_invalid_geometry_without_validate(self):
        try:
            geojson.Point((10, 20, 30))
            geojson.Point((10, 20, 30), validate=False)
        except ValueError:
            self.fail("Point raised ValueError unexpectedly")

    def test_valid_geometry(self):
        try:
            geojson.Point((10, 20), validate=True)
            geojson.Point((10, 20), validate=False)
        except ValueError:
            self.fail("Point raised ValueError unexpectedly")


class TestValidationGeoJSONObject(unittest.TestCase):

    def test_invalid_jsonobject(self):
        obj = [1, 2, 3]
        self.assertEqual(is_valid(obj)['valid'], NO)

    def test_valid_jsonobject(self):
        point = geojson.Point((-10.52, 2.33))
        self.assertEqual(is_valid(point)['valid'], YES)


class TestValidationPoint(unittest.TestCase):

    def test_invalid_point(self):
        point = geojson.Point((10, 20, 30))
        self.assertEqual(is_valid(point)['valid'], NO)

    def test_valid_point(self):
        point = geojson.Point((-3.68, 40.41))
        self.assertEqual(is_valid(point)['valid'], YES)


class TestValidationMultipoint(unittest.TestCase):

    def test_invalid_multipoint(self):
        mpoint = geojson.MultiPoint(
            [(3.5887, 10.44558), (2.5555, 3.887), (2.44, 3.44, 2.555)])
        self.assertEqual(is_valid(mpoint)['valid'], NO)

    def test_valid_multipoint(self):
        mpoint = geojson.MultiPoint([(10, 20), (30, 40)])
        self.assertEqual(is_valid(mpoint)['valid'], YES)


class TestValidationLineString(unittest.TestCase):

    def test_invalid_linestring(self):
        ls = geojson.LineString([(8.919, 44.4074)])
        self.assertEqual(is_valid(ls)['valid'], NO)

    def test_valid_linestring(self):
        ls = geojson.LineString([(10, 5), (4, 3)])
        self.assertEqual(is_valid(ls)['valid'], YES)


class TestValidationMultiLineString(unittest.TestCase):

    def test_invalid_multilinestring(self):
        mls = geojson.MultiLineString([[(10, 5), (20, 1)], []])
        self.assertEqual(is_valid(mls)['valid'], NO)

    def test_valid_multilinestring(self):
        ls1 = [(3.75, 9.25), (-130.95, 1.52)]
        ls2 = [(23.15, -34.25), (-1.35, -4.65), (3.45, 77.95)]
        mls = geojson.MultiLineString([ls1, ls2])
        self.assertEqual(is_valid(mls)['valid'], YES)


class TestValidationPolygon(unittest.TestCase):

    def test_invalid_polygon(self):
        poly1 = geojson.Polygon(
            [[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15)]])
        self.assertEqual(is_valid(poly1)['valid'], NO)
        poly2 = geojson.Polygon(
            [[(2.38, 57.322), (23.194, -20.28),
                (-120.43, 19.15), (2.38, 57.323)]])
        self.assertEqual(is_valid(poly2)['valid'], NO)

    def test_valid_polygon(self):
        poly = geojson.Polygon(
            [[(2.38, 57.322), (23.194, -20.28),
                (-120.43, 19.15), (2.38, 57.322)]])
        self.assertEqual(is_valid(poly)['valid'], YES)


class TestValidationMultiPolygon(unittest.TestCase):

    def test_invalid_multipolygon(self):
        poly1 = [(2.38, 57.322), (23.194, -20.28),
                 (-120.43, 19.15), (25.44, -17.91)]
        poly2 = [(2.38, 57.322), (23.194, -20.28),
                 (-120.43, 19.15), (2.38, 57.322)]
        multipoly = geojson.MultiPolygon([poly1, poly2])
        self.assertEqual(is_valid(multipoly)['valid'], NO)

    def test_valid_multipolygon(self):
        poly1 = [[(2.38, 57.322), (23.194, -20.28),
                  (-120.43, 19.15), (2.38, 57.322)]]
        poly2 = [[(-5.34, 3.71), (28.74, 31.44),
                  (28.55, 19.10), (-5.34, 3.71)]]
        poly3 = [[(3.14, 23.17), (51.34, 27.14),
                  (22, -18.11), (3.14, 23.17)]]
        multipoly = geojson.MultiPolygon([poly1, poly2, poly3])
        self.assertEqual(is_valid(multipoly)['valid'], YES)
