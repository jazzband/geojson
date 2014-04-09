#!/bin/sh

# Run unittests
python -m unittest discover -s tests

# Run doctests
python -m doctest README.rst
