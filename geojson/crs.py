

from geojson.base import GeoJSON


class CoordinateReferenceSystem(GeoJSON):

    def __init__(self, properties=None, **extra):
        super(CoordinateReferenceSystem, self).__init__(**extra)
        self.properties = properties if properties else {}

    @property
    def __geo_interface__(self):
        d = super(CoordinateReferenceSystem, self).__geo_interface__
        d.update(properties=self.properties)
        return d


class EPSG(CoordinateReferenceSystem):

    def __init__(self, properties=None, **extra):
        super(EPSG, self).__init__(**extra)
        self.properties = properties if properties else {"code": 4326}
