import geojson


def is_valid(obj):
    """ IsValid provides validation for GeoJSON objects
        All of error messages obtained from the official site
        http://geojson.org/geojson-spec.html

        Args:
            obj(geoJSON object): check validation

        Returns:
            dict of two parameters 'valid' and 'message'.
            In the case if geoJSON object is valid, returns
            {valid: 'yes', message: ''}
            If json objects is not valid, returns
            {valid: 'no', message:'explanation, why this object is not valid'}

        Example:
            >> point = Point((10,20), (30,40))
            >> IsValid(point)
            >> {valid: 'yes', message: ''}
    """

    if not isinstance(obj, geojson.GeoJSON):
        return output('this is not GeoJSON object')

    if isinstance(obj, geojson.Point):
        if len(obj['coordinates']) not in (2, 3):
            return output('the "coordinates" member must be a single position')

    if isinstance(obj, geojson.MultiPoint):
        if checkListOfObjects(obj['coordinates'], lambda x: len(x) in (2, 3)):
            return output(
                'the "coordinates" member must be an array of positions'
            )

    if isinstance(obj, geojson.LineString):
        if len(obj['coordinates']) < 2:
            return output('the "coordinates" member must be an array '
                          'of two or more positions')

    if isinstance(obj, geojson.MultiLineString):
        coord = obj['coordinates']
        if checkListOfObjects(coord, lambda x: len(x) >= 2):
            return output('the "coordinates" member must be an array '
                          'of LineString coordinate arrays')

    if isinstance(obj, geojson.Polygon):
        coord = obj['coordinates']
        lengths = all([len(elem) >= 4 for elem in coord])
        if lengths is False:
            return output('LinearRing must contain with 4 or more positions')

        isring = all([elem[0] == elem[-1] for elem in coord])
        if isring is False:
            return output('The first and last positions in LinearRing'
                          'must be equivalent')

    if isinstance(obj, geojson.MultiPolygon):
        if checkListOfObjects(obj['coordinates'], lambda x: is_polygon(x)):
            return output('the "coordinates" member must be an array'
                          'of Polygon coordinate arrays')

    return output('')


def is_polygon(coords):
    lengths = all(len(elem) >= 4 for elem in coords)
    isring = all(elem[0] == elem[-1] for elem in coords)
    return lengths and isring


def checkListOfObjects(coord, pred):
    """ This method provides checking list of geojson objects such Multipoint or
        MultiLineString that each element of the list is valid geojson object.
        This is helpful method for IsValid.

    :param coord: List of coordinates
    :type coord: list
    :param pred: Predicate to check validation of each member in the coord
    :type pred: function
    :return: True if list contains valid objects, False otherwise
    :rtype: bool
    """
    return not isinstance(coord, list) or not all([pred(ls) for ls in coord])


def output(message):
    """ Output result for IsValid

    :param message: If message is not empty, object is not valid
    :type message: str
    """
    result = {'valid': 'no', 'message': ''}
    if message != '':
        result['message'] = message
        return result
    result['valid'] = 'yes'
    return result
