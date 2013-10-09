Changes
=======

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
