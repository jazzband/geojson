from geojson.base import GeoJSON
import geojson.crs 


class Geometry(GeoJSON):

    """A (WGS84) GIS geometry."""

    def __init__(self, coordinates=None, crs=None, **extra):
        super(Geometry, self).__init__(**extra)
        self.coordinates = coordinates or []
        self.crs = self.to_instance(crs, default=geojson.crs.Default, strict=True)
                    
    @property
    def __geo_interface__(self):
        d = super(Geometry, self).__geo_interface__
        crs = getattr(self.crs, '__geo_interface__', None)
        d.update(coordinates=self.coordinates) 
        if crs is not None:
            d.update(crs=crs)
        return d


class GeometryCollection(GeoJSON):

    """A collection of (WGS84) GIS geometries."""

    def __init__(self, geometries=None, **extra):
        super(GeometryCollection, self).__init__(**extra)
        self.geometries = geometries or []
            
    @property
    def __geo_interface__(self):
        d = super(GeometryCollection, self).__geo_interface__
        geometries = list(self.to_instance(geom, strict=True)
                          for geom in self.geometries)
        d.update(geometries=geometries)
        return d


# Marker classes.

class Point(Geometry): pass


class MultiPoint(Geometry): pass


class LineString(MultiPoint):  pass
    
    
class MultiLineString(Geometry): pass 


class Polygon(Geometry): pass


class MultiPolygon(Geometry): pass


class Default(object): 
    """GeoJSON default.""" 
    pass