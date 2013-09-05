
class SimpleWebFeature(object):

    """
    A simple, Atom-ish, single geometry (WGS84) GIS feature.
    """

    def __init__(self, id=None, geometry=None, title=None, summary=None,
                 link=None):
        """Initialize."""
        self.id = id
        self.geometry = geometry
        self.properties = {}
        self.properties['title'] = title
        self.properties['summary'] = summary
        self.properties['link'] = link

    def as_dict(self):
        return {
            "type": "Feature",
            "id": self.id,
            "properties": self.properties,
            "geometry": self.geometry
            }

    __geo_interface__ = property(as_dict)


def createSimpleWebFeature(o):
    """Create an instance of SimpleWebFeature from a dict, o. If o does not
    match a Python feature object, simply return o. This function serves as a
    json decoder hook. See coding.load()."""
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
