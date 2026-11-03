"""
Tests for geojson/base.py
"""

import copy
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


class CopyTestCase(unittest.TestCase):
    """
    Tests for shallow and deep copying of GeoJSON objects
    """

    def setUp(self):
        self.point = geojson.Point((12.0, -5.0))
        self.feature = geojson.Feature(
            geometry=self.point, properties={"city": "Rome"}, id=42
        )
        self.collection = geojson.FeatureCollection([self.feature])

    def test_copy_method_geometry(self):
        point_copy = self.point.copy()
        self.assertIsInstance(point_copy, geojson.Point)
        self.assertEqual(point_copy, self.point)
        self.assertIsNot(point_copy, self.point)
        self.assertEqual(point_copy.coordinates, [12.0, -5.0])
        self.assertTrue(point_copy.is_valid)

        point_copy["extra"] = "value"
        self.assertNotIn("extra", self.point)

    def test_copy_method_feature(self):
        feature_copy = self.feature.copy()
        self.assertIsInstance(feature_copy, geojson.Feature)
        self.assertEqual(feature_copy, self.feature)
        self.assertIsNot(feature_copy, self.feature)
        self.assertEqual(feature_copy.properties, {"city": "Rome"})
        self.assertEqual(feature_copy.id, 42)
        self.assertTrue(feature_copy.is_valid)

    def test_copy_module(self):
        point_copy = copy.copy(self.point)
        self.assertIsInstance(point_copy, geojson.Point)
        self.assertEqual(point_copy, self.point)
        self.assertIsNot(point_copy, self.point)

        collection_copy = copy.copy(self.collection)
        self.assertIsInstance(collection_copy, geojson.FeatureCollection)
        self.assertEqual(collection_copy, self.collection)
        self.assertIsNot(collection_copy, self.collection)

    def test_deepcopy_module(self):
        collection_copy = copy.deepcopy(self.collection)
        self.assertIsInstance(collection_copy, geojson.FeatureCollection)
        self.assertEqual(collection_copy, self.collection)
        self.assertIsNot(collection_copy, self.collection)
        self.assertIsNot(collection_copy[0], self.feature)
        self.assertIsNot(collection_copy[0].geometry, self.point)


class BaseTestCase(unittest.TestCase):

    def test_to_instance(self):
        FAKE = 'fake'
        self.assertEqual(FAKE, geojson.GeoJSON.to_instance(
            None, (lambda: FAKE)))

        with self.assertRaises(ValueError):
            geojson.GeoJSON.to_instance({"type": "Not GeoJSON"}, strict=True)

    def test_errors(self):
        class Fake(geojson.GeoJSON):
            pass

        with self.assertRaises(NotImplementedError):
            Fake().errors()
