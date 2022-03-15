
config = {
    'render': {
        # Internal mappings for markdown formatted icons/emojis
        "icon_mappings": {
            'passed': ':white_check_mark:',     # Had equal/higher coverage than threshold
            'failed': ':x:',                    # Had lower coverage than threshold
            'unknown': 'unknown',
            'na': ''                            # Don't want to include an icon
        },

        # Icons used to decorate individual coverage results (file, packages, etc).
        "coverage_score_mappings": {
            'good': ':green_circle:',
            'ok': ':yellow_circle:',
            'poor': ':red_circle:',
            'na': ':question:'
        }
    }
}