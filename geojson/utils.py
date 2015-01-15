"""Coordinate utility functions."""


def coords(obj):
    """
    Yields the coordinates from a Feature or Geometry.

    :param obj: A geometry or feature to extract the coordinates from."
    :type obj: Feature, Geometry
    :return: A generator with coordinate tuples from the geometry or feature.
    :rtype: generator
    """

    if isinstance(obj, (tuple, list)):
        coordinates = obj
    elif 'geometry' in obj:
        coordinates = obj['geometry']['coordinates']
    else:
        coordinates = obj.get('coordinates', obj)
    for e in coordinates:
        if isinstance(e, (float, int)):
            yield tuple(coordinates)
            break
        for f in coords(e):
            yield f


def map_coords(func, obj):
    """
    Returns the coordinates from a Geometry after applying the provided
    function to the tuples.

    :param obj: A geometry or feature to extract the coordinates from.
    :type obj: Point, LineString, MultiPoint, MultiLineString, Polygon,
    MultiPolygon
    :return: The result of applying the function to each coordinate array.
    :rtype: list
    :raises ValueError: if the provided object is not a Geometry.
    """

    if obj['type'] == 'Point':
        coordinates = tuple(map(func, obj['coordinates']))
    elif obj['type'] in ['LineString', 'MultiPoint']:
        coordinates = [tuple(map(func, c)) for c in obj['coordinates']]
    elif obj['type'] in ['MultiLineString', 'Polygon']:
        coordinates = [[
            tuple(map(func, c)) for c in curve]
            for curve in obj['coordinates']]
    elif obj['type'] == 'MultiPolygon':
        coordinates = [[[
            tuple(map(func, c)) for c in curve]
            for curve in part]
            for part in obj['coordinates']]
    else:
        raise ValueError("Invalid geometry object %s" % repr(obj))
    return {'type': obj['type'], 'coordinates': coordinates}
