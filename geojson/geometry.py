import sys
from decimal import Decimal

from geojson.base import GeoJSON


if sys.version_info[0] == 3:
    # Python 3.x has no long type
    _JSON_compliant_types = (float, int, Decimal)
else:
    _JSON_compliant_types = (float, int, Decimal, long)  # noqa


class Geometry(GeoJSON):
    """
    Represents an abstract base class for a WGS84 geometry.
    """

    def __init__(self, coordinates=None, crs=None, validate=False, **extra):
        """
        Initialises a Geometry object.

        :param coordinates: Coordinates of the Geometry object.
        :type coordinates: tuple or list of tuple
        :param crs: CRS
        :type crs: CRS object
        """

        super(Geometry, self).__init__(**extra)
        self["coordinates"] = self.clean_coordinates(coordinates or [])

        if validate:
            errors = self.errors()
            if errors:
                raise ValueError('{}: {}'.format(errors, coordinates))
        if crs:
            self["crs"] = self.to_instance(crs, strict=True)

    @classmethod
    def clean_coordinates(cls, coords):
        if isinstance(coords, cls):
            return coords['coordinates']

        new_coords = []
        if isinstance(coords, Geometry):
            coords = [coords]
        for coord in coords:
            if isinstance(coord, (list, tuple)):
                new_coords.append(cls.clean_coordinates(coord))
            elif isinstance(coord, Geometry):
                new_coords.append(coord['coordinates'])
            elif isinstance(coord, _JSON_compliant_types):
                new_coords.append(coord)
            else:
                raise ValueError("%r is not a JSON compliant number" % coord)
        return new_coords


class GeometryCollection(GeoJSON):
    """
    Represents an abstract base class for collections of WGS84 geometries.
    """

    def __init__(self, geometries=None, **extra):
        super(GeometryCollection, self).__init__(**extra)
        self["geometries"] = geometries or []

    def errors(self):
        errors = [geom.errors() for geom in self['geometries']]
        return [err for err in errors if err]

    def __getitem__(self, key):
        try:
            return self.get("geometries", ())[key]
        except (KeyError, TypeError, IndexError):
            return super(GeoJSON, self).__getitem__(key)


# Marker classes.

def check_point(coord):
    if not isinstance(coord, list):
        return 'each position must be a list'
    if len(coord) not in (2, 3):
        return 'a position must have exactly 2 or 3 values'


class Point(Geometry):
    def errors(self):
        return check_point(self['coordinates'])


class MultiPoint(Geometry):
    def errors(self):
        return self.check_list_errors(check_point, self['coordinates'])


def check_line_string(coord):
    if not isinstance(coord, list):
        return 'each line must be a list of positions'
    if len(coord) < 2:
        return ('the "coordinates" member must be an array of '
                'two or more positions')
    for pos in coord:
        error = check_point(pos)
        if error:
            return error


class LineString(MultiPoint):
    def errors(self):
        return check_line_string(self['coordinates'])


class MultiLineString(Geometry):
    def errors(self):
        return self.check_list_errors(check_line_string, self['coordinates'])


def check_polygon(coord):
    if not isinstance(coord, list):
        return 'Each polygon must be a list of linear rings'

    if not all(isinstance(elem, list) for elem in coord):
        return "Each element of a polygon's coordinates must be a list"

    lengths = all(len(elem) >= 4 for elem in coord)
    if lengths is False:
        return 'Each linear ring must contain at least 4 positions'

    isring = all(elem[0] == elem[-1] for elem in coord)
    if isring is False:
        return 'Each linear ring must end where it started'


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
