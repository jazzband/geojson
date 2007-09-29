from geojson.coding import Map

def issupported(ob):
    """Return True if the object supports the Python feature protocol, else
    return False."""
    try:
        m = Map(ob)
        assert m.has('id')
        assert m.has('geometry')
        assert m.has('properties')
    except AssertionError, e:
        raise Warning, str(e)
        return False
    return True
        
