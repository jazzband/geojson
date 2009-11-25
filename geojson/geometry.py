from geojson.base import GeoJSON


class Geometry(GeoJSON):

    """A (WGS84) GIS geometry."""

    def __init__(self, coordinates=None, crs=None, **extra):
        super(Geometry, self).__init__(**extra)
        self["coordinates"] = coordinates or []
        if crs:
            self["crs"] = self.to_instance(crs, strict=True)


class GeometryCollection(GeoJSON):

    """A collection of (WGS84) GIS geometries."""

    def __init__(self, geometries=None, **extra):
        super(GeometryCollection, self).__init__(**extra)
        self["geometries"] = geometries or []
            

# Marker classes.

class Point(Geometry): pass


class MultiPoint(Geometry): pass


class LineString(MultiPoint):  pass
    
    
class MultiLineString(Geometry): pass 


class Polygon(Geometry): pass


class MultiPolygon(Geometry): pass


class Default(object): 

    """GeoJSON default.""" 
