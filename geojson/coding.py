# ============================================================================
# GeoJSON. Copyright (C) 2007 Sean C. Gillies
#
# See ../LICENSE.txt
# 
# Contact: Sean Gillies, sgillies@frii.com
# ============================================================================


import simplejson
from geojson.feature import SimpleWebFeature


# Equal access to object attributes or mapping items

class Fly(object):
    
    def __init__(self, ob):
        if hasattr(ob, '__geo_interface__'):
            self._ob = ob.__geo_interface__
        else:
            self._ob = ob

    def get(self, attr, default=None):
        try:
            return self._ob[attr]
        except (TypeError, KeyError):
            return getattr(self._ob, attr, default)

    def has(self, attr):
        try:
            return bool(self._ob[attr])
        except (TypeError, KeyError):
            return bool(getattr(self._ob, attr, None))

    def __iter__(self):
        return iter(self._ob)

    def __len__(self):
        return len(self._ob)


class PyGFPEncoder(simplejson.JSONEncoder):
    
    """
    Extends JSONEncoder, serializes objects which satisfy the Python
    GIS feature protocol (PyGFP). See
    http://trac.gispython.org/projects/PCL/wiki/PythonFeatureProtocol.
    """

    def crs_default(self, o):
        return {
            'type': o.get('type'),
            'properties': o.get('properties'),
            }

    def geom_default(self, o):
        if o.get('type') == 'GeometryCollection':
            value = {
                'type': 'GeometryCollection',
                'members': 
                    [self.geom_default(Fly(g)) for g in o.get('members')],
                }
            if o.has('crs'):
                value['crs'] = self.crs_default(Fly(o.get('crs')))
            return value
        else:
            value = {
                'type': o.get('type'),
                'coordinates': tuple(o.get('coordinates')),
                }
            if o.has('crs'):
                value['crs'] = self.crs_default(Fly(o.get('crs')))
            return value

    def feature_default(self, o):
        value = {
            'id': o.get('id'),
            'properties': o.get('properties'),
            'geometry': self.geom_default(Fly(o.get('geometry'))),
            }
        if o.has('crs'):
            value['crs'] = self.crs_default(Fly(o.get('crs')))
        return value

    def default(self, o):
        if o.has('coordinates'):
            return self.geom_default(o)
        elif o.has('geometry'):
            return self.feature_default(o)
        elif o.has('members'):
            value = {
                'members': [self.feature_default(Fly(m)) for m in iter(o)]
                }
            if o.has('crs'):
                value['crs'] = self.crs_default(o.get('crs'))
            return value
        else:
            return simplejson.JSONEncoder.default()


# Wrap the functions from simplejson, providing encoder, decoders, and
# object creation hooks

def dump(obj, fp):
    return simplejson.dump(Fly(obj), fp, cls=PyGFPEncoder)

def dumps(obj):
    return simplejson.dumps(Fly(obj), cls=PyGFPEncoder)

def load(fp, object_hook=None):
    return simplejson.load(fp, cls=simplejson.JSONDecoder, 
        object_hook=object_hook)

def loads(s, object_hook=None):
    return simplejson.loads(s, cls=simplejson.JSONDecoder,
        object_hook=object_hook)

