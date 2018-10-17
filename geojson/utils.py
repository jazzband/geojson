"""Coordinate utility functions."""


def coords(obj):
    """
    Yields the coordinates from a Feature or Geometry.

    :param obj: A geometry or feature to extract the coordinates from.
    :type obj: Feature, Geometry
    :return: A generator with coordinate tuples from the geometry or feature.
    :rtype: generator
    """
    # Handle recursive case first
    if 'features' in obj:
        for f in obj['features']:
            # For Python 2 compatibility
            # See https://www.reddit.com/r/learnpython/comments/4rc15s/yield_from_and_python_27/ # noqa: E501
            for c in coords(f):
                yield c
    else:
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
    Returns the mapped coordinates from a Geometry after applying the provided
    function to each dimension in tuples list (ie, linear scaling).

    :param func: Function to apply to individual coordinate values
    independently
    :type func: function
    :param obj: A geometry or feature to extract the coordinates from.
    :type obj: Point, LineString, MultiPoint, MultiLineString, Polygon,
    MultiPolygon
    :return: The result of applying the function to each dimension in the
    array.
    :rtype: list
    :raises ValueError: if the provided object is not GeoJSON.
    """

    def tuple_func(coord):
        return (func(coord[0]), func(coord[1]))

    return map_tuples(tuple_func, obj)


def map_tuples(func, obj):
    """
    Returns the mapped coordinates from a Geometry after applying the provided
    function to each coordinate.

    :param func: Function to apply to tuples
    :type func: function
    :param obj: A geometry or feature to extract the coordinates from.
    :type obj: Point, LineString, MultiPoint, MultiLineString, Polygon,
    MultiPolygon
    :return: The result of applying the function to each dimension in the
    array.
    :rtype: list
    :raises ValueError: if the provided object is not GeoJSON.
    """

    if obj['type'] == 'Point':
        coordinates = tuple(func(obj['coordinates']))
    elif obj['type'] in ['LineString', 'MultiPoint']:
        coordinates = [tuple(func(c)) for c in obj['coordinates']]
    elif obj['type'] in ['MultiLineString', 'Polygon']:
        coordinates = [[
            tuple(func(c)) for c in curve]
            for curve in obj['coordinates']]
    elif obj['type'] == 'MultiPolygon':
        coordinates = [[[
            tuple(func(c)) for c in curve]
            for curve in part]
            for part in obj['coordinates']]
    elif obj['type'] in ['Feature', 'FeatureCollection', 'GeometryCollection']:
        return map_geometries(lambda g: map_tuples(func, g), obj)
    else:
        raise ValueError("Invalid geometry object %s" % repr(obj))
    return {'type': obj['type'], 'coordinates': coordinates}


def map_geometries(func, obj):
    """
    Returns the result of passing every geometry in the given geojson object
    through func.

    :param func: Function to apply to tuples
    :type func: function
    :param obj: A geometry or feature to extract the coordinates from.
    :type obj: GeoJSON
    :return: The result of applying the function to each geometry
    :rtype: list
    :raises ValueError: if the provided object is not geojson.
    """
    simple_types = [
        'Point',
        'LineString',
        'MultiPoint',
        'MultiLineString',
        'Polygon',
        'MultiPolygon',
    ]

    if obj['type'] in simple_types:
        return func(obj)
    elif obj['type'] == 'GeometryCollection':
        geoms = [func(geom) if geom else None for geom in obj['geometries']]
        return {'type': obj['type'], 'geometries': geoms}
    elif obj['type'] == 'Feature':
        geom = func(obj['geometry']) if obj['geometry'] else None
        return {
            'type': obj['type'],
            'geometry': geom,
            'properties': obj['properties'],
        }
    elif obj['type'] == 'FeatureCollection':
        feats = [map_geometries(func, feat) for feat in obj['features']]
        return {'type': obj['type'], 'features': feats}
    else:
        raise ValueError("Invalid GeoJSON object %s" % repr(obj))


def generate_random(featureType, numberVertices=3,
                    boundingBox=[-180.0, -90.0, 180.0, 90.0]):
    """
    Generates random geojson features depending on the parameters
    passed through.
    The bounding box defaults to the world - [-180.0, -90.0, 180.0, 90.0].
    The number of vertices defaults to 3.

    :param featureType: A geometry type
    :type featureType: Point, LineString, Polygon
    :param numberVertices: The number vertices that a linestring or polygon
    will have
    :type numberVertices: int
    :param boundingBox: A bounding box in which features will be restricted to
    :type boundingBox: list
    :return: The resulting random geojson object or geometry collection.
    :rtype: object
    :raises ValueError: if there is no featureType provided.
    """

    from geojson import Point, LineString, Polygon
    import random
    import math

    lonMin = boundingBox[0]
    lonMax = boundingBox[2]

    def randomLon():
        return random.uniform(lonMin, lonMax)

    latMin = boundingBox[1]
    latMax = boundingBox[3]

    def randomLat():
        return random.uniform(latMin, latMax)

    def createPoint():
        return Point((randomLon(), randomLat()))

    def createLine():
        return LineString([createPoint() for unused in range(numberVertices)])

    def createPoly():
        aveRadius = 60
        ctrX = 0.1
        ctrY = 0.2
        irregularity = clip(0.1, 0, 1) * 2 * math.pi / numberVertices
        spikeyness = clip(0.5, 0, 1) * aveRadius

        angleSteps = []
        lower = (2 * math.pi / numberVertices) - irregularity
        upper = (2 * math.pi / numberVertices) + irregularity
        sum = 0
        for i in range(numberVertices):
            tmp = random.uniform(lower, upper)
            angleSteps.append(tmp)
            sum = sum + tmp

        k = sum / (2 * math.pi)
        for i in range(numberVertices):
            angleSteps[i] = angleSteps[i] / k

        points = []
        angle = random.uniform(0, 2 * math.pi)

        for i in range(numberVertices):
            r_i = clip(random.gauss(aveRadius, spikeyness), 0, 2 * aveRadius)
            x = ctrX + r_i * math.cos(angle)
            y = ctrY + r_i * math.sin(angle)
            points.append((int(x), int(y)))
            angle = angle + angleSteps[i]

        firstVal = points[0]
        points.append(firstVal)
        return Polygon([points])

    def clip(x, min, max):
        if(min > max):
            return x
        elif(x < min):
            return min
        elif(x > max):
            return max
        else:
            return x

    if featureType == 'Point':
        return createPoint()

    if featureType == 'LineString':
        return createLine()

    if featureType == 'Polygon':
        return createPoly()
