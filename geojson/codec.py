import json

import geojson
import geojson.factory
from geojson.mapping import to_mapping


class GeoJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        return geojson.factory.GeoJSON.to_instance(obj) # NOQA


# Wrap the functions from json, providing encoder, decoders, and
# object creation hooks.
# Here the defaults are set to only permit valid JSON as per RFC 4267

def _enforce_strict_numbers(obj):
    raise ValueError(f"Number {obj!r} is not JSON compliant")


def dump(obj, fp, cls=GeoJSONEncoder, allow_nan=False, **kwargs):
    return json.dump(to_mapping(obj),
                     fp, cls=cls, allow_nan=allow_nan, **kwargs)


def dumps(obj, cls=GeoJSONEncoder, allow_nan=False, ensure_ascii=False, **kwargs):
    return json.dumps(to_mapping(obj),
                      cls=cls, allow_nan=allow_nan, ensure_ascii=ensure_ascii, **kwargs)


_default_object_hook = geojson.base.GeoJSON.to_instance


def _decode_geojson(obj):
    result = [obj]
    # Convert children before their parents without Python recursion.
    stack = [(None, None, result, iter(enumerate(result)), False)]
    while stack:
        parent, parent_key, container, children, is_feature = stack[-1]
        try:
            key, value = next(children)
        except StopIteration:
            stack.pop()
            if isinstance(container, dict):
                parent[parent_key] = _default_object_hook(container)
            continue
        if is_feature and key == "properties":
            continue
        if isinstance(value, list):
            value = list(value)
            container[key] = value
            stack.append((container, key, value, iter(enumerate(value)),
                          False))
        elif isinstance(value, dict):
            stack.append((container, key, value, iter(value.items()),
                          value.get("type") == "Feature"))
    return result[0]


def load(fp,
         cls=json.JSONDecoder,
         parse_constant=_enforce_strict_numbers,
         object_hook=_default_object_hook,
         **kwargs):
    return loads(fp.read(), cls=cls, object_hook=object_hook,
                 parse_constant=parse_constant, **kwargs)


def loads(s,
          cls=json.JSONDecoder,
          parse_constant=_enforce_strict_numbers,
          object_hook=_default_object_hook,
          **kwargs):
    if (
        (cls is None or cls is json.JSONDecoder)
        and object_hook == _default_object_hook
        and kwargs.get("object_pairs_hook") is None
    ):
        obj = json.loads(s, cls=cls, parse_constant=parse_constant, **kwargs)
        return _decode_geojson(obj)
    return json.loads(s,
                      cls=cls, object_hook=object_hook,
                      parse_constant=parse_constant,
                      **kwargs)


# Backwards compatibility
PyGFPEncoder = GeoJSONEncoder
