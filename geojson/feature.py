"""
SimpleWebFeature is a working example of a class that satisfies the Python geo
interface.
"""

from geojson.base import GeoJSON


class Feature(GeoJSON):
    """
    Represents a WGS84 GIS feature.
    """

    def __init__(self, id=None, geometry=None, properties=None, **extra):
        """
        Initialises a Feature object with the given parameters.

        :param id: Feature identifier, such as a sequential number.
        :type id: str, int
        :param geometry: Geometry corresponding to the feature.
        :param properties: Dict containing properties of the feature.
        :type properties: dict
        :return: Feature object
        :rtype: Feature
        """
        super(Feature, self).__init__(**extra)
        if id is not None:
            self["id"] = id
        self["geometry"] = (self.to_instance(geometry, strict=True)
                            if geometry else None)
        self["properties"] = properties or {}


class FeatureCollection(GeoJSON):
    """
    Represents a FeatureCollection, a set of multiple Feature objects.
    """

    def __init__(self, features, **extra):
        """
        Initialises a FeatureCollection object from the
        :param features: List of features to constitute the FeatureCollection.
        :type features: list
        :return: FeatureCollection object
        :rtype: FeatureCollection
        """
        super(FeatureCollection, self).__init__(**extra)
        self["features"] = features
