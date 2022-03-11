from .models import CommentRow, Comment
from .models import CoverageType, ReportCoverage, CoverageEntry, CoverageSection, Table


def render_pr_comment(report_coverage: ReportCoverage, icon_mapping, include_package_coverage=True):
    overall_cov = report_coverage.overall
    packages_cov = report_coverage.packages
    changed_files_cov = report_coverage.changed_files

    # Overall coverage
    overall_comment_section = CoverageSection(
        visible=True,
        headers='|Overall|%|Status|',
        comment_rows=[
            CommentRow(
                name=__get_printable_name(overall_cov.name),
                value=overall_cov.result,
                icon=__get_icon(overall_cov, icon_mapping)
            )
        ]
    )

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
    package_section = CoverageSection(
        visible=include_package_coverage,
        headers='|Package Coverage|%|Status|',
        comment_rows=package_comment_rows
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
    changed_files_section = CoverageSection(
        visible=True,
        headers='|Changed File(s)|%|Status|',
        comment_rows=changed_files_comment_rows
    )

    comment = __gen_comment(
        overall_comment_section,
        package_section,
        changed_files_section
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


def __gen_table(section: CoverageSection):

    table_header = [
        section.headers,
        '|:-|:-:|:-:|'
    ]

    table_entries = []
    for entry in section.comment_rows:
        result_name = entry.name
        percentage_result = round(entry.value * 100, 1)
        formatted_result = int(percentage_result) if (1 <= percentage_result) else percentage_result
        result_icon = entry.icon
        table_entries.append(
            '|%s|%s|%s|' % (result_name, str(formatted_result), result_icon)
        )

    table_contents = table_header + table_entries
    table = Table(visible=section.visible, str_contents=table_contents)
    return table


def __gen_comment(
    overall_comment_section: CoverageSection,
    package_section: CoverageSection,
    changed_files_section: CoverageSection
):

    tables = [
        __gen_table(overall_comment_section),
        __gen_table(changed_files_section),
        __gen_table(package_section)
    ]

    visible_tables = [t for t in tables if t.visible]

    # Separate every table section with an empty row
    table_str = []
    for t in visible_tables:
        table_str += t.str_contents + ['']
    table_str = table_str[:-1]

    # Compose the entire string that makes up the final comment
    table_as_msg = '\n'.join(table_str)

    return Comment(table_as_msg)
