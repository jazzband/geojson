import doctest
import glob
import os

optionflags = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.NORMALIZE_WHITESPACE |
               doctest.ELLIPSIS)

_basedir = os.path.dirname(__file__)
paths = glob.glob(f"{_basedir}/*.txt")
test_suite = doctest.DocFileSuite(*paths, **dict(module_relative=False,
                                                 optionflags=optionflags))
