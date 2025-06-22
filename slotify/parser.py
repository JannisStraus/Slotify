from datetime import date

from bs4 import BeautifulSoup


def next_date(day: int, today: date) -> date:
    month, year = today.month, today.year
    if day <= today.day:
        # move to next month (and roll year if needed)
        month += 1
        if month == 13:
            month, year = 1, year + 1
    return date(year, month, day)


def parse_agenda(html: str, next_days: int | None = None) -> dict[str, list[str]]:
    soup = BeautifulSoup(html, "html.parser")
    result: dict[str, list[str]] = {}
    today = date.today()

    for day in soup.select('div[data-testid="agendaDay"]'):
        # --- headline (date number + weekday abbreviation)
        header = day.select_one('div[data-testid="day"]')
        number = int(header.select_one("span").text)
        cur_date = next_date(number, today)
        # weekday = str(header.select("span")[1].text).strip()

        if next_days is not None and (cur_date - today).days > next_days:
            continue
        if day.select_one('[data-testid="unavailableItem"]'):
            slots = []
        else:
            slots = [
                str(span.text).strip()
                for span in day.select('span[data-testid="branchTime"]')
            ]
        if slots:
            result[cur_date.strftime("%d.%m.%Y")] = slots
    return result
