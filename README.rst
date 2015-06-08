python-geojson
==============

.. image:: https://img.shields.io/travis/frewsxcv/python-geojson.svg
   :target: https://travis-ci.org/frewsxcv/python-geojson
.. image:: https://img.shields.io/codecov/c/github/frewsxcv/python-geojson.svg
   :target: https://codecov.io/github/frewsxcv/python-geojson?branch=master

This library contains:

- Functions for encoding and decoding GeoJSON_ formatted data
- Classes for all GeoJSON Objects
- An implementation of the Python `__geo_interface__ Specification`_

**Table of Contents**

.. contents::
   :backlinks: none
   :local:

Installation
------------

python-geojson is compatible with Python 2.6, 2.7, 3.2, 3.3, and 3.4. It is listed on `PyPi as 'geojson'`_. The recommended way to install is via pip_:

.. code::

  pip install geojson

.. _PyPi as 'geojson': https://pypi.python.org/pypi/geojson/
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

Visualize the result of the example above `here <https://gist.github.com/frewsxcv/b5768a857f5598e405fa>`__. General information about Point can be found in `Section 2.1.2`_ and `Appendix A: Point`_ within `The GeoJSON Format Specification`_.

.. _Section 2.1.2: http://www.geojson.org/geojson-spec.html#point
.. _Appendix A\: Point: http://www.geojson.org/geojson-spec.html#id2

MultiPoint
~~~~~~~~~~

.. code:: python

  >>> from geojson import MultiPoint

  >>> MultiPoint([(-155.52, 19.61), (-156.22, 20.74), (-157.97, 21.46)])  # doctest: +ELLIPSIS
  {"coordinates": [[-155.5..., 19.6...], [-156.2..., 20.7...], [-157.9..., 21.4...]], "type": "MultiPoint"}

Visualize the result of the example above `here <https://gist.github.com/frewsxcv/be02025c1eb3aa2040ee>`__. General information about MultiPoint can be found in `Section 2.1.3`_ and `Appendix A: MultiPoint`_ within `The GeoJSON Format Specification`_.

.. _Section 2.1.3: http://www.geojson.org/geojson-spec.html#multipoint
.. _Appendix A\: MultiPoint: http://www.geojson.org/geojson-spec.html#id5


LineString
~~~~~~~~~~

.. code:: python

  >>> from geojson import LineString

  >>> LineString([(8.919, 44.4074), (8.923, 44.4075)])  # doctest: +ELLIPSIS
  {"coordinates": [[8.91..., 44.407...], [8.92..., 44.407...]], "type": "LineString"}

Visualize the result of the example above `here <https://gist.github.com/frewsxcv/758563182ca49ce8e8bb>`__. General information about LineString can be found in `Section 2.1.4`_ and `Appendix A: LineString`_ within `The GeoJSON Format Specification`_.

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

Visualize the result of the example above `here <https://gist.github.com/frewsxcv/20b6522d8242ede00bb3>`__. General information about MultiLineString can be found in `Section 2.1.5`_ and `Appendix A: MultiLineString`_ within `The GeoJSON Format Specification`_.

.. _Section 2.1.5: http://www.geojson.org/geojson-spec.html#multilinestring
.. _Appendix A\: MultiLineString: http://www.geojson.org/geojson-spec.html#id6

Polygon
~~~~~~~

.. code:: python

  >>> from geojson import Polygon

  >>> # no hole within polygon
  >>> Polygon([[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)]])  # doctest: +ELLIPSIS
  {"coordinates": [[[2.3..., 57.32...], [23.19..., -20.2...], [-120.4..., 19.1...]]], "type": "Polygon"}

  >>> # hole within polygon
  >>> Polygon([
  ...     [(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)],
  ...     [(-5.21, 23.51), (15.21, -10.81), (-20.51, 1.51), (-5.21, 23.51)]
  ... ])  # doctest: +ELLIPSIS
  {"coordinates": [[[2.3..., 57.32...], [23.19..., -20.2...], [-120.4..., 19.1...]], [[-5.2..., 23.5...], [15.2..., -10.8...], [-20.5..., 1.5...], [-5.2..., 23.5...]]], "type": "Polygon"}

Visualize the results of the example above `here <https://gist.github.com/frewsxcv/b2f5c31c10e399a63679>`__. General information about Polygon can be found in `Section 2.1.6`_ and `Appendix A: Polygon`_ within `The GeoJSON Format Specification`_.

.. _Section 2.1.6: http://www.geojson.org/geojson-spec.html#polygon
.. _Appendix A\: Polygon: http://www.geojson.org/geojson-spec.html#id4

MultiPolygon
~~~~~~~~~~~~

.. code:: python

  >>> from geojson import MultiPolygon

  >>> MultiPolygon([
  ...     ([(3.78, 9.28), (-130.91, 1.52), (35.12, 72.234), (3.78, 9.28)],),
  ...     ([(23.18, -34.29), (-1.31, -4.61), (3.41, 77.91), (23.18, -34.29)],)
  ... ])  # doctest: +ELLIPSIS
  {"coordinates": [[[[3.7..., 9.2...], [-130.9..., 1.5...], [35.1..., 72.23...]]], [[[23.1..., -34.2...], [-1.3..., -4.6...], [3.4..., 77.9...]]]], "type": "MultiPolygon"}

Visualize the result of the example above `here <https://gist.github.com/frewsxcv/e0388485e28392870b74>`__. General information about MultiPolygon can be found in `Section 2.1.7`_ and `Appendix A: MultiPolygon`_ within `The GeoJSON Format Specification`_.

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

Visualize the result of the example above `here <https://gist.github.com/frewsxcv/6ec8422e97d338a101b0>`__. General information about GeometryCollection can be found in `Section 2.1.8`_ and `Appendix A: GeometryCollection`_ within `The GeoJSON Format Specification`_.

.. _Section 2.1.8: http://www.geojson.org/geojson-spec.html#geometry-collection
.. _Appendix A\: GeometryCollection: http://www.geojson.org/geojson-spec.html#geometrycollection

Feature
~~~~~~~

.. code:: python

  >>> from geojson import Feature, Point

  >>> my_point = Point((-3.68, 40.41))

  >>> Feature(geometry=my_point)  # doctest: +ELLIPSIS
  {"geometry": {"coordinates": [-3.68..., 40.4...], "type": "Point"}, "properties": {}, "type": "Feature"}

  >>> Feature(geometry=my_point, properties={"country": "Spain"})  # doctest: +ELLIPSIS
  {"geometry": {"coordinates": [-3.68..., 40.4...], "type": "Point"}, "properties": {"country": "Spain"}, "type": "Feature"}

  >>> Feature(geometry=my_point, id=27)  # doctest: +ELLIPSIS
  {"geometry": {"coordinates": [-3.68..., 40.4...], "type": "Point"}, "id": 27, "properties": {}, "type": "Feature"}

Visualize the results of the examples above `here <https://gist.github.com/frewsxcv/4488d30209d22685c075>`__. General information about Feature can be found in `Section 2.2`_ within `The GeoJSON Format Specification`_.

.. _Section 2.2: http://geojson.org/geojson-spec.html#feature-objects

FeatureCollection
~~~~~~~~~~~~~~~~~

.. code:: python

  >>> from geojson import Feature, Point, FeatureCollection

  >>> my_feature = Feature(geometry=Point((1.6432, -19.123)))

  >>> my_other_feature = Feature(geometry=Point((-80.234, -22.532)))

  >>> FeatureCollection([my_feature, my_other_feature])  # doctest: +ELLIPSIS
  {"features": [{"geometry": {"coordinates": [1.643..., -19.12...], "type": "Point"}, "properties": {}, "type": "Feature"}, {"geometry": {"coordinates": [-80.23..., -22.53...], "type": "Point"}, "properties": {}, "type": "Feature"}], "type": "FeatureCollection"}

Visualize the result of the example above `here <https://gist.github.com/frewsxcv/34513be6fb492771ef7b>`__. General information about FeatureCollection can be found in `Section 2.3`_ within `The GeoJSON Format Specification`_.

.. _Section 2.3: http://geojson.org/geojson-spec.html#feature-collection-objects

GeoJSON encoding/decoding
-------------------------

All of the GeoJSON Objects implemented in this library can be encoded and decoded into raw GeoJSON with the ``geojson.dump``, ``geojson.dumps``, ``geojson.load``, and ``geojson.loads`` functions.

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

Helpful utilities
-----------------

coords
~~~~~~

:code:`geojson.utils.coords` yields all coordinate tuples from a geometry or feature object.

.. code:: python

  >>> import geojson

  >>> my_line = LineString([(-152.62, 51.21), (5.21, 10.69)])

  >>> my_feature = geojson.Feature(geometry=my_line)

  >>> list(geojson.utils.coords(my_feature))  # doctest: +ELLIPSIS
  [(-152.62..., 51.21...), (5.21..., 10.69...)]

map_coords
~~~~~~~~~~

:code:`geojson.utils.map_coords` maps a function over all coordinate tuples and returns a geometry of the same type. Useful for translating a geometry in space or flipping coordinate order.

.. code:: python

  >>> import geojson

  >>> new_point = geojson.utils.map_coords(lambda x: x/2, geojson.Point((-115.81, 37.24)))

  >>> geojson.dumps(new_point, sort_keys=True)  # doctest: +ELLIPSIS
  '{"coordinates": [-57.905..., 18.62...], "type": "Point"}'

Development
-----------

To build this project, run :code:`python setup.py build`. To run the unit tests, run :code:`python setup.py test`.

Credits
-------

* Sean Gillies <sgillies@frii.com>
* Matthew Russell <matt@sanoodi.com>
* Corey Farwell <coreyf@rwell.org>
* Blake Grotewold <hello@grotewold.me>
* Zsolt Ero <zsolt.ero@gmail.com>


.. _GeoJSON: http://geojson.org/
.. _The GeoJSON Format Specification: http://www.geojson.org/geojson-spec.html
.. _\_\_geo\_interface\_\_ Specification: https://gist.github.com/sgillies/2217756
