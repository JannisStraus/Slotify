from datetime import datetime


def parse_date(date: str) -> str:
    if "." in date:
        dt = datetime.strptime(date, "%d.%m.%Y")
    else:
        dt = datetime.strptime(date, "%Y-%m-%d")
    return dt.strftime("%Y-%m-%d")
