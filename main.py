import os
import json
from distutils.util import strtobool
from main.process import process_report
from main.render import render_pr_comment
from main.publish import publish_comment
from main.config import config


def __valid_threshold(threshold):
    th = None
    if threshold is None:
        th = threshold
    else:
        try:
            float(threshold)
        except ValueError:
            print("Value of `threshold` is not a float: %s" % str(threshold))
            exit(1)
        th = float(threshold)
        if th < 0 or th > 1:
            print("Value of `threshold` must be between 0 and 1, but was: %s" % str(threshold))
            exit(1)
    return th


def parse_changed_files(changed_files_str):
    return json.loads(changed_files_str)


def main(repo_name, pr_number, token, report_name, min_statement_coverage, changed_files_str, include_package_coverage):

    icon_mappings = config['render']['icon_mappings']
    changed_files = parse_changed_files(changed_files_str)
    threshold = __valid_threshold(min_statement_coverage)
    report_coverage = process_report(report_name, threshold, changed_files)
    comment = render_pr_comment(report_coverage, icon_mappings, include_package_coverage)
    publish_comment(token, repo_name, pr_number, comment)

    # Output results for Github Actions
    print(f"::set-output name=statementCoverage::{report_coverage.overall.result}")


if __name__ == "__main__":

    repo = os.environ["INPUT_REPO"]
    issue_number = int(os.environ["INPUT_PR"])
    access_token = os.environ["INPUT_TOKEN"]
    report_file_name = os.environ["INPUT_FILE"]
    min_stmt_cov = os.environ["INPUT_MINSTATEMENTCOV"]
    changed_fs_str = os.environ["INPUT_CHANGEDFILES"]
    include_package_cov = bool(strtobool(os.environ["INPUT_INCLUDEPACKAGECOV"]))

    main(repo, issue_number, access_token, report_file_name, min_stmt_cov, changed_fs_str, include_package_cov)
