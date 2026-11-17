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
    if isinstance(obj, list):
        return [_decode_geojson(value) for value in obj]
    if isinstance(obj, dict):
        is_feature = obj.get("type") == "Feature"
        for key, value in obj.items():
            if not (is_feature and key == "properties"):
                obj[key] = _decode_geojson(value)
        return _default_object_hook(obj)
    return obj


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
    if object_hook == _default_object_hook and kwargs.get("object_pairs_hook") is None:
        obj = json.loads(s, cls=cls, parse_constant=parse_constant, **kwargs)
        return _decode_geojson(obj)
    return json.loads(s,
                      cls=cls, object_hook=object_hook,
                      parse_constant=parse_constant,
                      **kwargs)


# Backwards compatibility
PyGFPEncoder = GeoJSONEncoder
