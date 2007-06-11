from geojson.coding import Fly

def issupported(ob):
    """Return True if the object supports the Python feature protocol, else
    return False."""
    try:
        fly = Fly(ob)
        assert fly.has('id')
        assert fly.has('geometry')
        assert fly.has('properties')
    except AssertionError, e:
        raise Warning, e
        return False
    return True
        
