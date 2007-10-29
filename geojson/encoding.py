# ============================================================================
# GeoJSON. Copyright (C) 2007 Sean C. Gillies
#
# See ../LICENSE.txt
# 
# Contact: Sean Gillies, sgillies@frii.com
# ============================================================================

import operator

import simplejson

from geojson.base import GeoJSON
from geojson import geometry
from geojson import feature 


GEO_INTERFACE_MARKER = "__geo_interface__"
_geojson_factories = dict(Point=geometry.Point, 
                          MultiPoint=geometry.MultiPoint, 
                          LineString=geometry.LineString, 
                          MultiLineString=geometry.MultiLineString,
                          Polygon=geometry.Polygon, 
                          MultiPolygon=geometry.MultiPolygon,
                          GeometryCollection=geometry.GeometryCollection,
                          Feature=feature.Feature, 
                          FeatureCollection=feature.FeatureCollection)
                  

def is_mapping(ob):
    #mapping_attrs = ("__getitem__", "__iter__", "__len__", "keys")
    #ag = operator.attrgetter(*mapping_attrs)
    #try: 
    #    ag(ob)
    #except AttributeError:
    #    return False
    if not hasattr(ob, '__getitem__'):
        return False
    return True


def to_mapping(ob):
    if hasattr(ob, GEO_INTERFACE_MARKER):
        candidate = ob.__geo_interface__
    else:
        candidate = ob
    if not is_mapping(candidate):
        msg = "Expecting something that has %r or a mapping, got %r" 
        msg %= (GEO_INTERFACE_MARKER, ob)
        raise ValueError(msg) 
    return Mapping(candidate)


def to_geojson_dict(mapping):
    """Convert a mapping to GeoJSON.

    The resulting value will have GeoJSON's defaults applied.
    """
    d = dict(mapping)
    type_ = d.pop("type", None)
    if type_:
        geojson_factory = _geojson_factories.get(type_, GeoJSON)
        d = geojson_factory(**d).__geo_interface__
    return d


def to_geojson_object(geojson_dict):
    """Encode a GeoJSON dict into an GeoJSON object.

    Assumes the caller knows that the dict should satisfy a GeoJSON type.
    """
    # ensure keys are strings
    d = dict((str(k), geojson_dict[k]) for k in geojson_dict)
    try:
        geojson_factory = _geojson_factories.get(d.pop("type"))
        return geojson_factory(**d)
    except KeyError:
        raise ValueError("dictionary is not valid geojson dictionary")


class Mapping(object):
    
    """Define what a ``mapping`` is to geojson.

    Until py3k, where we have abstract base classes, this will have to do.
    """

    def __init__(self, ob):
        super(Mapping, self).__init__()
        self._ob = ob

    def __contains__(self, name):
        return bool(self.get(name))

    def __getitem__(self, key):
        return self._ob[key]

    def __iter__(self):
        return iter(self._ob)

    def __len__(self):
        return len(self._ob)

    def keys(self):
        return list(self._ob)

    def get(self, key, default=None):
        try:
            value = self._ob[key]
        except KeyError:
            value = default
        return value

    def update(self, other):
        for key in other:
            if not key in self:
                self[key] = other[key]


class PyGFPEncoder(simplejson.JSONEncoder):

    def default(self, obj):
        return to_geojson_dict(obj)


# Wrap the functions from simplejson, providing encoder, decoders, and
# object creation hooks

def dump(obj, fp, cls=PyGFPEncoder, **kwargs):
    return simplejson.dump(to_mapping(obj), fp, cls=cls, **kwargs)


def dumps(obj, cls=PyGFPEncoder, **kwargs):
    return simplejson.dumps(to_mapping(obj), cls=cls, **kwargs)


def load(fp, cls=simplejson.JSONDecoder, object_hook=None, **kwargs):
    return simplejson.load(fp, cls=cls, object_hook=object_hook, **kwargs)


def loads(s, cls=simplejson.JSONDecoder, object_hook=None, **kwargs):
    return simplejson.loads(s, cls=cls, object_hook=object_hook, **kwargs)

