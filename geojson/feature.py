"""
SimpleWebFeature is a working example of a class that satisfies the Python geo
interface.
"""

from geojson.base import GeoJSON


class Feature(GeoJSON):

    """A (WGS84) GIS Feature."""

    def __init__(self, id=None, geometry=None, properties=None, **extra):
        super(Feature, self).__init__(**extra)
        self["id"] = id
        self["geometry"] = (self.to_instance(geometry, strict=True)
                            if geometry else None)
        self["properties"] = properties or {}


class FeatureCollection(GeoJSON):

    """A collection of Features."""

    def __init__(self, features, **extra):
        super(FeatureCollection, self).__init__(**extra)
        self["features"] = features
