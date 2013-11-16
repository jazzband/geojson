python-geojson
==============

.. image:: https://travis-ci.org/frewsxcv/python-geojson.png?branch=master
   :target: https://travis-ci.org/frewsxcv/python-geojson

Python bindings for GeoJSON
This package contains:

- Functions for encoding and decoding GeoJSON_ formatted data.
- The reference implementation of the Python geo interface:

geojson provides geometry, feature, and collection classes, and supports pickle-style dump and load of objects that provide the lab's Python geo interface. Here's an example of a round-trip through the GeoJSON format:

Installation
------------

python-geojson is compatible with Python 2.6, 2.7, 3.2, and 3.3. It is listed on `PyPi as 'geojson'`_. The recommended way to install is via pip_:

.. code::

  pip install geojson

.. _PyPi as geojson: https://pypi.python.org/pypi/geojson/
.. _pip: http://www.pip-installer.org

GeoJSON Objects
---------------

This library implements all the `GeoJSON Objects`_ described in `The GeoJSON Format Specification`_.

.. _GeoJSON Objects: http://www.geojson.org/geojson-spec.html#geojson-objects

Point
~~~~~

.. code:: python

  >>> from geojson import Point

  >>> Point((-115.81, 37.24))  # doctest: +ELLIPSIS
  {"coordinates": [-115.8..., 37.2...], "type": "Point"}

General information about Point can be found in `Section 2.1.2`_ and `Appendix A: Point`_ within `The GeoJSON Format Specification`_.

.. _Section 2.1.2: http://www.geojson.org/geojson-spec.html#point
.. _Appendix A\: Point: http://www.geojson.org/geojson-spec.html#id2

MultiPoint
~~~~~~~~~~

.. code:: python

  >>> from geojson import MultiPoint

  >>> MultiPoint([(-155.52, 19.61), (-156.22, 20.74), (-157.97, 21.46)])  # doctest: +ELLIPSIS
  {"coordinates": [[-155.5..., 19.6...], [-156.2..., 20.7...], [-157.9..., 21.4...]], "type": "MultiPoint"}

General information about MultiPoint can be found in `Section 2.1.3`_ and `Appendix A: MultiPoint`_ within `The GeoJSON Format Specification`_.

.. _Section 2.1.3: http://www.geojson.org/geojson-spec.html#multipoint
.. _Appendix A\: MultiPoint: http://www.geojson.org/geojson-spec.html#id5


LineString
~~~~~~~~~~

.. code:: python

  >>> from geojson import LineString

  >>> LineString([(8.919, 44.4074), (8.923, 44.4075)])  # doctest: +ELLIPSIS
  {"coordinates": [[8.91..., 44.407...], [8.92..., 44.407...]], "type": "LineString"}

General information about LineString can be found in `Section 2.1.4`_ and `Appendix A: LineString`_ within `The GeoJSON Format Specification`_.

.. _Section 2.1.4: http://www.geojson.org/geojson-spec.html#linestring
.. _Appendix A\: LineString: http://www.geojson.org/geojson-spec.html#id3

MultiLineString
~~~~~~~~~~~~~~~

.. code:: python

  >>> from geojson import MultiLineString

  >>> MultiLineString([
  ...     [(3.75, 9.25), (-130.95, 1.52)],
  ...     [(23.15, -34.25), (-1.35, -4.65), (3.45, 77.95)]
  ... ])  # doctest: +ELLIPSIS
  {"coordinates": [[[3.7..., 9.2...], [-130.9..., 1.52...]], [[23.1..., -34.2...], [-1.3..., -4.6...], [3.4..., 77.9...]]], "type": "MultiLineString"}

General information about MultiLineString can be found in `Section 2.1.5`_ and `Appendix A: MultiLineString`_ within `The GeoJSON Format Specification`_.

.. _Section 2.1.5: http://www.geojson.org/geojson-spec.html#multilinestring
.. _Appendix A\: MultiLineString: http://www.geojson.org/geojson-spec.html#id6

Polygon
~~~~~~~

.. code:: python

  >>> from geojson import Polygon

  >>> Polygon([(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15)])  # doctest: +ELLIPSIS
  {"coordinates": [[2.3..., 57.32...], [23.19..., -20.2...], [-120.4..., 19.1...]], "type": "Polygon"}

General information about Polygon can be found in `Section 2.1.6`_ and `Appendix A: Polygon`_ within `The GeoJSON Format Specification`_.

.. _Section 2.1.6: http://www.geojson.org/geojson-spec.html#polygon
.. _Appendix A\: Polygon: http://www.geojson.org/geojson-spec.html#id4

MultiPolygon
~~~~~~~~~~~~

.. code:: python

  >>> from geojson import MultiPolygon

  >>> MultiPolygon([
  ...     [(3.78, 9.28), (-130.91, 1.52), (35.12, 72.234)],
  ...     [(23.18, -34.29), (-1.31, -4.61), (3.41, 77.91)]
  ... ])  # doctest: +ELLIPSIS
  {"coordinates": [[[3.7..., 9.2...], [-130.9..., 1.5...], [35.1..., 72.23...]], [[23.1..., -34.2...], [-1.3..., -4.6...], [3.4..., 77.9...]]], "type": "MultiPolygon"}

General information about MultiPolygon can be found in `Section 2.1.7`_ and `Appendix A: MultiPolygon`_ within `The GeoJSON Format Specification`_.

.. _Section 2.1.7: http://www.geojson.org/geojson-spec.html#multipolygon
.. _Appendix A\: MultiPolygon: http://www.geojson.org/geojson-spec.html#id7

GeometryCollection
~~~~~~~~~~~~~~~~~~

.. code:: python

  >>> from geojson import GeometryCollection, Point, LineString

  >>> my_point = Point((23.532, -63.12))

  >>> my_line = LineString([(-152.62, 51.21), (5.21, 10.69)])

  >>> GeometryCollection([my_point, my_line])  # doctest: +ELLIPSIS
  {"geometries": [{"coordinates": [23.53..., -63.1...], "type": "Point"}, {"coordinates": [[-152.6..., 51.2...], [5.2..., 10.6...]], "type": "LineString"}], "type": "GeometryCollection"}

General information about GeometryCollection can be found in `Section 2.1.8`_ and `Appendix A: GeometryCollection`_ within `The GeoJSON Format Specification`_.

.. _Section 2.1.8: http://www.geojson.org/geojson-spec.html#geometrycollection
.. _Appendix A\: GeometryCollection: http://www.geojson.org/geojson-spec.html#geometrycollection

Feature
~~~~~~~

.. code:: python

  >>> from geojson import Feature, Point

  >>> my_point = Point((43.24, -1.532))

  >>> Feature(geometry=my_point)  # doctest: +ELLIPSIS
  {"geometry": {"coordinates": [43.2..., -1.53...], "type": "Point"}, "id": null, "properties": {}, "type": "Feature"}

  >>> Feature(geometry=my_point, properties={"country": "Spain"})  # doctest: +ELLIPSIS
  {"geometry": {"coordinates": [43.2..., -1.53...], "type": "Point"}, "id": null, "properties": {"country": "Spain"}, "type": "Feature"}

  >>> Feature(geometry=my_point, id=27)  # doctest: +ELLIPSIS
  {"geometry": {"coordinates": [43.2..., -1.53...], "type": "Point"}, "id": 27, "properties": {}, "type": "Feature"}

General information about Feature can be found in `Section 2.2`_ within `The GeoJSON Format Specification`_.

.. _Section 2.2: http://geojson.org/geojson-spec.html#feature-objects

FeatureCollection
~~~~~~~~~~~~~~~~~

.. code:: python

  >>> from geojson import Feature, Point, FeatureCollection

  >>> my_feature = Feature(geometry=Point((1.6432, -19.123)))

  >>> my_other_feature = Feature(geometry=Point((-80.234, -22.532)))

  >>> FeatureCollection([my_feature, my_other_feature])  # doctest: +ELLIPSIS
  {"features": [{"geometry": {"coordinates": [1.643..., -19.12...], "type": "Point"}, "id": null, "properties": {}, "type": "Feature"}, {"geometry": {"coordinates": [-80.23..., -22.53...], "type": "Point"}, "id": null, "properties": {}, "type": "Feature"}], "type": "FeatureCollection"}

General information about FeatureCollection can be found in `Section 2.3`_ within `The GeoJSON Format Specification`_.

.. _Section 2.3: http://geojson.org/geojson-spec.html#feature-collection-objects

GeoJSON encoding/decoding
-------------------------

All of the GeoJSON Objects implemented in this library can be encoded and decoded into raw GeoJSON with the ``geosjon.dump``, ``geojson.dumps``, ``geojson.load``, and ``geojson.loads`` functions.

.. code:: python

  >>> import geojson

  >>> my_point = geojson.Point((43.24, -1.532))

  >>> my_point  # doctest: +ELLIPSIS
  {"coordinates": [43.2..., -1.53...], "type": "Point"}

  >>> dump = geojson.dumps(my_point, sort_keys=True)

  >>> dump  # doctest: +ELLIPSIS
  '{"coordinates": [43.2..., -1.53...], "type": "Point"}'

  >>> geojson.loads(dump)  # doctest: +ELLIPSIS
  {"coordinates": [43.2..., -1.53...], "type": "Point"}

Custom classes
~~~~~~~~~~~~~~

This encoding/decoding functionality shown in the previous can be extended to custom classes using the interface described by the `__geo_interface__ Specification`_.

.. _\_\_geo\_interface\_\_ Specification: http://google.com

.. code:: python

  >>> import geojson

  >>> class MyPoint():
  ...     def __init__(self, x, y):
  ...         self.x = x
  ...         self.y = y
  ...
  ...     @property
  ...     def __geo_interface__(self):
  ...         return {'type': 'Point', 'coordinates': (self.x, self.y)}

  >>> point_instance = MyPoint(52.235, -19.234)

  >>> geojson.dumps(point_instance, sort_keys=True)  # doctest: +ELLIPSIS
  '{"coordinates": [52.23..., -19.23...], "type": "Point"}'

Credits
-------

* Sean Gillies <sgillies@frii.com>
* Matthew Russell <matt@sanoodi.com>
* Corey Farwell <coreyf@rwell.org>


.. _GeoJSON: http://geojson.org/
.. _The GeoJSON Format Specification: http://www.geojson.org/geojson-spec.html
