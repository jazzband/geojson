import sys
from decimal import Decimal

from geojson.base import GeoJSON


class Geometry(GeoJSON):
    """
    Represents an abstract base class for a WGS84 geometry.
    """

    if sys.version_info[0] == 3:
        # Python 3.x has no long type
        __JSON_compliant_types = (float, int, Decimal)
    else:
        __JSON_compliant_types = (float, int, Decimal, long)  # noqa

    def __init__(self, coordinates=None, crs=None, validate=False, **extra):
        """
        Initialises a Geometry object.

        :param coordinates: Coordinates of the Geometry object.
        :type coordinates: tuple
        :param crs: CRS
        :type crs: CRS object
        """

        super(Geometry, self).__init__(**extra)
        self["coordinates"] = coordinates or []
        self.clean_coordinates(self["coordinates"])
        if validate:
            errors = self.errors()
            if errors:
                raise ValueError('{}: {}'.format(errors, coordinates))
        if crs:
            self["crs"] = self.to_instance(crs, strict=True)

    @classmethod
    def clean_coordinates(cls, coords):
        for coord in coords:
            if isinstance(coord, (list, tuple)):
                cls.clean_coordinates(coord)
            elif not isinstance(coord, cls.__JSON_compliant_types):
                raise ValueError("%r is not JSON compliant number" % coord)


class GeometryCollection(GeoJSON):
    """
    Represents an abstract base class for collections of WGS84 geometries.
    """

    def __init__(self, geometries=None, **extra):
        super(GeometryCollection, self).__init__(**extra)
        self["geometries"] = geometries or []


# Marker classes.

def check_point(coord):
    if len(coord) not in (2, 3):
        return 'the "coordinates" member must be a single position'


class Point(Geometry):
    def errors(self):
        return check_point(self['coordinates'])


class MultiPoint(Geometry):
    def errors(self):
        return self.check_list_errors(check_point, self['coordinates'])


def check_line_string(coord):
    if len(coord) < 2:
        return ('the "coordinates" member must be an array of '
                'two or more positions')


class LineString(MultiPoint):
    def errors(self):
        return check_line_string(self['coordinates'])


class MultiLineString(Geometry):
    def errors(self):
        return self.check_list_errors(check_line_string, self['coordinates'])


def check_polygon(coord):
    lengths = all(len(elem) >= 4 for elem in coord)
    if lengths is False:
        return 'LinearRing must contain with 4 or more positions'

    isring = all(elem[0] == elem[-1] for elem in coord)
    if isring is False:
        return 'The first and last positions in LinearRing must be equivalent'


class Polygon(Geometry):
    def errors(self):
        return check_polygon(self['coordinates'])


class MultiPolygon(Geometry):
    def errors(self):
        return self.check_list_errors(check_polygon, self['coordinates'])


class Default(object):
    """
    GeoJSON default object.
    """
