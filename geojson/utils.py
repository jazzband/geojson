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
    if 'features' in obj:  # FeatureCollection
        for f in obj['features']:
            yield from coords(f)
    elif 'geometry' in obj:  # Feature
        yield from coords(obj['geometry'])
    elif 'geometries' in obj:  # GeometryCollection
        for g in obj['geometries']:
            yield from coords(g)
    else:
        if isinstance(obj, (tuple, list)):
            coordinates = obj
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
        raise ValueError(f"Invalid geometry object {obj!r}")
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
        obj['geometry'] = func(obj['geometry']) if obj['geometry'] else None
        return obj
    elif obj['type'] == 'FeatureCollection':
        feats = [map_geometries(func, feat) for feat in obj['features']]
        return {'type': obj['type'], 'features': feats}
    else:
        raise ValueError(f"Invalid GeoJSON object {obj!r}")


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

    lon_min, lat_min, lon_max, lat_max = boundingBox

    def random_lon():
        return random.uniform(lon_min, lon_max)

    def random_lat():
        return random.uniform(lat_min, lat_max)

    def create_point():
        return Point((random_lon(), random_lat()))

    def create_line():
        return LineString([create_point() for _ in range(numberVertices)])

    def create_poly():
        ave_radius = 60
        ctr_x = 0.1
        ctr_y = 0.2
        irregularity = clip(0.1, 0, 1) * math.tau / numberVertices
        spikeyness = clip(0.5, 0, 1) * ave_radius

        lower = (math.tau / numberVertices) - irregularity
        upper = (math.tau / numberVertices) + irregularity
        angle_steps = []
        for _ in range(numberVertices):
            angle_steps.append(random.uniform(lower, upper))
        sum_angle = sum(angle_steps)

        k = sum_angle / math.tau
        angle_steps = [x / k for x in angle_steps]

        points = []
        angle = random.uniform(0, math.tau)

        for angle_step in angle_steps:
            r_i = clip(random.gauss(ave_radius, spikeyness), 0, 2 * ave_radius)
            x = ctr_x + r_i * math.cos(angle)
            y = ctr_y + r_i * math.sin(angle)
            x = (x + 180.0) * (abs(lon_min - lon_max) / 360.0) + lon_min
            y = (y + 90.0) * (abs(lat_min - lat_max) / 180.0) + lat_min
            x = clip(x, lon_min, lon_max)
            y = clip(y, lat_min, lat_max)
            points.append((x, y))
            angle += angle_step

        points.append(points[0])  # append first point to the end
        return Polygon([points])

    def clip(x, min_val, max_val):
        if min_val > max_val:
            return x
        else:
            return min(max(min_val, x), max_val)

    if featureType == 'Point':
        return create_point()

    if featureType == 'LineString':
        return create_line()

    if featureType == 'Polygon':
        return create_poly()

    raise ValueError(f"featureType: {featureType} is not supported.")
