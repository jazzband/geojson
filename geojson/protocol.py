
def issupported(ob):
    """Return True if the object supports the Python feature protocol, else
    return False."""
    try:
        ob['geometry']
        ob['properties']
        ob['id']
    except KeyError:
        return False
    return True
        
