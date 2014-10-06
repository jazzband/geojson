from geojson.geometry import Point, LineString, Polygon
from geojson.geometry import MultiLineString, MultiPoint, MultiPolygon
from geojson.geometry import GeometryCollection
from geojson.feature import Feature, FeatureCollection
from geojson.base import GeoJSON
from geojson.crs import Named, Linked

__all__ = ([Point, LineString, Polygon] +
           [MultiLineString, MultiPoint, MultiPolygon] +
           [GeometryCollection] +
           [Feature, FeatureCollection] +
           [GeoJSON])

name = Named
link = Linked
