from geojson.base import GeoJSON


class CoordinateReferenceSystem(GeoJSON):

    def __init__(self, properties=None, **extra):
        super(CoordinateReferenceSystem, self).__init__(**extra)
        self["properties"] = properties or {}


class Named(CoordinateReferenceSystem):

    def __init__(self, properties=None, **extra):
        super(Named, self).__init__(properties=properties, **extra)
        self["type"] = "name"

    def __repr__(self):
        return super(Named, self).__repr__()


class Linked(CoordinateReferenceSystem):

    def __init__(self, properties=None, **extra):
        super(Linked, self).__init__(properties=properties, **extra)
        self["type"] = "link"


class Default(object):

    """GeoJSON default, long/lat WGS84, is not serialized."""
