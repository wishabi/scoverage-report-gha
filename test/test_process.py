import unittest
import os
from main.process import process_report
from main.models import CoverageType, CoverageEntry, ReportCoverage


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
            cov_type=CoverageType.OVERALL,
            threshold=threshold
        )
        coverage_per_package = [
            CoverageEntry('com.app.testproject', 0.9880952380952381, cov_type=CoverageType.PACKAGE),
            CoverageEntry('com.app.testproject.config', 0.8518518518518519, cov_type=CoverageType.PACKAGE),
            CoverageEntry('com.app.testproject.monitoring', 0.9655172413793104, cov_type=CoverageType.PACKAGE),
            CoverageEntry('com.app.testproject.serde', 0.851063829787234, cov_type=CoverageType.PACKAGE),
        ]
        expected_results = ReportCoverage(
            overall=overall_coverage,
            packages=coverage_per_package,
            changed_files=[]
        )
        self.assertEqual(results, expected_results)

    def test_process_report_changed_files(self):
        threshold = 0.99
        changed_files = [
            'src/main/scala/com/app/testproject/config/StorageConfig.scala',
            'src/main/scala/com/app/testproject/Processor.scala',
            'README.md'
        ]
        results = process_report(self.TEST_COVERAGE_FILE, threshold, changed_files)
        overall_coverage = CoverageEntry(
            'statement_coverage',
            0.9502617801047121,
            cov_type=CoverageType.OVERALL,
            threshold=threshold
        )
        coverage_per_package = [
            CoverageEntry('com.app.testproject', 0.9880952380952381, cov_type=CoverageType.PACKAGE),
            CoverageEntry('com.app.testproject.config', 0.8518518518518519, cov_type=CoverageType.PACKAGE),
            CoverageEntry('com.app.testproject.monitoring', 0.9655172413793104, cov_type=CoverageType.PACKAGE),
            CoverageEntry('com.app.testproject.serde', 0.851063829787234, cov_type=CoverageType.PACKAGE),
        ]
        coverage_per_changed_file = [
            CoverageEntry('Processor.scala - ProcessorLive', 0.9926470588235294, cov_type=CoverageType.CHANGED_FILE),
            CoverageEntry('Processor.scala - Processor', 1.0, cov_type=CoverageType.CHANGED_FILE),
            CoverageEntry('StorageConfig.scala - StorageConfig', 0.7037037037037037, cov_type=CoverageType.CHANGED_FILE)
        ]
        expected_results = ReportCoverage(
            overall=overall_coverage,
            packages=coverage_per_package,
            changed_files=coverage_per_changed_file
        )
        self.assertEqual(results, expected_results)


if __name__ == '__main__':
    unittest.main()
