import unittest
from .config import config
from main.models import CoverageType, ReportCoverage, CoverageEntry
from main.render import render_pr_comment


class TestRender(unittest.TestCase):

    ICON_MAPPINGS = config['render']['icon_mappings']

    def test_render_pr_comment_pass_threshold(self):
        results = ReportCoverage(
            overall=CoverageEntry('statement_coverage', 0.75, threshold=0.20, cov_type=CoverageType.OVERALL),
            packages=[
                CoverageEntry('com.app.pk1', 0.9, cov_type=CoverageType.PACKAGE),
                CoverageEntry('com.app.pk2', 0.6, cov_type=CoverageType.PACKAGE)
            ],
            changed_files=[]
        )
        comment = render_pr_comment(results, self.ICON_MAPPINGS)
        expected_comment = self.__build_comment([
            '|Overall|%|Status|',
            '|:-|:-:|:-:|',
            '|Statement Coverage|75.0|:white_check_mark:|',
            '',
            '|Changed File(s)|%|Status|',
            '|:-|:-:|:-:|',
            '',
            '|Package Coverage|%|Status|',
            '|:-|:-:|:-:|',
            '|com.app.pk1|90.0||',
            '|com.app.pk2|60.0||'
        ])
        self.assertEqual(comment.msg, expected_comment)

    def test_render_pr_comment_fail_threshold(self):
        results = ReportCoverage(
            overall=CoverageEntry('statement_coverage', 0.60, threshold=0.90, cov_type=CoverageType.OVERALL),
            packages=[
                CoverageEntry('com.app.pk1', 0.7, cov_type=CoverageType.PACKAGE),
                CoverageEntry('com.app.pk2', 0.5, cov_type=CoverageType.PACKAGE)
            ],
            changed_files=[]
        )
        comment = render_pr_comment(results, self.ICON_MAPPINGS)
        expected_comment = self.__build_comment([
            '|Overall|%|Status|',
            '|:-|:-:|:-:|',
            '|Statement Coverage|60.0|:x:|',
            '',
            '|Changed File(s)|%|Status|',
            '|:-|:-:|:-:|',
            '',
            '|Package Coverage|%|Status|',
            '|:-|:-:|:-:|',
            '|com.app.pk1|70.0||',
            '|com.app.pk2|50.0||'
        ])
        self.assertEqual(comment.msg, expected_comment)

    def test_render_pr_comment_with_changed_files(self):
        results = ReportCoverage(
            overall=CoverageEntry('statement_coverage', 0.75, threshold=0.20, cov_type=CoverageType.OVERALL),
            packages=[
                CoverageEntry('com.app.pk1', 0.9, cov_type=CoverageType.PACKAGE),
                CoverageEntry('com.app.pk2', 0.6, cov_type=CoverageType.PACKAGE)
            ],
            changed_files=[
                CoverageEntry('File.scala - ClassX', 0.95, cov_type=CoverageType.CHANGED_FILE)
            ]
        )
        comment = render_pr_comment(results, self.ICON_MAPPINGS)
        expected_comment = self.__build_comment([
            '|Overall|%|Status|',
            '|:-|:-:|:-:|',
            '|Statement Coverage|75.0|:white_check_mark:|',
            '',
            '|Changed File(s)|%|Status|',
            '|:-|:-:|:-:|',
            '|File.scala - ClassX|95.0||',
            '',
            '|Package Coverage|%|Status|',
            '|:-|:-:|:-:|',
            '|com.app.pk1|90.0||',
            '|com.app.pk2|60.0||'
        ])
        self.assertEqual(comment.msg, expected_comment)

    def test_render_pr_comment_without_package_coverage(self):
        results = ReportCoverage(
            overall=CoverageEntry('statement_coverage', 0.75, threshold=0.20, cov_type=CoverageType.OVERALL),
            packages=[
                CoverageEntry('com.app.pk1', 0.9, cov_type=CoverageType.PACKAGE),
                CoverageEntry('com.app.pk2', 0.6, cov_type=CoverageType.PACKAGE)
            ],
            changed_files=[
                CoverageEntry('File.scala - ClassX', 0.95, cov_type=CoverageType.CHANGED_FILE)
            ]
        )
        comment = render_pr_comment(results, self.ICON_MAPPINGS, include_package_coverage=False)
        expected_comment = self.__build_comment([
            '|Overall|%|Status|',
            '|:-|:-:|:-:|',
            '|Statement Coverage|75.0|:white_check_mark:|',
            '',
            '|Changed File(s)|%|Status|',
            '|:-|:-:|:-:|',
            '|File.scala - ClassX|95.0||',
        ])
        self.assertEqual(comment.msg, expected_comment)

    @staticmethod
    def __build_comment(rows):
        return '\n'.join(rows)


if __name__ == '__main__':
    unittest.main()
