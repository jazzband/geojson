# ============================================================================
# GeoJSON. Copyright (C) 2007 Sean C. Gillies
#
# See ../LICENSE.txt
# 
# Contact: Sean Gillies, sgillies@frii.com
# ============================================================================


import simplejson
from geojson.feature import SimpleWebFeature


class PyGFPEncoder(simplejson.JSONEncoder):
    
    """
    Extends JSONEncoder, serializes objects which satisfy the Python
    GIS feature protocol (PyGFP). See
    http://trac.gispython.org/projects/PCL/wiki/PythonFeatureProtocol.
    """

    def default(self, o):
        # Try feature protocol
        try:
           return {'id': o['id'], 'geometry': o['geometry'].copy(),
                   'properties': o['properties'].copy()}
        except KeyError:
            return simplejson.JSONEncoder.default(self, o)


# Wrap the functions from simplejson, providing encoder, decoders, and
# object creation hooks

def dump(obj, fp):
    return simplejson.dump(obj, fp, cls=PyGFPEncoder)

def dumps(obj):
    return simplejson.dumps(obj, cls=PyGFPEncoder)

def load(fp, object_hook=None):
    return simplejson.load(fp, cls=simplejson.JSONDecoder, 
        object_hook=object_hook)

def loads(s, object_hook=None):
    return simplejson.loads(s, cls=simplejson.JSONDecoder,
        object_hook=object_hook)

