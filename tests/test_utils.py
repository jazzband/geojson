"""
Tests for geojson generation
"""

import random
import unittest

import geojson
from geojson.utils import generate_random, map_geometries


def generate_bbox():
    min_lat = random.random() * 180.0 - 90.0
    max_lat = random.random() * 180.0 - 90.0
    if min_lat > max_lat:
        min_lat, max_lat = max_lat, min_lat
    min_lon = random.random() * 360.0 - 180.0
    max_lon = random.random() * 360.0 - 180.0
    if min_lon > max_lon:
        min_lon, max_lon = max_lon, min_lon
    return [min_lon, min_lat, max_lon, max_lat]


def check_polygon_bbox(polygon, bbox):
    min_lon, min_lat, max_lon, max_lat = bbox
    eps = 1e-3
    for linear_ring in polygon['coordinates']:
        for coordinate in linear_ring:
            if not (min_lon-eps <= coordinate[0] <= max_lon+eps
                    and min_lat-eps <= coordinate[1] <= max_lat+eps):
                return False
    return True


def check_point_bbox(point, bbox):
    min_lon, min_lat, max_lon, max_lat = bbox
    eps = 1e-3
    if (
        min_lon - eps <= point["coordinates"][0] <= max_lon + eps
        and min_lat - eps <= point["coordinates"][1] <= max_lat + eps
    ):
        return True
    return False


class TestGenerateRandom(unittest.TestCase):
    def test_simple_polygon(self):
        for _ in range(5000):
            bbox = [-180.0, -90.0, 180.0, 90.0]
            result = generate_random('Polygon')
            self.assertIsInstance(result, geojson.geometry.Polygon)
            self.assertTrue(geojson.geometry.check_polygon(result))
            self.assertTrue(check_polygon_bbox(result, bbox))

    def test_bbox_polygon(self):
        for _ in range(5000):
            bbox = generate_bbox()
            result = generate_random('Polygon', boundingBox=bbox)
            self.assertIsInstance(result, geojson.geometry.Polygon)
            self.assertTrue(geojson.geometry.check_polygon(result))
            self.assertTrue(check_polygon_bbox(result, bbox))

    def test_bbox_point(self):
        for _ in range(5000):
            bbox = generate_bbox()
            result = generate_random("Point", boundingBox=bbox)
            self.assertIsInstance(result, geojson.geometry.Point)
            self.assertTrue(geojson.geometry.check_point(result))
            self.assertTrue(check_point_bbox(result, bbox))

    def test_raise_value_error(self):
        with self.assertRaises(ValueError):
            generate_random("MultiPolygon")


class TestMapGeometries(unittest.TestCase):
    def test_with_simple_type(self):
        new_point = map_geometries(
            lambda g: geojson.MultiPoint([g["coordinates"]]),
            geojson.Point((-115.81, 37.24)),
        )
        self.assertEqual(new_point, geojson.MultiPoint([(-115.81, 37.24)]))

    def test_with_feature_collection(self):
        new_point = map_geometries(
            lambda g: geojson.MultiPoint([g["coordinates"]]),
            geojson.FeatureCollection([geojson.Point((-115.81, 37.24))]),
        )
        self.assertEqual(
            new_point,
            geojson.FeatureCollection(
                [geojson.MultiPoint([geojson.Point((-115.81, 37.24))])]
            ),
        )

    def test_raise_value_error(self):
        invalid_object = geojson.Feature(type="InvalidType")
        with self.assertRaises(ValueError):
            map_geometries(lambda g: g, invalid_object)
