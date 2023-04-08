from __future__ import annotations

from typing import Any, Callable, Iterable, Optional, Type, Union, TYPE_CHECKING

import geojson
from geojson.mapping import to_mapping

if TYPE_CHECKING:
    from geojson.types import G, LineLike, PolyLike, ErrorList, CheckErrorFunc


class GeoJSON(dict):
    """
    A class representing a GeoJSON object.
    """

    def __init__(self, iterable: Iterable[Any] = (), **extra) -> None:
        """
        Initializes a GeoJSON object

        :param iterable: iterable from which to draw the content of the GeoJSON
        object.
        :type iterable: dict, array, tuple
        """
        super().__init__(iterable)
        self["type"] = getattr(self, "type", type(self).__name__)
        self.update(extra)

    def __repr__(self) -> str:
        return geojson.dumps(self, sort_keys=True)

    __str__ = __repr__

    def __getattr__(self, name: str) -> Any:
        """
        Permit dictionary items to be retrieved like object attributes

        :param name: attribute name
        :type name: str
        :return: dictionary value
        """
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Permit dictionary items to be set like object attributes.

        :param name: key of item to be set
        :type name: str
        :param value: value to set item to
        """

        self[name] = value

    def __delattr__(self, name: str) -> None:
        """
        Permit dictionary items to be deleted like object attributes

        :param name: key of item to be deleted
        :type name: str
        """

        del self[name]

    @property
    def __geo_interface__(self) -> Optional[G]:
        if self.type == "GeoJSON":
            return None
        else:
            return self

    @classmethod
    def to_instance(
        cls,
        ob: Optional[G],
        default: Union[Type[GeoJSON], Callable[..., G], None] = None,
        strict: bool = False,
    ) -> G:
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
        if ob is None:
            if default is None:
                raise ValueError("At least one argument must be provided")
            else:
                return default()

        if isinstance(ob, GeoJSON):
            return ob

        # If object is not an instance of GeoJSON
        mapping = to_mapping(ob)
        d = {k: v for k, v in mapping.items()}
        error_msg = "Cannot coerce %r into a valid GeoJSON structure: %s"
        try:
            type_ = d.pop("type")
        except KeyError as invalid:
            if strict:
                raise ValueError(error_msg.format(ob, invalid))
            return ob
        try:
            type_ = str(type_)
        except UnicodeEncodeError:
            # If the type contains non-ascii characters, we can assume
            # it's not a valid GeoJSON type
            raise AttributeError(f"{type_} is not a GeoJSON type")
        try:
            geojson_factory: Type[GeoJSON] = getattr(geojson.factory, type_)
            return geojson_factory(**d)
        except (AttributeError, TypeError) as invalid:
            if strict:
                raise ValueError(error_msg.format(ob, invalid))
            return ob

    @property
    def is_valid(self) -> bool:
        return not self.errors()

    def check_list_errors(
        self,
        checkFunc: CheckErrorFunc,
        lst: Union[LineLike, PolyLike],
    ) -> ErrorList:
        """Validation helper function."""
        # Check for errors on each subitem, filter only subitems with errors
        results = (checkFunc(i) for i in lst)
        return [err for err in results if err]

    def errors(self) -> Any:
        """Return validation errors (if any).
        Implement in each subclass.
        """

        # Make sure that each subclass implements it's own validation function
        if self.__class__ != GeoJSON:
            raise NotImplementedError(self.__class__)
