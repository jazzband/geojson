
To run the standard test suite:

$python[version] setup.py nosetests

Change options in setup.cfg under 'nosetests' as per nose documentation in order
to add/change the test suite behaviour.

For backwards compatiability, the command:

$ python setup.py test

will still work and run all doctests defined.


