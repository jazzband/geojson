import unittest

import geojson
from geojson.utils import coords, map_coords

TOO_PRECISE = (1.12341234, -2.12341234)


class CoordsTestCase(unittest.TestCase):
    def test_point(self):
        itr = coords(geojson.Point((-115.81, 37.24)))
        self.assertEqual(next(itr), (-115.81, 37.24))

    def test_point_rounding(self):
        itr = coords(geojson.Point(TOO_PRECISE))
        self.assertEqual(next(itr), tuple([round(c, 6) for c in TOO_PRECISE]))

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

    def test_featurecollection(self):
        p1 = geojson.Feature(geometry=geojson.Point((-115.11, 37.11)))
        p2 = geojson.Feature(geometry=geojson.Point((-115.22, 37.22)))
        itr = coords(geojson.FeatureCollection([p1, p2]))
        pairs = list(itr)
        self.assertEqual(pairs[0], (-115.11, 37.11))
        self.assertEqual(pairs[1], (-115.22, 37.22))

    def test_geometrycollection(self):
        p1 = geojson.Point((-115.11, 37.11))
        p2 = geojson.Point((-115.22, 37.22))
        ln = geojson.LineString(
            [(-115.3, 37.3), (-115.4, 37.4), (-115.5, 37.5)])
        g = geojson.MultiPolygon([
            ([(3.78, 9.28), (-130.91, 1.52), (35.12, 72.234), (3.78, 9.28)],),
            ([(23.18, -34.29), (-1.31, -4.61),
              (3.41, 77.91), (23.18, -34.29)],)])
        itr = coords(geojson.GeometryCollection([p1, p2, ln, g]))
        pairs = set(itr)
        self.assertEqual(pairs, {
            (-115.11, 37.11), (-115.22, 37.22),
            (-115.3, 37.3), (-115.4, 37.4), (-115.5, 37.5),
            (3.78, 9.28), (-130.91, 1.52), (35.12, 72.234), (3.78, 9.28),
            (23.18, -34.29), (-1.31, -4.61), (3.41, 77.91), (23.18, -34.29)
        })

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

    def test_map_feature(self):
        g = geojson.Feature(
            id='123',
            geometry=geojson.Point([-115.81, 37.24])
        )
        result = map_coords(lambda x: x, g)
        self.assertEqual(result['type'], 'Feature')
        self.assertEqual(result['id'], '123')
        self.assertEqual(result['geometry']['coordinates'], (-115.81, 37.24))

    def test_map_invalid(self):
        with self.assertRaises(ValueError):
            map_coords(lambda x: x, {"type": ""})
