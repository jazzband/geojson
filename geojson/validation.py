import geojson

def IsValid(obj):
    result = {'valid': 'no', 'message':''}
    if isinstance(obj, geojson.LineString):
        if len(obj['coordinates']) < 2:
            result['message'] = 'the "coordinates" member must be an array \
                    of two or more positions'
            return result

    if isinstance(obj, geojson.MultiLineString):
        coord = obj['coordinates']
        if not isinstance(coord, list) or \
                not all([len(ls) >= 2 for ls in coord]):
            result['message'] = 'the "coordinates" member must be an array \
                    of LineString coordinate arrays'
            return result
    result['valid'] = 'yes'
    return result

