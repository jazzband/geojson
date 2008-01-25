
from geojson.base import GeoJSON
import geojson.crs 


class Geometry(GeoJSON):

    """A (WGS84) GIS geometry."""

    def __init__(self, coordinates=(), crs=None, decimal_precision=7, **extra):
        super(Geometry, self).__init__(**extra)
        self._decimal_precision = decimal_precision
        self.coordinates = coordinates
        self.crs = self.to_instance(crs, default=geojson.crs.EPSG, strict=True)
                    
    @property
    def __geo_interface__(self):
        d = super(Geometry, self).__geo_interface__
        crs = self.crs.__geo_interface__
        d.update(coordinates=self.coordinates, crs=crs)
        return d

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
        if self.crs:
            crs = self.crs.__geo_interface__
            d.update(crs=crs)
        return d


# Marker classes.

class Point(Geometry): pass


class MultiPoint(Geometry): pass


class LineString(MultiPoint):  pass
    
    
class MultiLineString(Geometry): pass 


class Polygon(Geometry): pass


class MultiPolygon(Geometry): pass

          
