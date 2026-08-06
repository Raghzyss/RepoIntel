import re


def is_valid_github_url(url: str) -> bool:
    """
    Checks whether the provided URL is a valid GitHub repository URL.
    """

    pattern = r"^https://github\.com/[\w.-]+/[\w.-]+/?$"

    return bool(re.match(pattern, url))