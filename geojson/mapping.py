from collections.abc import Iterable, MutableMapping
import itertools

try:
    import simplejson as json
except ImportError:
    import json

import geojson


GEO_INTERFACE_MARKER = "__geo_interface__"


def is_mapping(obj):
    """
    Checks if the object is an instance of MutableMapping.

    :param obj: Object to be checked.
    :return: Truth value of whether the object is an instance of
    MutableMapping.
    :rtype: bool
    """
    return isinstance(obj, MutableMapping)


def extract_dict(arg):
    """
    If arg represents a dictionary initialization sequence (mapping or iterable
    of key-value pairs where keys match GeoJSON schema attributes, as produced
    by dict constructors or dataclasses.asdict), returns (dict, None).
    Otherwise returns (None, reconstructed_arg).
    """
    if isinstance(arg, geojson.GeoJSON):
        return None, arg
    if isinstance(arg, dict):
        return arg, None
    if isinstance(arg, (tuple, list)):
        if len(arg) > 0:
            first = arg[0]
            if (
                isinstance(first, (tuple, list))
                and len(first) == 2
                and isinstance(first[0], str)
                and not isinstance(first, geojson.GeoJSON)
                and not isinstance(first, dict)
                and first[0] in (
                    'type', 'coordinates', 'features', 'geometry',
                    'properties', 'geometries', 'id'
                )
            ):
                return dict(arg), None
        return None, arg
    if isinstance(arg, Iterable) and not isinstance(arg, (str, bytes)):
        it = iter(arg)
        try:
            first = next(it)
        except StopIteration:
            return None, []
        if (
            isinstance(first, (tuple, list))
            and len(first) == 2
            and isinstance(first[0], str)
            and not isinstance(first, geojson.GeoJSON)
            and not isinstance(first, dict)
            and first[0] in (
                'type', 'coordinates', 'features', 'geometry',
                'properties', 'geometries', 'id'
            )
        ):
            return dict(itertools.chain([first], it)), None
        return None, list(itertools.chain([first], it))
    return None, arg


def to_mapping(obj):

    mapping = getattr(obj, GEO_INTERFACE_MARKER, None)

    if mapping is not None:
        return mapping

    if is_mapping(obj):
        return obj

    if isinstance(obj, geojson.GeoJSON):
        return dict(obj)

    return json.loads(json.dumps(obj))
