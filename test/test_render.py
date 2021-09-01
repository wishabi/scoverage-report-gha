import unittest
import os
from main.render import render_pr_comment
from .config import config


class TestProcess(unittest.TestCase):
    TEST_COVERAGE_FILE = os.path.join(os.path.dirname(__file__),
                                      'resources',
                                      'scoverage.xml')

    ICON_MAPPINGS = config['render']['icon_mappings']

    def test_render_pr_comment_pass_threshold(self):
        results = {
            'statement_coverage': 0.75,
            'com.app.pk1': 0.9,
            'com.app.pk2': 0.6
        }
        thresholds = {
            'statement_coverage': 0.20
        }
        comment = render_pr_comment(results, self.ICON_MAPPINGS, thresholds)
        expected_comment = self.__build_comment([
            '|Code Coverage|%|Status|',
            '|:-|:-:|:-:|',
            '|Statement Coverage|75.0|:white_check_mark:|',
            '|com.app.pk1|90.0||',
            '|com.app.pk2|60.0||'
        ])
        self.assertEqual(comment, expected_comment)

    def test_render_pr_comment_fail_threshold(self):
        results = {
            'statement_coverage': 0.60,
            'com.app.pk1': 0.7,
            'com.app.pk2': 0.5
        }
        thresholds = {
            'statement_coverage': 0.90
        }
        comment = render_pr_comment(results, self.ICON_MAPPINGS, thresholds)
        expected_comment = self.__build_comment([
            '|Code Coverage|%|Status|',
            '|:-|:-:|:-:|',
            '|Statement Coverage|60.0|:x:|',
            '|com.app.pk1|70.0||',
            '|com.app.pk2|50.0||'
        ])
        self.assertEqual(comment, expected_comment)

    @staticmethod
    def __build_comment(rows):
        return '\n'.join(rows)


if __name__ == '__main__':
    unittest.main()
