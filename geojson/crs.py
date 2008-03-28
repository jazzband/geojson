

from geojson.base import GeoJSON


class CoordinateReferenceSystem(GeoJSON):

    def __init__(self, properties=None, **extra):
        super(CoordinateReferenceSystem, self).__init__(**extra)
        self.properties = properties or {}

    @property
    def __geo_interface__(self):
        d = super(CoordinateReferenceSystem, self).__geo_interface__
        d.update(type=self.type, properties=self.properties)
        return d


class Named(CoordinateReferenceSystem):

    def __init__(self, properties=None, **extra):
        super(Named, self).__init__(**extra)
        self.type = 'name'
        self.properties = properties


class Linked(CoordinateReferenceSystem):
    
    def __init__(self, properties=None, **extra):
        super(Linked, self).__init__(**extra)
        self.type = 'link'
        self.properties = properties


class Default(object):
    """GeoJSON default, long/lat WGS84, is not serialized."""
    pass

