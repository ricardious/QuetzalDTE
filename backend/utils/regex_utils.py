import re


def extract_date(timestamp: str) -> str | None:
    m = re.search(r"\d{1,2}/\d{1,2}/\d{4}", timestamp)
    return m.group(0) if m else None


def extract_time(timestamp: str) -> str | None:
    m = re.search(r"\d{1,2}:\d{2}", timestamp)
    return m.group(0) if m else None
