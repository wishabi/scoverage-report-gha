from .models import CommentRow, Comment
from .models import CoverageType, ReportCoverage, CoverageEntry


def render_pr_comment(report_coverage: ReportCoverage, icon_mapping):
    overall_cov = report_coverage.overall
    packages_cov = report_coverage.packages
    changed_files_cov = report_coverage.changed_files

    # Overall coverage
    overall_comment_rows = [
        CommentRow(
            name=__get_printable_name(overall_cov.name),
            value=overall_cov.result,
            icon=__get_icon(overall_cov, icon_mapping)
        )
    ]

    # Per package coverage
    package_comment_rows = []
    for pkg in packages_cov:
        package_comment_rows.append(
            CommentRow(
                name=pkg.name,
                value=pkg.result,
                icon=__get_icon(pkg, icon_mapping)
            )
        )

    # Coverage for changed files (if applicable)
    changed_files_comment_rows = []
    for file_cov in changed_files_cov:
        changed_files_comment_rows.append(
            CommentRow(
                name=file_cov.name,
                value=file_cov.result,
                icon=__get_icon(file_cov, icon_mapping)
            )
        )

    comment = __gen_comment(
        overall_comment_rows,
        package_comment_rows,
        changed_files_comment_rows
    )

    return comment


def __get_printable_name(coverage_entry_name):
    return coverage_entry_name.title().replace("_", " ")


def __get_icon(coverage_entry: CoverageEntry, icon_mapping):
    result_icon = ""
    if coverage_entry.cov_type in (CoverageType.PACKAGE, CoverageType.CHANGED_FILE):
        result_icon = icon_mapping['na']
    elif coverage_entry.threshold is None:
        result_icon = icon_mapping['unknown']
    else:
        result_icon = icon_mapping['failed'] if (coverage_entry.result < coverage_entry.threshold) else icon_mapping['passed']
    return result_icon


def __gen_table(coverage_entries, table_type):

    table_headers = {
        'overall': '|Overall|%|Status|',
        'package': '|Package Coverage|%|Status|',
        'changed_files': '|Changed File(s)|%|Status|'
    }

    table_header = [
        table_headers[table_type],
        '|:-|:-:|:-:|'
    ]

    table_entries = []
    for entry in coverage_entries:
        result_name = entry.name
        formatted_result = round(entry.value * 100, 2)
        result_icon = entry.icon
        table_entries.append(
            '|%s|%s|%s|' % (result_name, str(formatted_result), result_icon)
        )

    table = table_header + table_entries
    return table


def __gen_comment(overall_comment_rows, package_comment_rows, changed_files_comment_rows):

    overall_table = __gen_table(overall_comment_rows, 'overall')
    changed_files_table = __gen_table(changed_files_comment_rows, 'changed_files')
    package_table = __gen_table(package_comment_rows, 'package')

    entire_table = overall_table + [''] + changed_files_table + [''] + package_table
    table = '\n'.join(entire_table)
    return Comment(table)
