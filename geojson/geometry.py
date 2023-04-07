from __future__ import annotations

from decimal import Decimal
from numbers import Real
from typing import TYPE_CHECKING, Any, List, Optional

from geojson.base import GeoJSON

if TYPE_CHECKING:
    from geojson.types import (
        CoordsAny,
        PointLike,
        LineLike,
        ErrorList,
        ErrorSingle,
    )


DEFAULT_PRECISION = 6


class Geometry(GeoJSON):
    """
    Represents an abstract base class for a WGS84 geometry.
    """

    def __init__(
        self,
        coordinates: Optional[CoordsAny] = None,
        validate: bool = False,
        precision: Optional[int] = None,
        **extra
    ) -> None:
        """
        Initialises a Geometry object.

        :param coordinates: Coordinates of the Geometry object.
        :type coordinates: tuple or list of tuple
        :param validate: Raise exception if validation errors are present?
        :type validate: boolean
        :param precision: Number of decimal places for lat/lon coords.
        :type precision: integer
        """
        super().__init__(**extra)
        if precision is None:
            precision = DEFAULT_PRECISION
        self["coordinates"] = self.clean_coordinates(
            coordinates or [], precision)

        if validate:
            errors = self.errors()
            if errors:
                raise ValueError(f'{errors}: {coordinates}')

    @classmethod
    def clean_coordinates(cls, coords: CoordsAny, precision: int) -> CoordsAny:
        if isinstance(coords, cls):
            return coords['coordinates']
        new_coords: List[CoordsAny] = []
        if isinstance(coords, Geometry):
            coords = [coords]
        for coord in coords:
            if isinstance(coord, (list, tuple)):
                new_coords.append(cls.clean_coordinates(coord, precision))
            elif isinstance(coord, Geometry):
                new_coords.append(coord['coordinates'])
            elif isinstance(coord, (Real, Decimal)):
                new_coords.append(round(coord, precision))
            else:
                raise ValueError("%r is not a JSON compliant number" % coord)
        return new_coords


class GeometryCollection(GeoJSON):
    """
    Represents an abstract base class for collections of WGS84 geometries.
    """

    def __init__(
        self, geometries: Optional[List[Geometry]] = None, **extra
    ) -> None:
        super().__init__(**extra)
        self["geometries"] = geometries or []

    def errors(self) -> List[str]:
        errors = [geom.errors() for geom in self['geometries']]
        return [err for err in errors if err]

    def __getitem__(self, key: str) -> Any:
        try:
            return self.get("geometries", ())[key]
        except (KeyError, TypeError, IndexError):
            return super(GeoJSON, self).__getitem__(key)


# Marker classes.

def check_point(coord: PointLike) -> ErrorSingle:
    if not isinstance(coord, list):
        return 'each position must be a list'
    if len(coord) not in (2, 3):
        return 'a position must have exactly 2 or 3 values'
    for number in coord:
        if not isinstance(number, (Real, Decimal)):
            return 'a position cannot have inner positions'
    return None


class Point(Geometry):
    def errors(self) -> ErrorSingle:
        return check_point(self['coordinates'])


class MultiPoint(Geometry):
    def errors(self) -> ErrorList:
        return self.check_list_errors(check_point, self['coordinates'])


def check_line_string(coord: LineLike) -> ErrorSingle:
    if not isinstance(coord, list):
        return 'each line must be a list of positions'
    if len(coord) < 2:
        return ('the "coordinates" member must be an array of '
                'two or more positions')
    for pos in coord:
        error = check_point(pos)
        if error:
            return error
    return None


class LineString(MultiPoint):
    def errors(self) -> ErrorList:
        error = check_line_string(self['coordinates'])
        return [error] if error else []


class MultiLineString(Geometry):
    def errors(self) -> ErrorList:
        return self.check_list_errors(check_line_string, self['coordinates'])


def check_polygon(coord: LineLike) -> ErrorSingle:
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

    return None


class Polygon(Geometry):
    def errors(self) -> ErrorSingle:
        return check_polygon(self['coordinates'])


class MultiPolygon(Geometry):
    def errors(self) -> ErrorList:
        return self.check_list_errors(check_polygon, self['coordinates'])


class Default:
    """
    GeoJSON default object.
    """
