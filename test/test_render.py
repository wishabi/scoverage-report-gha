import unittest
from .config import config
from main.models import ReportCoverage, CoverageEntry
from main.render import render_pr_comment


class TestRender(unittest.TestCase):

    ICON_MAPPINGS = config['render']['icon_mappings']

    def test_render_pr_comment_pass_threshold(self):
        results = ReportCoverage(
            overall=CoverageEntry('statement_coverage', 0.75, threshold=0.20, is_package=False),
            packages=[
                CoverageEntry('com.app.pk1', 0.9, is_package=True),
                CoverageEntry('com.app.pk2', 0.6, is_package=True)
            ]
        )
        comment = render_pr_comment(results, self.ICON_MAPPINGS)
        expected_comment = self.__build_comment([
            '|Overall|%|Status|',
            '|:-|:-:|:-:|',
            '|Statement Coverage|75.0|:white_check_mark:|',
            '',
            '|Package Coverage|%|Status|',
            '|:-|:-:|:-:|',
            '|com.app.pk1|90.0||',
            '|com.app.pk2|60.0||'
        ])
        self.assertEqual(comment.msg, expected_comment)

    def test_render_pr_comment_fail_threshold(self):
        results = ReportCoverage(
            overall=CoverageEntry('statement_coverage', 0.60, threshold=0.90, is_package=False),
            packages=[
                CoverageEntry('com.app.pk1', 0.7, is_package=True),
                CoverageEntry('com.app.pk2', 0.5, is_package=True)
            ]
        )
        comment = render_pr_comment(results, self.ICON_MAPPINGS)
        expected_comment = self.__build_comment([
            '|Overall|%|Status|',
            '|:-|:-:|:-:|',
            '|Statement Coverage|60.0|:x:|',
            '',
            '|Package Coverage|%|Status|',
            '|:-|:-:|:-:|',
            '|com.app.pk1|70.0||',
            '|com.app.pk2|50.0||'
        ])
        self.assertEqual(comment.msg, expected_comment)

    @staticmethod
    def __build_comment(rows):
        return '\n'.join(rows)


if __name__ == '__main__':
    unittest.main()
