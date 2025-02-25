from geojson.base import GeoJSON

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List, Literal, Optional, Union, Dict, Any
    from .geometry import Geometry

class Feature(GeoJSON):
    """
    Represents a WGS84 GIS feature.
    """
    # https://datatracker.ietf.org/doc/html/rfc7946#section-3.2
    type: Literal["Feature"]
    geometry: Optional[Geometry]
    properties: Dict[str, Any]
    id: Optional[Union[int, str]]

    def __init__(self, id=None, geometry=None, properties=None, **extra):
        """
        Initialises a Feature object with the given parameters.

        :param id: Feature identifier, such as a sequential number.
        :type id: str, int
        :param geometry: Geometry corresponding to the feature.
        :param properties: Dict containing properties of the feature.
        :type properties: dict
        :return: Feature object
        :rtype: Feature
        """
        super().__init__(**extra)
        if id is not None:
            self["id"] = id
        self["geometry"] = (self.to_instance(geometry, strict=True)
                            if geometry else None)
        self["properties"] = properties or {}

    def errors(self):
        geo = self.get('geometry')
        return geo.errors() if geo else None


class FeatureCollection(GeoJSON):
    """
    Represents a FeatureCollection, a set of multiple Feature objects.
    """
    features: List[Feature]

    def __init__(self, features, **extra):
        """
        Initialises a FeatureCollection object from the
        :param features: List of features to constitute the FeatureCollection.
        :type features: list
        :return: FeatureCollection object
        :rtype: FeatureCollection
        """
        super().__init__(**extra)
        self["features"] = features

    def errors(self):
        return self.check_list_errors(lambda x: x.errors(), self.features)

    def __getitem__(self, key):
        try:
            return self.get("features", ())[key]
        except (KeyError, TypeError, IndexError):
            return super(GeoJSON, self).__getitem__(key)
