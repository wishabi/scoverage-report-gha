import xml.etree.ElementTree as ElemTree
from typing import List
from .models import CoverageType, CoverageEntry, ReportCoverage


def process_report(report_file_name, threshold, changed_files=[]):
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
        cov_type=CoverageType.OVERALL,
        threshold=threshold
    )

    # Statement coverage - per package
    coverage_per_package = []
    for package in root.findall('packages/package'):
        package_name = package.attrib['name']
        count = float(package.attrib['statement-count'])
        invoked = float(package.attrib['statements-invoked'])
        cov = invoked / count
        result = CoverageEntry(package_name, cov, cov_type=CoverageType.PACKAGE)
        coverage_per_package.append(result)

    # Changed files
    coverage_per_changed_file = __process_changed_files(root, changed_files)

    return ReportCoverage(
        overall=overall_coverage,
        packages=coverage_per_package,
        changed_files=coverage_per_changed_file
    )


def __process_changed_files(report_root, changed_files: List[str]):
    coverage_per_file = []
    # In Scala, multiple classes/objects can co-exist in the same file.
    # So to keep track of unique entries we concatenate file name with class/object name.
    # This "unique" identity is referred to as a key in the code below.
    keys_found = []
    for package in report_root.findall('packages/package'):
        for class_entry in package.findall('classes/class'):
            file_name = class_entry.attrib['filename']
            # Changed files not found in the coverage report wont be analyzed, as expected.
            match = [f for f in changed_files if f.endswith(file_name)]
            if len(match) > 0:
                class_name = class_entry.attrib['name']
                key = '-'.join([file_name, class_name])
                if key not in keys_found:
                    keys_found.append(key)
                    entry_name = ' - '.join([
                        file_name.split('/')[-1],
                        class_name.split('.')[-1]
                    ])
                    count = float(class_entry.attrib['statement-count'])
                    invoked = float(class_entry.attrib['statements-invoked'])
                    cov = invoked / count
                    result = CoverageEntry(entry_name, cov, cov_type=CoverageType.CHANGED_FILE)
                    coverage_per_file.append(result)

    return coverage_per_file
