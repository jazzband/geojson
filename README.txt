geojson: encode/decode geodata
==============================

This package contains:

* The reference implementation of the Python geo interface:

  http://trac.gispython.org/lab/wiki/PythonGeoInterface

* Functions for encoding and decoding GeoJSON (http://geojson.org) formatted
  data.

Geojson provides geometry, feature, and collection classes, and supports
pickle-style dump and load of objects that provide the lab's Python geo
interface. Here's an example of a round-trip through the GeoJSON format::

  >>> import geojson
  >>> p = geojson.Point([0.0, 0.0])
  >>> p
  Point(coordinates=[0.0, 0.0])
  >>> data = geojson.dumps(p)
  >>> data
  '{"type": "Point", "coordinates": [0.0, 0.0]}'
  >>> q = geojson.loads(data, object_hook=geojson.GeoJSON.to_instance)
  >>> q
  Point(coordinates=[0.0, 0.0])

The geometry classes interoperate with Shapely via the geo interface::

  >>> from shapely.geometry import asShape
  >>> x = asShape(p)
  >>> x.wkt
  'POINT (0.0000000000000000 0.0000000000000000)'
