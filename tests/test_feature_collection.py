try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import unittest

from geojson.feature import Feature, FeatureCollection


class FeatureCollectionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.feature1 = Feature(
            id="1",
            geometry={"type": "Point", "coordinates": [53.0, -4.0]},
            properties={
                "title": "Feature 1",
                "summary": "The first feature",
                "link": "http://example.org/features/1",
            },
        )
        self.feature2 = Feature(
            id="1",
            geometry={"type": "Point", "coordinates": [54.0, -3.0]},
            properties={
                "title": "Feature 2",
                "summary": "The second feature",
                "link": "http://example.org/features/2",
            },
        )

    def test_feature_collection_add(self):
        fc1 = FeatureCollection([self.feature1])
        fc2 = FeatureCollection([self.feature2])

        fc3 = fc1 + fc2

        assert len(fc1["features"]) == 1
        assert len(fc2["features"]) == 1
        assert len(fc3["features"]) == 2
        assert fc3["features"][0] == self.feature1
        assert fc3["features"][1] == self.feature2

    def test_feature_collection_radd(self):
        fc = FeatureCollection([self.feature1, self.feature2])

        list1 = [] + fc

        assert len(list1) == 2
        assert isinstance(list1, list)
        assert list1[0] == self.feature1
        assert list1[1] == self.feature2

    def test_feature_collection_append(self):
        fc = FeatureCollection([self.feature1])

        fc.append(self.feature2)

        assert len(fc["features"]) == 2
        assert fc["features"][0] == self.feature1
        assert fc["features"][1] == self.feature2

    def test_feature_collection_clear(self):
        fc = FeatureCollection([self.feature1, self.feature2])

        fc.clear()

        assert not fc["features"]

    def test_feature_collection_extend(self):
        fc1 = FeatureCollection([self.feature1])
        fc2 = FeatureCollection([self.feature2])

        fc3 = fc1 + fc2

        assert len(fc3["features"]) == 2
        assert len(fc1["features"]) == 1
        assert len(fc2["features"]) == 1
        assert fc3["features"][0] == self.feature1
        assert fc3["features"][1] == self.feature2

    def test_feature_collection_insert(self):
        fc = FeatureCollection([self.feature1])

        fc.insert(0, self.feature2)

        assert len(fc["features"]) == 2
        assert fc["features"][1] == self.feature1
        assert fc["features"][0] == self.feature2
