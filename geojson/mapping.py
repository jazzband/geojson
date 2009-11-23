import sys

GEO_INTERFACE_MARKER = "__geo_interface__"

if sys.version_info[:2] >= (2, 6):
    from collections import Mapping
    is_mapping = lambda obj: isinstance(obj, Mapping)
    mapping_base = Mapping
else:
    mapping_base = object
    def is_mapping(ob):
        return hasattr(ob, "__getitem__")


class GeoJSONMapping(mapping_base):
    
    """Define what a ``mapping`` is to geojson."""

    def __init__(self, ob):
        super(GeoJSONMapping, self).__init__()
        self._ob = ob

    def __contains__(self, name):
        return bool(self.get(name))

    def __getitem__(self, key):
        return self._ob[key]

    def __iter__(self):
        return iter(self._ob)
        
    def __len__(self):
        return len(self._ob)

    def keys(self):
        return list(self._ob)

    def get(self, key, default=None):
        try:
            value = self._ob[key]
        except KeyError:
            value = default
        return value

    def update(self, other):
        for key in other:
            if not key in self:
                self[key] = other[key]


def to_mapping(ob):
    if hasattr(ob, GEO_INTERFACE_MARKER):
        candidate = ob.__geo_interface__
        candidate = to_mapping(candidate)
    else:
        candidate = ob
    if not is_mapping(candidate):
        msg = "Expecting something that has %r or a mapping, got %r" 
        msg %= (GEO_INTERFACE_MARKER, ob)
        raise ValueError(msg) 
    return GeoJSONMapping(candidate)
