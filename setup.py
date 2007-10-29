
from setuptools import setup

# Get text from README.txt
readme_text = file('README.txt', 'rb').read()

setup(name          = 'GeoJSON',
      version       = '1.0a4',
      description   = 'Encoder/decoder for simple GIS features',
      license       = 'BSD',
      keywords      = 'gis geography json',
      author        = 'Sean Gillies',
      author_email  = 'sgillies@frii.com',
      maintainer        = 'Sean Gillies',
      maintainer_email  = 'sgillies@frii.com',
      url           = 'http://trac.gispython.org/projects/PCL/wiki/GeoJSON',
      long_description = readme_text,
      packages          = ['geojson'],
      install_requires  = ['simplejson', 'setuptools'],
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

