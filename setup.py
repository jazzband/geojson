from setuptools import setup
import sys
import re


with open("README.rst") as readme_file:
    readme_text = readme_file.read()

VERSIONFILE = "geojson/_version.py"
verstrline = open(VERSIONFILE).read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError(f"Unable to find version string in {VERSIONFILE}.")


def test_suite():
    import doctest
    import unittest

    suite = unittest.TestLoader().discover("tests")
    suite.addTest(doctest.DocFileSuite("README.rst"))
    return suite


major_version, minor_version = sys.version_info[:2]
if not (major_version == 3 and 7 <= minor_version <= 11):
    sys.stderr.write("Sorry, only Python 3.7 - 3.11 are "
                     "supported at this time.\n")
    exit(1)

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
    python_requires=">=3.7, <3.12",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: GIS",
    ]
)
