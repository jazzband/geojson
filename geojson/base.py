

class GeoJSON(object):

    def __init__(self, **extra):
        super(GeoJSON, self).__init__()
        self.type = type(self).__name__
        self.extra = extra

    def __iter__(self):        
        def iter_geo_interface(ob):
            for (key, value) in ob.__geo_interface__.items():
                if hasattr(value, "__geo_interface__"):
                    key, value = iter_geo_interface(value)
                yield (key, value)

        return iter_geo_interface(self)

    @property
    def __geo_interface__(self):
        d = dict(**self.extra)
        if self.type != "GeoJSON":
            d.update(type=self.type)
        return d

    @classmethod
    def from_value(cls, value, namespace, base=None, default=None):
        if not base:
            base = cls
        if isinstance(value, base):
            return value
        if value:
            type_ = value.pop("type", None)
            if type_:
                candidate = getattr(namespace, type_, None)
                if candidate:
                    if issubclass(candidate, base):
                        d = dict((str(k), value[k]) for k in value)
                        return candidate(**d)
                    else:
                        d["type"] = type_
                        raise ValueError("%r is not a valid geometry type" % candidate)
        if not default:
            default = base
        return default()

