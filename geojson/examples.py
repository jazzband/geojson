from __future__ import annotations

from typing import TYPE_CHECKING, Any, MutableMapping, Optional, Union

if TYPE_CHECKING:
    from geojson.geometry import Geometry
    from geojson.types import G


class SimpleWebFeature:

    """
    A simple, Atom-ish, single geometry (WGS84) GIS feature.
    """

    def __init__(
        self,
        id: Optional[Any] = None,
        geometry: Union[Geometry, MutableMapping, None] = None,
        title: Optional[str] = None,
        summary: Optional[str] = None,
        link: Optional[str] = None,
    ) -> None:
        """
        Initialises a SimpleWebFeature from the parameters provided.

        :param id: Identifier assigned to the object.
        :type id: int, str
        :param geometry: The geometry on which the object is based.
        :type geometry: Geometry
        :param title: Name of the object
        :type title: str
        :param summary: Short summary associated with the object.
        :type summary: str
        :param link: Link associated with the object.
        :type link: str
        """
        self.id = id
        self.geometry = geometry
        self.properties = {'title': title, 'summary': summary, 'link': link}

    def as_dict(self) -> dict[str, Any]:
        return {
            "type": "Feature",
            "id": self.id,
            "properties": self.properties,
            "geometry": self.geometry
            }

    __geo_interface__ = property(as_dict)

    """
    Create an instance of SimpleWebFeature from a dict, o. If o does not
    match a Python feature object, simply return o. This function serves as a
    json decoder hook. See coding.load().
    """


def create_simple_web_feature(o: G) -> Union[SimpleWebFeature, G]:
    """
    Create an instance of SimpleWebFeature from a dict, o. If o does not
    match a Python feature object, simply return o. This function serves as a
    json decoder hook. See coding.load().

    :param o: A dict to create the SimpleWebFeature from.
    :type o: dict
    :return: A SimpleWebFeature from the dict provided.
    :rtype: SimpleWebFeature
    """
    try:
        id = o['id']
        g = o['geometry']
        p = o['properties']
        return SimpleWebFeature(str(id), {
            'type': str(g.get('type')),
            'coordinates': g.get('coordinates', [])},
            title=p.get('title'),
            summary=p.get('summary'),
            link=str(p.get('link')))
    except (KeyError, TypeError):
        pass
    return o
