import sys
import geojson

try:
    import simplejson as json
except ImportError:
    import json
from collections import MutableMapping
is_mapping = lambda obj: isinstance(obj, MutableMapping)
mapping_base = MutableMapping


GEO_INTERFACE_MARKER = "__geo_interface__"


def to_mapping(obj):
    mapping = getattr(obj, GEO_INTERFACE_MARKER, None)
    if mapping is None:
        if is_mapping(obj):
            mapping = obj
        else:
            if isinstance(obj, geojson.GeoJSON):
                mapping = dict(obj)
            else:
                mapping = json.loads(json.dumps(obj))
    return mapping
