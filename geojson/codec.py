# ============================================================================
# GeoJSON. Copyright (C) 2007 Sean C. Gillies
#
# See ../LICENSE.txt
# 
# Contact: Sean Gillies, sgillies@frii.com
# ============================================================================

import simplejson
import geojson
import geojson.factory
from geojson.mapping import Mapping, to_mapping


class GeoJSONEncoder(simplejson.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Mapping):
            mapping = obj
        else:
            mapping = to_mapping(obj)
        d = dict(mapping)
        type_str = d.pop("type", None)
        if type_str:
            geojson_factory = getattr(geojson.factory, type_str, geojson.factory.GeoJSON)
            d = geojson_factory(**d).__geo_interface__
        return d


# Wrap the functions from simplejson, providing encoder, decoders, and
# object creation hooks

def dump(obj, fp, cls=GeoJSONEncoder, **kwargs):
    return simplejson.dump(to_mapping(obj), fp, cls=cls, **kwargs)


def dumps(obj, cls=GeoJSONEncoder, **kwargs):
    return simplejson.dumps(to_mapping(obj), cls=cls, **kwargs)


def load(fp, cls=simplejson.JSONDecoder, object_hook=None, **kwargs):
    return simplejson.load(fp, cls=cls, object_hook=object_hook, **kwargs)


def loads(s, cls=simplejson.JSONDecoder, object_hook=None, **kwargs):
    return simplejson.loads(s, cls=cls, object_hook=object_hook, **kwargs)

# Backwards compatibility
PyGFPEncoder = GeoJSONEncoder
