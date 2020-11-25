"""
Encoding/decoding custom objects with __geo_interface__
"""
import unittest

import geojson
from geojson.mapping import to_mapping


class EncodingDecodingTest(unittest.TestCase):

    def setUp(self):
        class Restaurant:
            """
            Basic Restaurant class
            """
            def __init__(self, name, latlng):
                super().__init__()
                self.name = name
                self.latlng = latlng

        class Restaurant1(Restaurant):
            """
            Extends Restaurant with __geo_interface__ returning dict
            """
            @property
            def __geo_interface__(self):
                return {'type': "Point", 'coordinates': self.latlng}

        class Restaurant2(Restaurant):
            """
            Extends Restaurant with __geo_interface__ returning another
            __geo_interface__ object
            """
            @property
            def __geo_interface__(self):
                return geojson.Point(self.latlng)

        class RestaurantFeature1(Restaurant):
            """
            Extends Restaurant with __geo_interface__ returning dict
            """
            @property
            def __geo_interface__(self):
                return {
                    'geometry': {
                        'type': "Point",
                        'coordinates': self.latlng,
                    },
                    'type': "Feature",
                    'properties': {
                        'name': self.name,
                    },
                }

        class RestaurantFeature2(Restaurant):
            """
            Extends Restaurant with __geo_interface__ returning another
            __geo_interface__ object
            """
            @property
            def __geo_interface__(self):
                return geojson.Feature(
                    geometry=geojson.Point(self.latlng),
                    properties={'name': self.name})

        self.name = "In N Out Burger"
        self.latlng = [-54.0, 4.0]

        self.restaurant_nogeo = Restaurant(self.name, self.latlng)

        self.restaurant1 = Restaurant1(self.name, self.latlng)
        self.restaurant2 = Restaurant2(self.name, self.latlng)

        self.restaurant_str = ('{"coordinates": [-54.0, 4.0],'
                               ' "type": "Point"}')

        self.restaurant_feature1 = RestaurantFeature1(self.name, self.latlng)
        self.restaurant_feature2 = RestaurantFeature2(self.name, self.latlng)

        self.restaurant_feature_str = ('{"geometry":'
                                       ' {"coordinates": [-54.0, 4.0],'
                                       ' "type": "Point"},'
                                       ' "properties":'
                                       ' {"name": "In N Out Burger"},'
                                       ' "type": "Feature"}')

    def test_encode(self):
        """
        Ensure objects that implement __geo_interface__ can be encoded into
        GeoJSON strings
        """
        actual = geojson.dumps(self.restaurant1, sort_keys=True)
        self.assertEqual(actual, self.restaurant_str)

        actual = geojson.dumps(self.restaurant2, sort_keys=True)
        self.assertEqual(actual, self.restaurant_str)

        # Classes that don't implement geo interface should raise TypeError
        with self.assertRaises(TypeError):
            geojson.dumps(self.restaurant_nogeo)

    def test_encode_nested(self):
        """
        Ensure nested objects that implement __geo_interface__ can be encoded
        into GeoJSON strings
        """
        actual = geojson.dumps(self.restaurant_feature1, sort_keys=True)
        self.assertEqual(actual, self.restaurant_feature_str)

        actual = geojson.dumps(self.restaurant_feature2, sort_keys=True)
        self.assertEqual(actual, self.restaurant_feature_str)

    def test_decode(self):
        """
        Ensure a GeoJSON string can be decoded into GeoJSON objects
        """
        actual = geojson.loads(self.restaurant_str)
        expected = self.restaurant1.__geo_interface__
        self.assertEqual(expected, actual)

    def test_decode_nested(self):
        """
        Ensure a GeoJSON string can be decoded into nested GeoJSON objects
        """
        actual = geojson.loads(self.restaurant_feature_str)
        expected = self.restaurant_feature1.__geo_interface__
        self.assertEqual(expected, actual)

        nested = expected['geometry']
        expected = self.restaurant1.__geo_interface__
        self.assertEqual(nested, expected)

    def test_invalid(self):
        with self.assertRaises(ValueError) as cm:
            geojson.loads('{"type":"Point", "coordinates":[[-Infinity, 4.0]]}')

        self.assertIn('is not JSON compliant', str(cm.exception))

    def test_mapping(self):
        self.assertEqual(to_mapping(geojson.Point([1.0, 2.0])),
                         {"coordinates": [1.0, 2.0], "type": "Point"})

    def test_GeoJSON(self):
        self.assertEqual(None, geojson.GeoJSON().__geo_interface__)

        self.assertEqual({"type": "GeoJSON"}, to_mapping(geojson.GeoJSON()))
