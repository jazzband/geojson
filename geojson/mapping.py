from collections import MutableMapping
try:
    import simplejson as json
except ImportError:
    import json

import geojson


mapping_base = MutableMapping


GEO_INTERFACE_MARKER = "__geo_interface__"


def is_mapping(obj):
    return isinstance(obj, MutableMapping)


def to_mapping(obj):
    mapping = getattr(obj, GEO_INTERFACE_MARKER, None)
    if mapping is None:
        if is_mapping(obj):
            mapping = obj
        elif isinstance(obj, geojson.GeoJSON):
            mapping = dict(obj)
        else:
            mapping = json.loads(json.dumps(obj))
    return mapping
