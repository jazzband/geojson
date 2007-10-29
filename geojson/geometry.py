
from geojson.base import GeoJSON


class Geometry(GeoJSON):

    """A (WGS84) GIS geometry."""

    def __init__(self, coordinates=(), decimal_precision=7, **extra):
        super(Geometry, self).__init__(**extra)
        self._decimal_precision = decimal_precision
        self.coordinates = coordinates
        check = getattr(self, "check_%s" % self.type.lower())
        check(self.coordinates)

    def check_point(self, point):
        if len(point) != 2:
            raise ValueError("Geometry of type %r must be 2 dimensional" % self.type)

    def _check_point_seq(self, point_seq):
        for point in point_seq:
            self.check_point(point)

    def check_multipoint(self, multipoint):
        self._check_point_seq(multipoint)
        
    def check_linestring(self, linestring):
        self._check_point_seq(linestring)

    def check_multilinestring(self, multilinestring):
        for linestring in multilinestring:
            self.check_linestring(linestring)

    def check_polygon(self, polygon):
        # check it's a ring
        (first, last) = (polygon[0], polygon[-1])
        if round(last - first, self._decimal_precision) == 0:
            raise ValueError("Invalid Polygon, must form a ring.")
        self._check_point_seq(polygon)
        
    def check_multipolygon(self, multipolygon):
        for polygon in multipolygon:
            self.check_polygon(polygon)
            
    @property
    def __geo_interface__(self):
        d = super(Geometry, self).__geo_interface__
        d.update(coordinates=self.coordinates)
        return d


class Point(Geometry): pass


class MultiPoint(Geometry): pass


class LineString(Geometry): pass


class MultiLineString(Geometry): pass


class Polygon(Geometry): pass


class MultiPolygon(Geometry): pass


class GeometryCollection(GeoJSON):

    """A collection of (WGS84) GIS geometries."""

    def __init__(self, geometries, **extra):
        super(GeometryCollection, self).__init__(**extra)
        self.geometries = geometries

    @property
    def __geo_interface__(self):
        d = super(GeometryCollection, self).__geo_interface__
        geometries = list(g.__geo_interface__ for g in self.geometries)
        d.update(geometries=geometries)
        return d

        
