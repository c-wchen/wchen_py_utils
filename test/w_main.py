import unittest
# https://www.cnblogs.com/mlp1234/p/13212708.html
import sys
sys.path.append('..')

if __name__ == '__main__':
    suites = unittest.TestSuite()
    # from test_expect import TestExpectFunctions
    # from test_file import TestFileFunctions
    # suites.addTest(TestExpectFunctions())
    # suites.addTest(TestFileFunctions())
    tests = unittest.defaultTestLoader.discover('.', pattern='test*.py')
    suites.addTest(tests)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suites)