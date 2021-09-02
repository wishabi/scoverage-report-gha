import unittest
import os
from main.process import process_report
from main.models import CoverageEntry, ReportCoverage


class TestProcess(unittest.TestCase):
    TEST_COVERAGE_FILE = os.path.join(
        os.path.dirname(__file__),
        'resources',
        'scoverage.xml'
    )

    def test_process_report(self):
        threshold = 0.99
        results = process_report(self.TEST_COVERAGE_FILE, threshold)
        overall_coverage = CoverageEntry(
            'statement_coverage',
            0.9502617801047121,
            is_package=False,
            threshold=threshold
        )
        coverage_per_package = [
            CoverageEntry('com.app.testproject', 0.9880952380952381, is_package=True),
            CoverageEntry('com.app.testproject.config', 0.8518518518518519, is_package=True),
            CoverageEntry('com.app.testproject.monitoring', 0.9655172413793104, is_package=True),
            CoverageEntry('com.app.testproject.serde', 0.851063829787234, is_package=True),
        ]
        expected_results = ReportCoverage(
            overall=overall_coverage,
            packages=coverage_per_package
        )
        self.assertEqual(results, expected_results)


if __name__ == '__main__':
    unittest.main()
