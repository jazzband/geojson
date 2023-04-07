from __future__ import annotations

try:
    import simplejson as json
except ImportError:
    import json

from typing import TYPE_CHECKING, IO, Any, Callable, Type

import geojson.factory
from geojson.mapping import to_mapping

if TYPE_CHECKING:
    from geojson.types import G


class GeoJSONEncoder(json.JSONEncoder):
    def default(self, obj: G) -> G:
        return geojson.factory.GeoJSON.to_instance(obj) # NOQA


# Wrap the functions from json, providing encoder, decoders, and
# object creation hooks.
# Here the defaults are set to only permit valid JSON as per RFC 4267

def _enforce_strict_numbers(obj: str) -> None:
    raise ValueError("Number %r is not JSON compliant" % obj)


def dump(
    obj: G,
    fp: IO[str],
    cls: Type[json.JSONEncoder] = GeoJSONEncoder,
    allow_nan: bool = False,
    **kwargs
) -> None:
    return json.dump(to_mapping(obj),
                     fp, cls=cls, allow_nan=allow_nan, **kwargs)


def dumps(
    obj: G,
    cls: Type[json.JSONEncoder] = GeoJSONEncoder,
    allow_nan: bool = False,
    ensure_ascii: bool = False,
    **kwargs
) -> str:
    return json.dumps(
        to_mapping(obj),
        cls=cls,
        allow_nan=allow_nan,
        ensure_ascii=ensure_ascii,
        **kwargs
    )


def load(fp: IO[str],
         cls: Type[json.JSONDecoder] = json.JSONDecoder,
         parse_constant: Callable[[str], None] = _enforce_strict_numbers,
         object_hook: Callable[..., G] = geojson.factory.GeoJSON.to_instance,
         **kwargs) -> Any:
    return json.load(fp,
                     cls=cls, object_hook=object_hook,
                     parse_constant=parse_constant,
                     **kwargs)


def loads(s: str,
          cls: Type[json.JSONDecoder] = json.JSONDecoder,
          parse_constant: Callable[[str], None] = _enforce_strict_numbers,
          object_hook: Callable[..., G] = geojson.factory.GeoJSON.to_instance,
          **kwargs) -> Any:
    return json.loads(s,
                      cls=cls, object_hook=object_hook,
                      parse_constant=parse_constant,
                      **kwargs)


# Backwards compatibility
PyGFPEncoder = GeoJSONEncoder
