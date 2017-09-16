# -*- coding: utf-8 -*-
"""
Tests for geojson object constructor
"""

import unittest

import geojson


class TestGeoJSONConstructor(unittest.TestCase):

    def test_copy_construction(self):
        coords = [1, 2]
        pt = geojson.Point(coords)
        self.assertEquals(geojson.Point(pt), pt)

    def test_nested_constructors(self):
        a = [5, 6]
        b = [9, 10]
        c = [-5, 12]
        mp = geojson.MultiPoint([geojson.Point(a), b])
        self.assertEquals(mp.coordinates, [a, b])

        mls = geojson.MultiLineString([geojson.LineString([a, b]), [a, c]])
        self.assertEquals(mls.coordinates, [[a, b], [a, c]])

        outer = [a, b, c, a]
        poly = geojson.Polygon(geojson.MultiPoint(outer))
        other = [[1, 1], [1, 2], [2, 1], [1, 1]]
        poly2 = geojson.Polygon([outer, other])
        self.assertEquals(geojson.MultiPolygon([poly, poly2]).coordinates,
                          [[outer], [outer, other]])
