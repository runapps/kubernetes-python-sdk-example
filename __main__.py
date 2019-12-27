import unittest
from unit_test import deployment_unittest
from unit_test import serviceaccount_unittest
import xmlrunner
import sys

if __name__ == '__main__':
    args = sys.argv
    runner = xmlrunner.XMLTestRunner(output='unit_test/jenkins_output')
    discovery = unittest.TestLoader().discover(args[1], pattern='*.py')
    runner.run(discovery)

"""
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromModule(deployment_unittest)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromModule(serviceaccount_unittest)
    unittest.TextTestRunner(verbosity=2).run(suite)
"""