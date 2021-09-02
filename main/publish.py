from github import Github


def publish_comment(access_token, repo_name, issue_number, comment):

    g = Github(access_token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(issue_number)
    pr.create_issue_comment(comment.msg)
