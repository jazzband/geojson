
from geojson.mapping import is_mapping, to_mapping
import geojson
import geojson.factory


class GeoJSON(object):

    def __init__(self, **extra):
        super(GeoJSON, self).__init__()
        self.type = type(self).__name__
        self.extra = extra

    def __repr__(self):
        params = ", ".join("%s=%s" % (key, value) 
                           for (key, value) in self
                           if key != "type")
        return "%s(%s)" % (self.type, params)                           

    def __str__(self):
        return str(self.__geo_interface__)

    def __iter__(self):        
        def iter_geo_interface(ob):
            if not hasattr(ob, "__geo_interface__"):
                return
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
    def to_instance(cls, ob, default=None, strict=False):
        """Encode a GeoJSON dict into an GeoJSON object.
        
        Assumes the caller knows that the dict should satisfy a GeoJSON type.
        """
        if ob is None and default is not None:
            instance = default()
        elif isinstance(ob, GeoJSON):
            instance = ob
        else:
            mapping = to_mapping(ob)
            d = dict((str(k), mapping[k]) for k in mapping)
            try:
                type_ = d.pop("type")
                geojson_factory = getattr(geojson.factory, type_)
                if not issubclass(geojson_factory, GeoJSON):
                    raise TypeError("""\
                    Not a valid GeoJSON type:
                    %r (geojson_factory: %r, cls: %r)
                    """ % (type_, geojson_factory, cls))
                instance = geojson_factory(**d)
            except (AttributeError, KeyError), invalid:
                if not strict:
                    instance = ob
                else:
                    msg = "Cannot coerce %r into a valid GeoJSON structure: %s"
                    msg %= (ob, invalid)
                    raise ValueError(msg)
        return instance


