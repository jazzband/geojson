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

    if mapping is not None:
        return mapping

    if is_mapping(obj):
        return obj

    if isinstance(obj, geojson.GeoJSON):
        return dict(obj)

    return json.loads(json.dumps(obj))
