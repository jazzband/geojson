Python Geo Interface
====================

Specified here is a simple interface, when provided, allows objects to be
easily adapted for use with the Python Cartographic Library, GeoJSON, or
Shapely. It is inspired by the Numpy Array Interface, and plays a very similar
role in GIS or geospatial programming. The Geo Interface has 3 levels: feature
collections, features, and geometries.

Feature Collection
------------------

A feature collection maps 1 item:

*members*: a sequence of objects that provide the next (feature) level of the
interface.

Feature
-------

A feature object maps 3 items: 

*id*: a unique string identifier.

*properties*: a mapping of feature properties.

*geometry*: an object that provides the next (geometry) level of the interface.

Geometry
--------

A geometry object maps 3 items:

*type*: 'Point', 'Line', 'Polygon', 'Box' (multi-types not yet under
consideration).

*coordinates*: a sequence of sequences of float values in x, y, (and maybe z)
order.

Coordinate Systems
------------------

Version 1.0 does not consider coordinate systems. 

The Simplest Possible Example
-----------------------------

Here is the simplest example of all 3 levels of the interface::

  # feature collection
  {'members': [
      # feature
      {'id': '1', 'properties': {'title': 'Member One'}, 'geometry': {
          # geometry
          'type': 'Point',
          'coordinates': ((-106.0, 40.0))}
          }
      ]
  }

What the Geo Interface does is allow feature collections to be adapted to PCL
feature sources::

  >>> pcl_source = IFeatureSource(data)
  
features to be adapted for use with PCL like::

  >>> pcl_feature = IFeature(data['members'][0])

and geometries to be adapted for use with Shapely::

  >>> shapely_geom = asShape(data['members'][0]['geometry'])


Providing the Interface
-----------------------

A Python object may provide the interface directly (as does the dict above), or
expose an attribute named __geo_interface__ that directly provides the
interface. The latter is inspired by the Numpy array interface. For example::

  class Point(object):
      def __init__(self, x, y):
          self.x = x
          self.y = y    
      @property
      def __geo_interface__(self):
          return {'type': 'Point', 'coordinates': (self.x, self.y)}
  
  class Feature(object):   
      def __init__(self, id, title, geom={}):
          """The geom *must* provide the geometry geo interface."""
          self.id = id
          self.title = title
          self.geom = geom
      @property
      def __geo_interface__(self):
          return {'id': self.id, 'properties': {'title': self.title}, 'geometry': self.geom}
  
  class Collection(object):   
      def __init__(self, features=[]):
          """The features *must* provide the geometry geo interface."""
          self.features = features
      @property
      def __geo_interface__(self):
          return {'members': features}

