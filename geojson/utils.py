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


def generate_random(featureType, numberFeatures=1, numberVertices=3, boundingBox=[-180.0, -90.0, 180.0, 90.0]):

    from geojson import Point, LineString, Polygon, GeometryCollection
    import random

    lonMin = boundingBox[0]
    lonMax = boundingBox[2]

    def randomLon():
        return random.randrange(lonMin, lonMax)

    latMin = boundingBox[0]
    latMax = boundingBox[2]

    def randomLat():
        return random.randrange(latMin, latMax)

    def createPoint():
        return Point((randomLon(), randomLat()))

    def createLine():
        coords = []
        for i in range(0, numberVertices):
            coords.append((randomLon(), randomLat()))
        return LineString(coords)

    def createPoly():
        coords = []
        for i in range(0, numberVertices):
            coords.append((randomLon(), randomLat()))
        sorted(coords, key=lambda lon: lon[0])
        sorted(coords, key=lambda bla: bla[1])
        firstVal = coords[0]
        coords.append(firstVal)
        return Polygon([coords])

    if numberFeatures > 1:
        group = []
        for i in range(0, numberFeatures):
            if featureType == 'Point':
                group.append(createPoint())
            elif featureType == 'LineString':
                group.append(createLine())
            elif featureType == 'Polygon':
                group.append(createPoly())

        return GeometryCollection(group)

    else:
        if featureType == 'Point':
            return createPoint()

        if featureType == 'LineString':
            return createLine()

        if featureType == 'Polygon':
            return createPoly()
