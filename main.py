import os
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


def main(repo_name, pr_number, token, report_name, min_statement_coverage, changed_files):

    icon_mappings = config['render']['icon_mappings']
    threshold = __valid_threshold(min_statement_coverage)
    report_coverage = process_report(report_name, threshold, changed_files)
    comment = render_pr_comment(report_coverage, icon_mappings)
    publish_comment(token, repo_name, pr_number, comment)

    # Output results for Github Actions
    print(f"::set-output name=statementCoverage::{report_coverage.overall.result}")


if __name__ == "__main__":

    repo = os.environ["INPUT_REPO"]
    issue_number = int(os.environ["INPUT_PR"])
    access_token = os.environ["INPUT_TOKEN"]
    report_file_name = os.environ["INPUT_FILE"]
    min_stmt_cov = os.environ["INPUT_MINSTATEMENTCOV"]
    changed_fs = os.environ["INPUT_CHANGEDFILES"]

    main(repo, issue_number, access_token, report_file_name, min_stmt_cov, changed_fs)
