import os
import xml.etree.ElementTree as ElemTree
from github import Github


def __render_pr_comment(results, thresholds=None):

    icon_mapping = {
        'passed': ':white_check_mark:',
        'failed': ':x:',
        'unknown': 'unknown'
    }

    comment_entries = []
    for k, v in results.items():
        result_name = k.title().replace("_", " ")
        result_value = v
        threshold = thresholds[k] if (thresholds is not None and k in thresholds) else None
        result_icon = __get_icon(v, threshold, icon_mapping)
        comment_entries.append(
            {
                'result_name': result_name,
                'result_value': result_value,
                'result_icon': result_icon
            }
        )
    comment = __gen_comment(comment_entries)

    return comment


def __get_icon(result_value, threshold, icon_mapping):
    result_icon = ""
    if threshold is None:
        result_icon = icon_mapping['unknown']
    else:
        result_icon = icon_mapping['failed'] if (result_value < threshold) else icon_mapping['passed']
    return result_icon


def __gen_comment(comment_entries):

    table_entries = [
        '|Code Coverage|%|Status|',
        '|:-|:-:|:-:|'
    ]

    for entry in comment_entries:
        result_name = entry['result_name']
        formatted_result = round(entry['result_value'] * 100, 2)
        result_icon = entry['result_icon']
        table_entries.append(
            '|%s|%s|%s|' % (result_name, str(formatted_result), result_icon)
        )

    table = '\n'.join(table_entries)
    return table


def __process_report(report_file_name):

    # Read report
    root = ElemTree.parse(report_file_name).getroot()

    # Process
    statement_count = float(root.attrib['statement-count'])
    statements_invoked = float(root.attrib['statements-invoked'])
    statement_coverage = statements_invoked / statement_count
    results = {
        'statement_coverage': statement_coverage
    }

    return results


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


def main(repo_name, issue_number, access_token, report_name, min_statement_coverage):

    thresholds = {
        'statement_coverage': __valid_threshold(min_statement_coverage)
    }
    results = __process_report(report_name)
    comment = __render_pr_comment(results, thresholds)

    # Write comment to PR
    g = Github(access_token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(issue_number)
    pr.create_issue_comment(comment)

    # Output results
    print(f"::set-output name=statementCoverage::{results['statement_coverage']}")


if __name__ == "__main__":

    repo = os.environ["INPUT_REPO"]
    issue_number = int(os.environ["INPUT_PR"])
    access_token = os.environ["INPUT_TOKEN"]
    report_file_name = os.environ["INPUT_FILE"]
    min_stmt_cov = os.environ["INPUT_MINSTATEMENTCOV"]

    main(repo, issue_number, access_token, report_file_name, min_stmt_cov)
