"""
SimpleWebFeature is a working example of a class that satisfies the Python geo
interface.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from geojson.base import GeoJSON

if TYPE_CHECKING:
    from geojson.geometry import Geometry
    from geojson.types import ErrorList, ErrorSingle


class Feature(GeoJSON):
    """
    Represents a WGS84 GIS feature.
    """

    def __init__(
        self,
        id: Optional[Any] = None,
        geometry: Optional[Geometry] = None,
        properties: Optional[Dict[str, Any]] = None,
        **extra
    ) -> None:
        """
        Initialises a Feature object with the given parameters.

        :param id: Feature identifier, such as a sequential number.
        :type id: str, int
        :param geometry: Geometry corresponding to the feature.
        :param properties: Dict containing properties of the feature.
        :type properties: dict
        """
        super().__init__(**extra)
        if id is not None:
            self["id"] = id
        self["geometry"] = (self.to_instance(geometry, strict=True)
                            if geometry else None)
        self["properties"] = properties or {}

    def errors(self) -> Union[ErrorSingle, ErrorList]:
        geo: Optional[Geometry] = self.get('geometry')
        return geo.errors() if geo else None


class FeatureCollection(GeoJSON):
    """
    Represents a FeatureCollection, a set of multiple Feature objects.
    """

    def __init__(self, features: List[Feature], **extra) -> None:
        """
        Initialises a FeatureCollection object from the
        :param features: List of features to constitute the FeatureCollection.
        :type features: list
        """
        super().__init__(**extra)
        self["features"] = features

    def errors(self) -> ErrorList:
        return self.check_list_errors(lambda x: x.errors(), self.features)

    def __getitem__(self, key: str) -> Any:
        try:
            return self.get("features", ())[key]
        except (KeyError, TypeError, IndexError):
            return super(GeoJSON, self).__getitem__(key)
