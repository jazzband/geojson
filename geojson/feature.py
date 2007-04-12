# ============================================================================
# GeoJSON. Copyright (C) 2007 Sean C. Gillies
#
# See ../LICENSE.txt
# 
# Contact: Sean Gillies, sgillies@frii.com
# ============================================================================

"""
SimpleWebFeature is a working example of a class that satisfies the Python GIS
feature protocol.
"""
   
class PropertyCollection(dict):
    
    """
    A Collection of feature properties.
    """
    
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value


class SimpleWebFeature(object):

    """
    A simple, Atom-ish, single geometry (WGS84) GIS feature. 
    """

    def __init__(self, id=None, geometry=None, title=None, summary=None, 
                 link=None):
        """Initialize."""
        self.id = id
        self.geometry = geometry
        self.properties = PropertyCollection()
        self.properties['title'] = title
        self.properties['summary'] = summary
        self.properties['link'] = link

    def __getitem__(self, key):
        """To satisfy the Python GIS feature protocol, we need to handle at
        least id, geometry, and properties keys.
        """
        try:
            return getattr(self, key)
        except AttributeError, e:
            raise KeyError, e


def createSimpleWebFeature(o):
    """Create an instance of SimpleWebFeature from a dict, o. If o does not
    match a Python feature object, simply return o. This function serves as a 
    simplejson decoder hook. See coding.load()."""
    try:
        id = o['id']
        g = o['geometry']
        p = o['properties']
        return SimpleWebFeature(str(id), 
            {'type': str(g.get('type', None)),
             'coordinates': g.get('coordinates', [[]])},
            title=p.get('title', None),
            summary=p.get('summary', None),
            link=str(p.get('link', None)))
    except (KeyError, TypeError):
        pass
    return o

