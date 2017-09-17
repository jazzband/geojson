# -*- coding: utf-8 -*-
"""
Tests for geojson/validation
"""

import unittest

import geojson

INVALID_POS = (10, 20, 30, 40)
VALID_POS = (10, 20)
VALID_POS_WITH_ELEVATION = (10, 20, 30)


class TestValidationGeometry(unittest.TestCase):

    def test_invalid_geometry_with_validate(self):
        with self.assertRaises(ValueError):
            geojson.Point(INVALID_POS, validate=True)

    def test_invalid_geometry_without_validate(self):
        geojson.Point(INVALID_POS)
        geojson.Point(INVALID_POS, validate=False)

    def test_valid_geometry(self):
        geojson.Point(VALID_POS, validate=True)

    def test_valid_geometry_with_elevation(self):
        geojson.Point(VALID_POS_WITH_ELEVATION, validate=True)

    def test_not_sequence(self):
        with self.assertRaises(ValueError) as cm:
            geojson.MultiPoint([5], validate=True)

        self.assertIn('each position must be a list', str(cm.exception))

    def test_not_number(self):
        with self.assertRaises(ValueError) as cm:
            geojson.MultiPoint([[1, '?']], validate=False)

        self.assertIn('is not a JSON compliant number', str(cm.exception))


class TestValidationGeoJSONObject(unittest.TestCase):

    def test_valid_jsonobject(self):
        point = geojson.Point((-10.52, 2.33))
        self.assertEqual(point.is_valid, True)


class TestValidationPoint(unittest.TestCase):

    def test_invalid_point(self):
        point = geojson.Point((10, 20, 30, 40))
        self.assertEqual(point.is_valid, False)

    def test_valid_point(self):
        point = geojson.Point((-3.68, 40.41))
        self.assertEqual(point.is_valid, True)

    def test_valid_point_with_elevation(self):
        point = geojson.Point((-3.68, 40.41, 3.45))
        self.assertEqual(point.is_valid, True)


class TestValidationMultipoint(unittest.TestCase):

    def test_invalid_multipoint(self):
        mpoint = geojson.MultiPoint(
            [(3.5887,), (3.5887, 10.44558),
             (2.5555, 3.887, 4.56), (2.44, 3.44, 2.555, 4.56)])
        self.assertEqual(mpoint.is_valid, False)

    def test_valid_multipoint(self):
        mpoint = geojson.MultiPoint([(10, 20), (30, 40)])
        self.assertEqual(mpoint.is_valid, True)

    def test_valid_multipoint_with_elevation(self):
        mpoint = geojson.MultiPoint([(10, 20, 30), (30, 40, 50)])
        self.assertEqual(mpoint.is_valid, True)


class TestValidationLineString(unittest.TestCase):

    def test_invalid_linestring(self):
        with self.assertRaises(ValueError) as cm:
            geojson.LineString([(8.919, 44.4074)], validate=True)

        self.assertIn('must be an array of two or more positions',
                      str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            geojson.LineString([(8.919, 44.4074), [3]], validate=True)

        self.assertIn('a position must have exactly 2 or 3 values',
                      str(cm.exception))

    def test_valid_linestring(self):
        ls = geojson.LineString([(10, 5), (4, 3)])
        self.assertEqual(ls.is_valid, True)


class TestValidationMultiLineString(unittest.TestCase):

    def test_invalid_multilinestring(self):
        with self.assertRaises(ValueError) as cm:
            geojson.MultiLineString([1], validate=True)

        self.assertIn('each line must be a list of positions',
                      str(cm.exception))

        mls = geojson.MultiLineString([[(10, 5), (20, 1)], []])
        self.assertEqual(mls.is_valid, False)

    def test_valid_multilinestring(self):
        ls1 = [(3.75, 9.25), (-130.95, 1.52)]
        ls2 = [(23.15, -34.25), (-1.35, -4.65), (3.45, 77.95)]
        mls = geojson.MultiLineString([ls1, ls2])
        self.assertEqual(mls.is_valid, True)


class TestValidationPolygon(unittest.TestCase):

    def test_invalid_polygon(self):
        with self.assertRaises(ValueError) as cm:
            geojson.Polygon([1], validate=True)

        self.assertIn("Each element of a polygon's coordinates must be a list",
                      str(cm.exception))

        poly1 = geojson.Polygon(
            [[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15)]])
        self.assertEqual(poly1.is_valid, False)
        poly2 = geojson.Polygon(
            [[(2.38, 57.322), (23.194, -20.28),
                (-120.43, 19.15), (2.38, 57.323)]])
        self.assertEqual(poly2.is_valid, False)

    def test_valid_polygon(self):
        poly = geojson.Polygon(
            [[(2.38, 57.322), (23.194, -20.28),
                (-120.43, 19.15), (2.38, 57.322)]])
        self.assertEqual(poly.is_valid, True)


class TestValidationMultiPolygon(unittest.TestCase):

    def test_invalid_multipolygon(self):
        with self.assertRaises(ValueError) as cm:
            geojson.MultiPolygon([1], validate=True)

        self.assertIn("Each polygon must be a list of linear rings",
                      str(cm.exception))

        poly1 = [(2.38, 57.322), (23.194, -20.28),
                 (-120.43, 19.15), (25.44, -17.91)]
        poly2 = [(2.38, 57.322), (23.194, -20.28),
                 (-120.43, 19.15), (2.38, 57.322)]
        multipoly = geojson.MultiPolygon([poly1, poly2])
        self.assertEqual(multipoly.is_valid, False)

    def test_valid_multipolygon(self):
        poly1 = [[(2.38, 57.322), (23.194, -20.28),
                  (-120.43, 19.15), (2.38, 57.322)]]
        poly2 = [[(-5.34, 3.71), (28.74, 31.44),
                  (28.55, 19.10), (-5.34, 3.71)]]
        poly3 = [[(3.14, 23.17), (51.34, 27.14),
                  (22, -18.11), (3.14, 23.17)]]
        multipoly = geojson.MultiPolygon([poly1, poly2, poly3])
        self.assertEqual(multipoly.is_valid, True)


class TestValidationGeometryCollection(unittest.TestCase):

    def test_invalid_geometrycollection(self):
        point = geojson.Point((10, 20))
        bad_poly = geojson.Polygon([[(2.38, 57.322), (23.194, -20.28),
                                   (-120.43, 19.15), (25.44, -17.91)]])

        geom_collection = geojson.GeometryCollection(
                geometries=[point, bad_poly]
            )
        self.assertFalse(geom_collection.is_valid)

    def test_valid_geometrycollection(self):
        point = geojson.Point((10, 20))
        poly = geojson.Polygon([[(2.38, 57.322), (23.194, -20.28),
                                (-120.43, 19.15), (2.38, 57.322)]])

        geom_collection = geojson.GeometryCollection(
                geometries=[point, poly]
            )
        self.assertTrue(geom_collection.is_valid)
