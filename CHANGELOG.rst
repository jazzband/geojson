Changes
=======

1.2.0 (2015-06-19)
------------------

- Utility function to validate GeoJSON objects

  - https://github.com/frewsxcv/python-geojson/pull/56

1.1.0 (2015-06-08)
------------------

- Stop outputting invalid GeoJSON value id=null on Features

  - https://github.com/frewsxcv/python-geojson/pull/53

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
