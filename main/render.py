def render_pr_comment(results, icon_mapping, thresholds=None):
    comment_entries = []
    for k, v in results.items():
        result_name = k if (__is_package(k)) else k.title().replace("_", " ")
        result_value = v
        threshold = thresholds[k] if (thresholds is not None and k in thresholds) else None
        result_icon = icon_mapping['na'] if (__is_package(k)) else __get_icon(v, threshold, icon_mapping)
        comment_entries.append(
            {
                'result_name': result_name,
                'result_value': result_value,
                'result_icon': result_icon
            }
        )
    comment = __gen_comment(comment_entries)

    return comment


def __is_package(category):
    package_prefix = "com."
    return str(category).startswith(package_prefix)


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
