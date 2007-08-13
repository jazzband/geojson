
from setuptools import setup

setup(name          = 'GeoJSON',
      version       = '1.0',
      description   = 'Encoder/decoder for simple GIS features',
      license       = 'BSD',
      keywords      = 'gis geography json',
      author        = 'Sean Gillies',
      author_email  = 'sgillies@frii.com',
      maintainer        = 'Sean Gillies',
      maintainer_email  = 'sgillies@frii.com',
      url           = 'http://trac.gispython.org/projects/PCL/wiki/GeoJSON',
      packages          = ['geojson'],
      install_requires  = ['simplejson', 'setuptools'],
      tests_require     = ['zope.testing'],
      classifiers   = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
        ],
)

