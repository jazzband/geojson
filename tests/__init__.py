import doctest
import glob
import os

optionflags = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.NORMALIZE_WHITESPACE |
               doctest.ELLIPSIS)

_basedir = os.path.dirname(__file__)
paths = glob.glob("%s/*.txt" % _basedir)
test_suite = doctest.DocFileSuite(*paths, **dict(module_relative=False,
                                                 optionflags=optionflags))
