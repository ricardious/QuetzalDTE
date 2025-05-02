from datetime import datetime


def parse_date(date_str: str, fmt: str = "%d/%m/%Y"):
    try:
        return datetime.strptime(date_str, fmt)
    except ValueError:
        return None


def format_date(date_obj: datetime, fmt: str = "%d/%m/%Y") -> str:
    return date_obj.strftime(fmt)


def is_date_in_range(
    date_str: str, start_str: str, end_str: str, fmt: str = "%d/%m/%Y"
) -> bool:
    date = parse_date(date_str, fmt)
    start = parse_date(start_str, fmt)
    end = parse_date(end_str, fmt)
    if None in (date, start, end):
        return False
    return start <= date <= end
