import unittest


suite = unittest.TestLoader().discover("tests")
unittest.TextTestRunner(verbosity=2).run(suite)
