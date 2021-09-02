import xml.etree.ElementTree as ElemTree
from .models import CoverageEntry, ReportCoverage


def process_report(report_file_name, threshold):

    OVERALL_COVERAGE_LABEL = 'statement_coverage'

    # Read report
    root = ElemTree.parse(report_file_name).getroot()

    # Statement coverage - overall
    statement_count = float(root.attrib['statement-count'])
    statements_invoked = float(root.attrib['statements-invoked'])
    statement_coverage = statements_invoked / statement_count
    overall_coverage = CoverageEntry(
        name=OVERALL_COVERAGE_LABEL,
        result=statement_coverage,
        is_package=False,
        threshold=threshold
    )

    # Statement coverage - per package
    coverage_per_package = []
    for package in root.findall('packages/package'):
        package_name = package.attrib['name']
        count = float(package.attrib['statement-count'])
        invoked = float(package.attrib['statements-invoked'])
        cov = invoked / count
        result = CoverageEntry(package_name, cov, is_package=True)
        coverage_per_package.append(result)

    return ReportCoverage(
        overall=overall_coverage,
        packages=coverage_per_package
    )
