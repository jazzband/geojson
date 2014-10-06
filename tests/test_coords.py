import unittest

import geojson
from geojson.utils import coords, map_coords


class CoordsTestCase(unittest.TestCase):
    def test_point(self):
        itr = coords(geojson.Point((-115.81, 37.24)))
        self.assertEqual(next(itr), (-115.81, 37.24))

    def test_dict(self):
        itr = coords({'type': 'Point', 'coordinates': [-115.81, 37.24]})
        self.assertEqual(next(itr), (-115.81, 37.24))

    def test_point_feature(self):
        itr = coords(geojson.Feature(geometry=geojson.Point((-115.81, 37.24))))
        self.assertEqual(next(itr), (-115.81, 37.24))

    def test_multipolygon(self):
        g = geojson.MultiPolygon([
            ([(3.78, 9.28), (-130.91, 1.52), (35.12, 72.234), (3.78, 9.28)],),
            ([(23.18, -34.29), (-1.31, -4.61),
              (3.41, 77.91), (23.18, -34.29)],)])
        itr = coords(g)
        pairs = list(itr)
        self.assertEqual(pairs[0], (3.78, 9.28))
        self.assertEqual(pairs[-1], (23.18, -34.29))

    def test_map_point(self):
        result = map_coords(lambda x: x, geojson.Point((-115.81, 37.24)))
        self.assertEqual(result['type'], 'Point')
        self.assertEqual(result['coordinates'], (-115.81, 37.24))

    def test_map_linestring(self):
        g = geojson.LineString(
            [(3.78, 9.28), (-130.91, 1.52), (35.12, 72.234), (3.78, 9.28)])
        result = map_coords(lambda x: x, g)
        self.assertEqual(result['type'], 'LineString')
        self.assertEqual(result['coordinates'][0], (3.78, 9.28))
        self.assertEqual(result['coordinates'][-1], (3.78, 9.28))

    def test_map_polygon(self):
        g = geojson.Polygon([
            [(3.78, 9.28), (-130.91, 1.52), (35.12, 72.234), (3.78, 9.28)], ])
        result = map_coords(lambda x: x, g)
        self.assertEqual(result['type'], 'Polygon')
        self.assertEqual(result['coordinates'][0][0], (3.78, 9.28))
        self.assertEqual(result['coordinates'][0][-1], (3.78, 9.28))

    def test_map_multipolygon(self):
        g = geojson.MultiPolygon([
            ([(3.78, 9.28), (-130.91, 1.52), (35.12, 72.234), (3.78, 9.28)],),
            ([(23.18, -34.29), (-1.31, -4.61),
              (3.41, 77.91), (23.18, -34.29)],)])
        result = map_coords(lambda x: x, g)
        self.assertEqual(result['type'], 'MultiPolygon')
        self.assertEqual(result['coordinates'][0][0][0], (3.78, 9.28))
        self.assertEqual(result['coordinates'][-1][-1][-1], (23.18, -34.29))
