from __future__ import unicode_literals

import geojson
from geojson.mapping import to_mapping


class GeoJSON(dict):
    """
    A class representing a GeoJSON object.
    """

    def __init__(self, iterable=(), **extra):
        """
        Initialises a GeoJSON object

        :param iterable: iterable from which to draw the content of the GeoJSON
        object.
        :type iterable: dict, array, tuple
        :return: a GeoJSON object
        :rtype: GeoJSON
        """
        super(GeoJSON, self).__init__(iterable)
        self["type"] = getattr(self, "type", type(self).__name__)
        self.update(extra)

    def __repr__(self):
        return geojson.dumps(self, sort_keys=True)

    __str__ = __repr__

    def __getattr__(self, name):
        """
        Permit dictionary items to be retrieved like object attributes

        :param name: attribute name
        :type name: str, int
        :return: dictionary value
        """
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        """
        Permit dictionary items to be set like object attributes.

        :param name: key of item to be set
        :type name: str
        :param value: value to set item to
        """

        self[name] = value

    def __delattr__(self, name):
        """
        Permit dictionary items to be deleted like object attributes

        :param name: key of item to be deleted
        :type name: str
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

        :param cls: Dict containing the elements to be encoded into a GeoJSON
        object.
        :type cls: dict
        :param ob: GeoJSON object into which to encode the dict provided in
        `cls`.
        :type ob: GeoJSON
        :param default: A default instance to append the content of the dict
        to if none is provided.
        :type default: GeoJSON
        :param strict: Raise error if unable to coerce particular keys or
        attributes to a valid GeoJSON structure.
        :type strict: bool
        :return: A GeoJSON object with the dict's elements as its constituents.
        :rtype: GeoJSON
        :raises TypeError: If the input dict contains items that are not valid
        GeoJSON types.
        :raises UnicodeEncodeError: If the input dict contains items of a type
        that contain non-ASCII characters.
        :raises AttributeError: If the input dict contains items that are not
        valid GeoJSON types.
        """
        if ob is None and default is not None:
            instance = default()
        elif isinstance(ob, GeoJSON):
            instance = ob
        else:
            mapping = to_mapping(ob)
            d = {}
            for k in mapping:
                d[k] = mapping[k]
            try:
                type_ = d.pop("type")
                try:
                    type_ = str(type_)
                except UnicodeEncodeError:
                    # If the type contains non-ascii characters, we can assume
                    # it's not a valid GeoJSON type
                    raise AttributeError(
                        "{0} is not a GeoJSON type").format(type_)
                geojson_factory = getattr(geojson.factory, type_)
                if not issubclass(geojson_factory, GeoJSON):
                    raise TypeError("""\
                    Not a valid GeoJSON type:
                    %r (geojson_factory: %r, cls: %r)
                    """ % (type_, geojson_factory, cls))
                instance = geojson_factory(**d)
            except (AttributeError, KeyError) as invalid:
                if strict:
                    msg = "Cannot coerce %r into a valid GeoJSON structure: %s"
                    msg %= (ob, invalid)
                    raise ValueError(msg)
                instance = ob
        return instance

    @property
    def is_valid(self):
        return not self.errors()

    def check_list_errors(self, checkFunc, lst):
        """Validation helper function."""
        # check for errors on each subitem, filter only subitems with errors
        results = (checkFunc(i) for i in lst)
        return [err for err in results if err]

    def errors(self):
        """Return validation errors (if any).
        Implement in each subclass.
        """

        # make sure that each subclass implements it's own validation function
        if self.__class__ != GeoJSON:
            raise NotImplementedError(self.__class__)

        # check for errors on own dict (self)
        results = {key: obj.errors() for (key, obj) in self.iteritems()}
        return {key: err for (key, err) in results.iteritems() if err}
