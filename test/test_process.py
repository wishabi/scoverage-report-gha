import unittest
import os
from main.process import process_report


class TestProcess(unittest.TestCase):
    TEST_COVERAGE_FILE = os.path.join(os.path.dirname(__file__),
                                      'resources',
                                      'scoverage.xml')

    def test_process_report(self):
        results = process_report(self.TEST_COVERAGE_FILE)
        expected_results = {
            'statement_coverage': 0.9502617801047121,
            'com.app.testproject': 0.9880952380952381,
            'com.app.testproject.config': 0.8518518518518519,
            'com.app.testproject.monitoring': 0.9655172413793104,
            'com.app.testproject.serde': 0.85106382978723
        }
        self.assertEqual(results, expected_results)


if __name__ == '__main__':
    unittest.main()
