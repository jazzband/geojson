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
    except:
        import unittest

    suite = unittest.TestLoader().discover("tests")
    suite.addTest(doctest.DocFileSuite("README.rst"))
    return suite


if sys.version_info[:2] not in [(2, 6), (2, 7)] and \
        sys.version_info[:1] not in [(3, )]:
    sys.stderr.write("Sorry, only Python 2.7, and 3.x are supported "
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
    maintainer="Corey Farwell",
    maintainer_email="coreyf@rwell.org",
    url="https://github.com/frewsxcv/python-geojson",
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
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: GIS",
    ]
)
