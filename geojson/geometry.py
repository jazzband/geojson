
from geojson.base import GeoJSON
import geojson.crs 


class Geometry(GeoJSON):

    """A (WGS84) GIS geometry."""

    def __init__(self, coordinates=(), crs=None, decimal_precision=7, **extra):
        super(Geometry, self).__init__(**extra)
        self._decimal_precision = decimal_precision
        self.coordinates = coordinates
        self.crs = GeoJSON.from_value(crs, geojson.crs, default=lambda:None)
        #self.check(self.coordinates)

    def check(self, coordinates):
        pass

    @property
    def __geo_interface__(self):
        d = super(Geometry, self).__geo_interface__
        d.update(coordinates=self.coordinates)
        if self.crs:
            crs = self.crs.__geo_interface__
            d.update(crs=crs)
        return d

        
class Point(Geometry):

    @classmethod
    def check(cls, coordinates):
        if len(coordinates) != 2:
            msg = "Geometry of type %r must be 2 dimensional" % coordinates
            raise ValueError(msg)

        
class MultiPoint(Geometry): 

    @classmethod
    def check(cls, coordinates):
        for point in coordinates:
            Point.check(point)


class LineString(MultiPoint):  pass


class MultiLineString(Geometry): 

    @classmethod
    def check(cls, coordinates):
        for linestring in coordinates:
            LineString.check(linestring)


class Polygon(Geometry): 

    @classmethod
    def check(cls, coordinates):
        # check it's a ring
        (first, last) = (coordinates[0], coordinates[-1])
        if round(last - first, self._decimal_precision) == 0:
            raise ValueError("Invalid Polygon, must form a ring.")
        MultiPoint.check(coordinates)


class MultiPolygon(Geometry): 

    @classmethod
    def check(cls, coordinates):
        for polygon in coordinates:
            Polygon.check(polygon)


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

        
