from io import BytesIO  # NOQA
import unittest

import geojson


class FeaturesTest(unittest.TestCase):
    def test_protocol(self):
        """
        A dictionary can satisfy the protocol
        """
        f = {
            'type': 'Feature',
            'id': '1',
            'geometry': {'type': 'Point', 'coordinates': [53, -4]},
            'properties': {'title': 'Dict 1'},
        }

        json = geojson.dumps(f, sort_keys=True)
        self.assertEqual(json, '{"geometry":'
                               ' {"coordinates": [53, -4],'
                               ' "type": "Point"},'
                               ' "id": "1",'
                               ' "properties": {"title": "Dict 1"},'
                               ' "type": "Feature"}')

        o = geojson.loads(json)
        output = geojson.dumps(o, sort_keys=True)
        self.assertEqual(output, '{"geometry":'
                                 ' {"coordinates": [53, -4],'
                                 ' "type": "Point"},'
                                 ' "id": "1",'
                                 ' "properties": {"title": "Dict 1"},'
                                 ' "type": "Feature"}')

    def test_unicode_properties(self):
        with open("tests/data.geojson") as file_:
            obj = geojson.load(file_)
        geojson.dumps(obj)

    def test_feature_class(self):
        """
        Test the Feature class
        """

        from geojson.examples import SimpleWebFeature
        feature = SimpleWebFeature(
            id='1',
            geometry={'type': 'Point', 'coordinates': [53, -4]},
            title='Feature 1', summary='The first feature',
            link='http://example.org/features/1'
        )

        # It satisfies the feature protocol
        self.assertEqual(feature.id, '1')
        self.assertEqual(feature.properties['title'], 'Feature 1')
        self.assertEqual(feature.properties['summary'], 'The first feature')
        self.assertEqual(feature.properties['link'],
                         'http://example.org/features/1')
        self.assertEqual(geojson.dumps(feature.geometry, sort_keys=True),
                         '{"coordinates": [53, -4], "type": "Point"}')

        # Encoding
        json = ('{"geometry": {"coordinates": [53, -4],'
                ' "type": "Point"},'
                ' "id": "1",'
                ' "properties":'
                ' {"link": "http://example.org/features/1",'
                ' "summary": "The first feature",'
                ' "title": "Feature 1"},'
                ' "type": "Feature"}')
        self.assertEqual(geojson.dumps(feature, sort_keys=True), json)

        # Decoding
        factory = geojson.examples.create_simple_web_feature
        json = ('{"geometry": {"type": "Point",'
                ' "coordinates": [53, -4]},'
                ' "id": "1",'
                ' "properties": {"summary": "The first feature",'
                ' "link": "http://example.org/features/1",'
                ' "title": "Feature 1"}}')
        feature = geojson.loads(json, object_hook=factory, encoding="utf-8")
        self.assertEqual(repr(type(feature)),
                         "<class 'geojson.examples.SimpleWebFeature'>")
        self.assertEqual(feature.id, '1')
        self.assertEqual(feature.properties['title'], 'Feature 1')
        self.assertEqual(feature.properties['summary'], 'The first feature')
        self.assertEqual(feature.properties['link'],
                         'http://example.org/features/1')
        self.assertEqual(geojson.dumps(feature.geometry, sort_keys=True),
                         '{"coordinates": [53, -4], "type": "Point"}')

    def test_geo_interface(self):
        class Thingy(object):
            def __init__(self, id, title, x, y):
                self.id = id
                self.title = title
                self.x = x
                self.y = y

            @property
            def __geo_interface__(self):
                return ({"id": self.id,
                         "properties": {"title": self.title},
                         "geometry": {"type": "Point",
                                      "coordinates": (self.x, self.y)}})

        ob = Thingy('1', 'thingy one', -106, 40)
        self.assertEqual(geojson.dumps(ob.__geo_interface__['geometry'],
                                       sort_keys=True),
                         '{"coordinates": [-106, 40], "type": "Point"}')
        self.assertEqual(geojson.dumps(ob, sort_keys=True),
                         ('{"geometry": {"coordinates": [-106, 40],'
                          ' "type": "Point"},'
                          ' "id": "1",'
                          ' "properties": {"title": "thingy one"}}'))
