import sys
from setuptools import setup

readme_text = open("README.rst", "rb").read()
version = open("VERSION.txt", "rb").read().strip()

deps = ["setuptools"]

if sys.version_info[:2] not in [(2, 6), (2, 7)]:
    sys.stderr.write("Sorry, only Python 2.6 and Python 2.7 are supported "
                     "at this time. Python 3.x support is coming soon.\n")
    exit(1)


setup(
    name="geojson",
    version=version,
    description="Encoder/decoder for simple GIS features",
    license="BSD",
    keywords="gis geography json",
    author="Sean Gillies",
    author_email="sgillies@frii.com",
    maintainer="Sean Gillies",
    maintainer_email="sgillies@frii.com",
    url="http://trac.gispython.org/lab/wiki/GeoJSON",
    long_description=readme_text,
    packages=["geojson"],
    package_dir={"geojson": "geojson"},
    package_data={"geojson": ["VERSION.txt"]},
    setup_requires=["nose==1.3.0"],
    tests_require=["nose==1.3.0", "coverage==3.6"],
    install_requires=deps,
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
