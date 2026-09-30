"""
Tests for geojson object constructor
"""

from dataclasses import asdict, dataclass
import json
import unittest

import geojson


class TestGeoJSONConstructor(unittest.TestCase):

    def test_copy_construction(self):
        coords = [1, 2]
        pt = geojson.Point(coords)
        self.assertEqual(geojson.Point(pt), pt)

    def test_nested_constructors(self):
        a = [5, 6]
        b = [9, 10]
        c = [-5, 12]
        mp = geojson.MultiPoint([geojson.Point(a), b])
        self.assertEqual(mp.coordinates, [a, b])

        mls = geojson.MultiLineString([geojson.LineString([a, b]), [a, c]])
        self.assertEqual(mls.coordinates, [[a, b], [a, c]])

        outer = [a, b, c, a]
        poly = geojson.Polygon(geojson.MultiPoint(outer))
        other = [[1, 1], [1, 2], [2, 1], [1, 1]]
        poly2 = geojson.Polygon([outer, other])
        self.assertEqual(geojson.MultiPolygon([poly, poly2]).coordinates,
                         [[outer], [outer, other]])

    def test_dict_construction(self):
        pt_dict = {"type": "Point", "coordinates": [1.0, 2.0]}
        pt = geojson.Point(pt_dict)
        self.assertEqual(pt.coordinates, [1.0, 2.0])
        self.assertTrue(pt.is_valid)

        feat_dict = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [1.0, 2.0]},
            "properties": {"name": "test"},
        }
        feat = geojson.Feature(feat_dict)
        self.assertEqual(feat.properties, {"name": "test"})
        self.assertEqual(feat.geometry.coordinates, [1.0, 2.0])
        self.assertTrue(feat.is_valid)

        gc_dict = {
            "type": "GeometryCollection",
            "geometries": [{"type": "Point", "coordinates": [1.0, 2.0]}],
        }
        gc = geojson.GeometryCollection(gc_dict)
        self.assertEqual(len(gc.geometries), 1)
        self.assertTrue(gc.is_valid)

    def test_dataclass_asdict(self):
        @dataclass
        class Container:
            point: geojson.Point
            feature: geojson.Feature
            feature_collection: geojson.FeatureCollection

        pt = geojson.Point([1.0, 2.0])
        feat = geojson.Feature(geometry=pt, properties={"name": "alpha"})
        fc = geojson.FeatureCollection([feat])

        c = Container(point=pt, feature=feat, feature_collection=fc)
        d = asdict(c)

        self.assertEqual(d["point"]["type"], "Point")
        self.assertEqual(d["point"]["coordinates"], [1.0, 2.0])
        self.assertEqual(d["feature"]["type"], "Feature")
        self.assertEqual(d["feature"]["geometry"]["coordinates"], [1.0, 2.0])
        self.assertEqual(d["feature_collection"]["type"], "FeatureCollection")
        self.assertEqual(len(d["feature_collection"]["features"]), 1)

        # Ensure it is JSON-serializable
        encoded = json.dumps(d)
        self.assertIn('"type": "FeatureCollection"', encoded)
