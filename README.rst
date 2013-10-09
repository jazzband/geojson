geojson: encode/decode geodata
==============================

.. image:: https://travis-ci.org/frewsxcv/geojson.png?branch=master
   :target: https://travis-ci.org/frewsxcv/geojson

This package contains:

- The reference implementation of the Python geo interface:

  https://gist.github.com/2217756

- Functions for encoding and decoding GeoJSON_ formatted
  data.

geojson provides geometry, feature, and collection classes, and supports
pickle-style dump and load of objects that provide the lab's Python geo
interface. Here's an example of a round-trip through the GeoJSON format:

.. code:: python

  >>> import geojson
  >>> p = geojson.Point([0.0, 0.0])
  >>> p 
  {"coordinates": [0.0, 0.0], "type": "Point"}

  >>> data = geojson.dumps(p)
  >>> data # doctest: +ELLIPSIS
  '{"type": "Point", "coordinates": [0.0, 0.0]}'

  >>> q = geojson.loads(data)
  >>> q # doctest: +ELLIPSIS
  {"coordinates": [0..., 0...], "type": "Point"}


The geometry classes interoperate with Shapely via the geo interface:

.. code:: python

  >>> x = None
  ... try:
  ...     from shapely.geometry import asShape
  ... except ImportError:
  ...     pass
  ... else:
  ...     x = asShape(p)
  ...     x.wkt
  >>> if x:  
  ...    x ==  'POINT (0.0000000000000000 0.0000000000000000)'
  ... else:
  ...    x is None
  True

.. _GeoJSON: http://geojson.org/


Credits
-------

* Sean Gillies <sgillies@frii.com>
* Matthew Russell <matt@sanoodi.com>
* Corey Farwell <coreyf@rwell.org>
