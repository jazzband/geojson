
import geojson
from geojson.coords import coords, map_coords

def test_point():
    itr = coords(geojson.Point((-115.81, 37.24)))
    assert next(itr) == (-115.81, 37.24)

def test_dict():
    itr = coords({'type': 'Point', 'coordinates': [-115.81, 37.24]})
    assert next(itr) == (-115.81, 37.24)

def test_point_feature():
    itr = coords(geojson.Feature(geometry=geojson.Point((-115.81, 37.24))))
    assert next(itr) == (-115.81, 37.24)

def test_multipolygon():
    g = geojson.MultiPolygon([
        ([(3.78, 9.28), (-130.91, 1.52), (35.12, 72.234), (3.78, 9.28)],),
        ([(23.18, -34.29), (-1.31, -4.61), (3.41, 77.91), (23.18, -34.29)],)])
    itr = coords(g)
    pairs = list(itr)
    assert pairs[0] == (3.78, 9.28)
    assert pairs[-1] == (23.18, -34.29)

def test_map_point():
    result = map_coords(lambda x: x, geojson.Point((-115.81, 37.24)))
    assert result['type'] == 'Point'
    assert result['coordinates'] == (-115.81, 37.24)

def test_map_linestring():
    g = geojson.LineString(
        [(3.78, 9.28), (-130.91, 1.52), (35.12, 72.234), (3.78, 9.28)])
    result = map_coords(lambda x: x, g)
    assert result['type'] == 'LineString'
    assert result['coordinates'][0] == (3.78, 9.28)
    assert result['coordinates'][-1] == (3.78, 9.28)

def test_map_polygon():
    g = geojson.Polygon([
        [(3.78, 9.28), (-130.91, 1.52), (35.12, 72.234), (3.78, 9.28)],])
    result = map_coords(lambda x: x, g)
    assert result['type'] == 'Polygon'
    assert result['coordinates'][0][0] == (3.78, 9.28)
    assert result['coordinates'][0][-1] == (3.78, 9.28)

def test_map_multipolygon():
    g = geojson.MultiPolygon([
        ([(3.78, 9.28), (-130.91, 1.52), (35.12, 72.234), (3.78, 9.28)],),
        ([(23.18, -34.29), (-1.31, -4.61), (3.41, 77.91), (23.18, -34.29)],)])
    result = map_coords(lambda x: x, g)
    assert result['type'] == 'MultiPolygon'
    assert result['coordinates'][0][0][0] == (3.78, 9.28)
    assert result['coordinates'][-1][-1][-1] == (23.18, -34.29)

