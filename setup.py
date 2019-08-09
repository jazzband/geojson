import io
from setuptools import setup
import sys
import re


with io.open("README.rst") as readme_file:
    readme_text = readme_file.read()

VERSIONFILE = "geojson/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


def test_suite():
    import doctest
    try:
        import unittest2 as unittest
    except ImportError:
        import unittest

    suite = unittest.TestLoader().discover("tests")
    suite.addTest(doctest.DocFileSuite("README.rst"))
    return suite


major_version, minor_version = sys.version_info[:2]
if not ((major_version == 2 and minor_version == 7)
        or (major_version == 3 and minor_version >= 5)):
    sys.stderr.write("Sorry, only Python 2.7, 3.5, 3.6 and 3.7 are supported "
                     "at this time.\n")
    exit(1)

# Get around this issue: http://bugs.python.org/issue15881
# Appears to be a problem in older versions of Python 2.7
import multiprocessing  # NOQA

setup(
    name="geojson",
    version=verstr,
    description="Python bindings and utilities for GeoJSON",
    license="BSD",
    keywords="gis geography json",
    author="Sean Gillies",
    author_email="sgillies@frii.com",
    maintainer="Ray Riga",
    maintainer_email="ray@strongoutput.com",
    url="https://github.com/jazzband/geojson",
    long_description=readme_text,
    packages=["geojson"],
    package_dir={"geojson": "geojson"},
    package_data={"geojson": ["*.rst"]},
    install_requires=[],
    test_suite="setup.test_suite",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: GIS",
    ]
)
