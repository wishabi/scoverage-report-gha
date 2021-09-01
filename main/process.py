import xml.etree.ElementTree as ElemTree


def process_report(report_file_name):

    results = {}

    # Read report
    root = ElemTree.parse(report_file_name).getroot()

    # Statement coverage - overall
    statement_count = float(root.attrib['statement-count'])
    statements_invoked = float(root.attrib['statements-invoked'])
    statement_coverage = statements_invoked / statement_count
    results['statement_coverage'] = statement_coverage

    # Statement coverage - per package
    for package in root.findall('packages/package'):
        package_name = package.attrib['name']
        count = float(package.attrib['statement-count'])
        invoked = float(package.attrib['statements-invoked'])
        cov = invoked / count
        results[package_name] = cov

    return results
