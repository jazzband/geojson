import sys
import io
from setuptools import setup


readme_text = io.open("README.rst", "r").read()

if sys.version_info[:2] not in [(2, 6), (2, 7)] and \
        sys.version_info[:1] not in [(3, )]:
    sys.stderr.write("Sorry, only Python 2.6, 2.7, and 3.x are supported "
                     "at this time.\n")
    exit(1)

# Get around this issue: http://bugs.python.org/issue15881
# Appears to be a problem in older versions of Python 2.6 and 2.7
import multiprocessing  # NOQA

setup(
    name="geojson",
    version="1.0.5",
    description="Python bindings and utilities for GeoJSON",
    license="BSD",
    keywords="gis geography json",
    author="Sean Gillies",
    author_email="sgillies@frii.com",
    maintainer="Corey Farwell",
    maintainer_email="coreyf@rwell.org",
    url="https://github.com/frewsxcv/geojson",
    long_description=readme_text,
    packages=["geojson"],
    package_dir={"geojson": "geojson"},
    package_data={"geojson": ["*.rst"]},
    setup_requires=["nose==1.3.0"],
    tests_require=["nose==1.3.0", "coverage==3.6"],
    install_requires=["setuptools"],
    test_suite="nose.collector",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: GIS",
    ]
)
