
from setuptools import setup

setup(name          = 'GeoJSON',
      version       = '0.1.0',
      description   = 'Encoder/decoder for simple GIS features',
      license       = 'BSD',
      keywords      = 'gis geography json',
      author        = 'Sean Gillies',
      author_email  = 'sgillies@frii.com',
      maintainer        = 'Sean Gillies',
      maintainer_email  = 'sgillies@frii.com',
      url           = 'http://trac.gispython.org/projects/PCL/wiki/PythonFeatureProtocol',
      packages      = ['geojson'],
      classifiers   = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
        ],
)

