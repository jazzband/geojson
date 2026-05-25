from io import StringIO
import json
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
            'geometry': {'type': 'Point', 'coordinates': [53.0, -4.0]},
            'properties': {'title': 'Dict 1'},
        }

        json_str = geojson.dumps(f, sort_keys=True)
        # Parse JSON to avoid formatting issues across Python versions
        json_obj = json.loads(json_str)

        expected = {
            "geometry": {"coordinates": [53.0, -4.0], "type": "Point"},
            "id": "1",
            "properties": {"title": "Dict 1"},
            "type": "Feature"
        }
        self.assertEqual(json_obj, expected)

        o = geojson.loads(json_str)
        output_str = geojson.dumps(o, sort_keys=True)
        output_obj = json.loads(output_str)
        self.assertEqual(output_obj, expected)

    def test_unicode_properties(self):
        with open("tests/data.geojson") as file_:
            obj = geojson.load(file_)
        geojson.dump(obj, StringIO())

    def test_feature_class(self):
        """
        Test the Feature class
        """

        from geojson.examples import SimpleWebFeature
        feature = SimpleWebFeature(
            id='1',
            geometry={'type': 'Point', 'coordinates': [53.0, -4.0]},
            title='Feature 1', summary='The first feature',
            link='http://example.org/features/1'
        )

        # It satisfies the feature protocol
        self.assertEqual(feature.id, '1')
        self.assertEqual(feature.properties['title'], 'Feature 1')
        self.assertEqual(feature.properties['summary'], 'The first feature')
        self.assertEqual(feature.properties['link'],
                         'http://example.org/features/1')

        # Encoding - use JSON comparison to avoid formatting issues
        geometry_obj = json.loads(geojson.dumps(feature.geometry, sort_keys=True))
        self.assertEqual(geometry_obj, {"coordinates": [53.0, -4.0], "type": "Point"})

        expected_feature = {
            "geometry": {"coordinates": [53.0, -4.0], "type": "Point"},
            "id": "1",
            "properties": {
                "link": "http://example.org/features/1",
                "summary": "The first feature",
                "title": "Feature 1"
            },
            "type": "Feature"
        }

        feature_json_obj = json.loads(geojson.dumps(feature, sort_keys=True))
        self.assertEqual(feature_json_obj, expected_feature)

        # Decoding
        factory = geojson.examples.create_simple_web_feature
        json_str = ('{"geometry": {"type": "Point",'
                ' "coordinates": [53.0, -4.0]},'
                ' "id": "1",'
                ' "properties": {"summary": "The first feature",'
                ' "link": "http://example.org/features/1",'
                ' "title": "Feature 1"}}')
        feature = geojson.loads(json_str, object_hook=factory)
        self.assertEqual(repr(type(feature)),
                         "<class 'geojson.examples.SimpleWebFeature'>")
        self.assertEqual(feature.id, '1')
        self.assertEqual(feature.properties['title'], 'Feature 1')
        self.assertEqual(feature.properties['summary'], 'The first feature')
        self.assertEqual(feature.properties['link'],
                         'http://example.org/features/1')

        # Compare geometry using JSON
        geom_obj = json.loads(geojson.dumps(feature.geometry, sort_keys=True))
        self.assertEqual(geom_obj, {"coordinates": [53.0, -4.0], "type": "Point"})

    def test_geo_interface(self):
        class Thingy:
            def __init__(self, id, title, x, y):
                self.id = id
                self.title = title
                self.x = x
                self.y = y

            @property
            def __geo_interface__(self):
                return {"id": self.id,
                         "properties": {"title": self.title},
                         "geometry": {"type": "Point",
                                      "coordinates": (self.x, self.y)}}

        ob = Thingy('1', 'thingy one', -106.0, 40.0)

        # Use JSON comparison for geometry
        geom_json = json.loads(geojson.dumps(ob.__geo_interface__['geometry'],
                                       sort_keys=True))
        self.assertEqual(geom_json, {"coordinates": [-106.0, 40.0], "type": "Point"})

        # Use JSON comparison for the whole object
        expected_obj = {
            "geometry": {"coordinates": [-106.0, 40.0], "type": "Point"},
            "id": "1",
            "properties": {"title": "thingy one"},
            "type": "Feature"
        }
        ob_json = json.loads(geojson.dumps(ob, sort_keys=True))
        self.assertEqual(ob_json, expected_obj)


if __name__ == '__main__':
    unittest.main()
