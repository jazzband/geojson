import geojson
from geojson.mapping import to_mapping


class GeoJSON(dict):

    def __init__(self, iterable=(), **extra):
        super(GeoJSON, self).__init__(iterable)
        self["type"] = getattr(self, "type", type(self).__name__)
        self.update(extra)

    def __repr__(self):
        return geojson.dumps(self, sort_keys=True)

    __str__ = __repr__

    def __setattr__(self, name, value):
        """
        Permit dictionary items to be set like object attributes
        """
        self[name] = value

    def __getattr__(self, name):
        """
        Permit dictionary items to be retrieved like object attributes
        """
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __delattr__(self, name):
        """
        Permit dictionary items to be deleted like object attributes
        """
        del self[name]

    @property
    def __geo_interface__(self):
        if self.type != "GeoJSON":
            return self

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
            d = {}
            for k in mapping:
                try:
                    str_key = str(k)
                except (UnicodeEncodeError):
                    str_key = unicode(k)
                d[str_key] = mapping[k]
            try:
                type_ = d.pop("type")
                try:
                    type_ = str(type_)
                except (UnicodeEncodeError):
                    # If the type contains non-ascii characters, we can assume
                    # it's not a valid GeoJSON type
                    raise AttributeError(
                        unicode("{0} is not a GeoJSON type").format(
                        unicode(type_)))
                geojson_factory = getattr(geojson.factory, type_)
                if not issubclass(geojson_factory, GeoJSON):
                    raise TypeError("""\
                    Not a valid GeoJSON type:
                    %r (geojson_factory: %r, cls: %r)
                    """ % (type_, geojson_factory, cls))
                instance = geojson_factory(**d)
            except (AttributeError, KeyError) as invalid:
                if not strict:
                    instance = ob
                else:
                    msg = "Cannot coerce %r into a valid GeoJSON structure: %s"
                    msg %= (ob, invalid)
                    raise ValueError(msg)
        return instance
