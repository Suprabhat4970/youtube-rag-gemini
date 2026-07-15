import re


def extract_video_id(url):
    """
    Extract YouTube video ID from URL
    """

    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"

    match = re.search(pattern, url)

    if match:
        return match.group(1)

    return None


def truncate_text(text, max_chars=15000):

    if len(text) <= max_chars:
        return text

    return text[:max_chars]