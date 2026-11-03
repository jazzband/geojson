from geojson.base import GeoJSON
from geojson.mapping import extract_dict


class Feature(GeoJSON):
    """
    Represents a WGS84 GIS feature.
    """

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
        d, id = extract_dict(id)
        if d is not None:
            super().__init__(d, **extra)
            if "geometry" in self and self["geometry"]:
                self["geometry"] = (
                    self.to_instance(self["geometry"], strict=True)
                    if not isinstance(self["geometry"], GeoJSON)
                    else self["geometry"]
                )
            if "properties" not in self:
                self["properties"] = {}
            return

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

    def __init__(self, features=None, **extra):
        """
        Initialises a FeatureCollection object from the
        :param features: List of features to constitute the FeatureCollection.
        :type features: list
        :return: FeatureCollection object
        :rtype: FeatureCollection
        """
        d, features = extract_dict(features)
        if d is not None:
            super().__init__(d, **extra)
            self["features"] = [
                self.to_instance(f) if not isinstance(f, GeoJSON) else f
                for f in self.get("features", [])
            ]
            return

        super().__init__(**extra)
        self["features"] = [
            self.to_instance(f) if not isinstance(f, GeoJSON) else f
            for f in (features or [])
        ]

    def errors(self):
        return self.check_list_errors(lambda x: x.errors(), self.features)

    def __getitem__(self, key):
        try:
            return self.get("features", ())[key]
        except (KeyError, TypeError, IndexError):
            return super(GeoJSON, self).__getitem__(key)
