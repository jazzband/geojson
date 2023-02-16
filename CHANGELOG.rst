Changes
=======


3.0.1 (2022-02-15)
------------------

- Add Support for Python 3.11.x minor revisions

  - https://github.com/jazzband/geojson/pull/198


3.0.0 (2022-01-26)
------------------

- Support for Python versions 3.7-3.11 (Python 2 no longer supported)

- Primary development branch renamed from `master` to `main`

- Handle all real numbers as coordinates

  - https://github.com/jazzband/geojson/pull/188

- Default precision improvements

  - https://github.com/jazzband/geojson/pull/177

- CI improvements

  - https://github.com/jazzband/geojson/pull/172
  - https://github.com/jazzband/geojson/pull/155

- utf-8 support added to `geojson.dumps()`

  - https://github.com/jazzband/geojson/pull/165

- Polygons now constrained to bounding box

  - https://github.com/jazzband/geojson/pull/147

- Better GeometryCollection handling in `util.coords()`

  - https://github.com/jazzband/geojson/pull/146

- Improved point validation

  - https://github.com/jazzband/geojson/pull/144

2.5.0 (2019-07-18)
------------------

- Add "precision" parameter to GeoJSON Object classes with default precision of 6 (0.1m)

  - https://github.com/jazzband/geojson/pull/131

- Fix bug where `map_geometries()` util was not preserving Feature IDs

  - https://github.com/jazzband/geojson/pull/128
  - https://github.com/jazzband/geojson/pull/130

- Remove `crs` module and features to conform to official WGS84-only GeoJSON spec

  - https://github.com/jazzband/geojson/pull/124

- Set up semi-automatic PyPi releases via Travis/Jazzband

  - https://github.com/jazzband/geojson/pull/123

2.4.2 (2019-03-12)
------------------

- Tie Travis CI to jazzband instance
- Remove EOL 3.3 and 3.4 version support

  - https://github.com/jazzband/geojson/pull/120

2.4.1 (2018-10-17)
------------------

- Allow ``FeatureCollections`` to be passed to ``coords``

  - https://github.com/jazzband/geojson/pull/117

2.4.0 (2018-05-21)
------------------

- Additional functional maps for GeoJSON entities

  - https://github.com/jazzband/geojson/pull/112

2.3.0 (2017-09-18)
------------------

- Add ``__getitem__`` methods to sequence-like objects

  - https://github.com/jazzband/geojson/pull/103


2.2.0 (2017-09-17)
------------------

- Allow constructing geojson objects from geojson objects

  - https://github.com/jazzband/geojson/pull/104

2.1.0 (2017-08-29)
------------------

- Implement validation for GeometryCollection

  - https://github.com/jazzband/geojson/pull/102

2.0.0 (2017-07-28)
------------------

- Rewrite of validation mechanism (breaking change).

  - https://github.com/jazzband/geojson/pull/98

1.3.5 (2017-04-24)
------------------

- Changed the validator to allow elevation

  - https://github.com/jazzband/geojson/pull/92

1.3.4 (2017-02-11)
------------------

- Remove runtime dependency on setuptools

  - https://github.com/jazzband/geojson/pull/90

1.3.3 (2016-07-21)
------------------

- Add validate parameter to GeoJSON constructors

  - https://github.com/jazzband/geojson/pull/78

1.3.2 (2016-01-28)
------------------

- Add __version__ and __version_info__ attributes

  - https://github.com/jazzband/geojson/pull/74

1.3.1 (2015-10-12)
------------------

- Fix validation bug for MultiPolygons

  - https://github.com/jazzband/geojson/pull/63

1.3.0 (2015-08-11)
------------------

- Add utility to generate geometries with random data

  - https://github.com/jazzband/geojson/pull/60

1.2.2 (2015-07-13)
------------------

- Fix tests by including test file into build

  - https://github.com/jazzband/geojson/issues/61

- Build universal wheels

  - https://packaging.python.org/en/latest/distributing.html#universal-wheels

1.2.1 (2015-06-25)
------------------

- Encode long types correctly with Python 2.x

  - https://github.com/jazzband/geojson/pull/57

1.2.0 (2015-06-19)
------------------

- Utility function to validate GeoJSON objects

  - https://github.com/jazzband/geojson/pull/56

1.1.0 (2015-06-08)
------------------

- Stop outputting invalid GeoJSON value id=null on Features

  - https://github.com/jazzband/geojson/pull/53

1.0.9 (2014-10-05)
------------------

- Fix bug where unicode/non-string properties with a 'type' key cause a crash

1.0.8 (2014-09-30)
------------------

- Fix bug where unicode keys don't get decoded properly
- Add coords and map_coords utilities

1.0.7 (2014-04-19)
------------------

- Compatibility with Python 3.4
- Remove nose dependency
- Convert doctests to unittests
- Run tests using runtests.sh

1.0.6 (2014-01-18)
------------------

- Update README.rst documentation (fix errors, add examples)
- Allow simplejson to be used again

1.0.5 (2013-11-16)
------------------

- Remove warning about RSTs in test/ upon install

1.0.4 (2013-11-16)
------------------

- Flake8 everything
- Transition all documentation to reStructuredText
- Start using Travis CI
- Support Python 3
- Fix broken testcase when run using Python 2.6

1.0.3 (2009-11-25)
------------------

- Fixed #186
- Internal code simplification

1.0.2 (2009-11-24)
------------------

- Use nose test framework instead of rolling our own.

1.0.1 (2008-12-19)
------------------

- Handle features with null geometries (#174).

1.0 (2008-08-01)
----------------

- Final 1.0 release.
- Rename PyGFPEncoder to GeoJSONEncoder and expose it from the geojson module.

1.0rc1 (2008-07-11)
-------------------

- Release candidate.

1.0b1 (2008-07-02)
------------------

- Rename encoding module to codec.

1.0a4 (2008-04-27)
------------------

- Get in step with GeoJSON draft version 6.
- Made all code work with Python 2.4.3, 2.5.1, will test with all variations.
  (see tests/rundoctests.dist)
- Made tests use ELLIPSIS to avoid output transmogification due to floating
  point representation.
