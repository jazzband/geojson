from __future__ import annotations

try:
    import simplejson as json
except ImportError:
    import json

from typing import TYPE_CHECKING, Any, Optional, Union, MutableMapping

if TYPE_CHECKING:
    from geojson.base import GeoJSON
    from geojson.types import G


GEO_INTERFACE_MARKER = "__geo_interface__"


def is_mapping(obj: Any) -> bool:
    """
    Checks if the object is an instance of MutableMapping.
    Exists for backwards compatibility only.

    :param obj: Object to be checked.
    :return: Truth value of whether the object is an instance of
    MutableMapping.
    :rtype: bool
    """
    return isinstance(obj, MutableMapping)


def to_mapping(obj: Union[G, str]) -> G:
    """
    Converts an object to a GeoJSON-like object.

    :param obj: A GeoJSON-like object, or a JSON string.
    :type obj: GeoJSON-like object, str
    :return: A dictionary-like object representing the input GeoJSON.
    :rtype: GeoJSON-like object
    """
    mapping: Optional[GeoJSON] = getattr(obj, GEO_INTERFACE_MARKER, None)

    if mapping is not None:
        return mapping

    if isinstance(obj, MutableMapping):
        return obj

    if isinstance(obj, str):
        return json.loads(obj)

    return json.loads(json.dumps(obj))
