from setuptools import setup

readme_text = open("README.txt", "rb").read()
version = open("VERSION.txt", "rb").read().strip()

setup(name          = "geojson",
      version       = version,
      description   = "Encoder/decoder for simple GIS features",
      license       = "BSD",
      keywords      = "gis geography json",
      author        = "Sean Gillies",
      author_email  = "sgillies@frii.com",
      maintainer        = "Sean Gillies",
      maintainer_email  = "sgillies@frii.com",
      url           = "http://trac.gispython.org/lab/wiki/GeoJSON",
      long_description = readme_text,
      packages          = ["geojson"],
      install_requires  = ["simplejson", "setuptools"],
      test_suite    = "tests.test_suite",
      classifiers   = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: GIS",
        ],
)
