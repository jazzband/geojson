from decimal import Decimal
from geojson.base import GeoJSON


class Geometry(GeoJSON):

    """A (WGS84) GIS geometry."""

    def __init__(self, coordinates=None, crs=None, **extra):
        super(Geometry, self).__init__(**extra)
        self["coordinates"] = coordinates or []
        self.clean_coordinates(self["coordinates"])
        if crs:
            self["crs"] = self.to_instance(crs, strict=True)

    def clean_coordinates(self, coords):
        for coord in coords:
            if isinstance(coord, (list, tuple)):
                self.clean_coordinates(coord)
            else:
                if not isinstance(coord, (float, int, Decimal)):
                    raise ValueError("%r is not JSON compliant number", coord)


class GeometryCollection(GeoJSON):

    """A collection of (WGS84) GIS geometries."""

    def __init__(self, geometries=None, **extra):
        super(GeometryCollection, self).__init__(**extra)
        self["geometries"] = geometries or []


# Marker classes.

class Point(Geometry):
    pass


class MultiPoint(Geometry):
    pass


class LineString(MultiPoint):
    pass


class MultiLineString(Geometry):
    pass


class Polygon(Geometry):
    pass


class MultiPolygon(Geometry):
    pass


class Default(object):
    """GeoJSON default."""
