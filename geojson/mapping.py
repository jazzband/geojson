import sys
import geojson

if sys.version_info[:2] >= (2, 6):
    import json
    from collections import MutableMapping
    is_mapping = lambda obj: isinstance(obj, MutableMapping)
    mapping_base = MutableMapping
else:
    import simplejson as json
    mapping_base = object
    def is_mapping(ob):
        return hasattr(ob, "__getitem__")


GEO_INTERFACE_MARKER = "__geo_interface__"


def to_mapping(obj):
    mapping = getattr(obj, GEO_INTERFACE_MARKER, None)
    if mapping is None:
        if is_mapping(obj):
            mapping = obj
        else:
            if isinstance(obj, geojson.GeoJSON) :
                mapping = dict(obj)
            else:
                mapping = json.loads(json.dumps(obj))
    return mapping
    
