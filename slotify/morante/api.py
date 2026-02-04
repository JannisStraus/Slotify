import os
import re
from collections import defaultdict
from functools import lru_cache
from typing import Any, Final
from urllib.parse import urljoin

import requests

from slotify.morante.parser import cached_slots, days_to_datetime, utc_to_local

API_URL: Final = "https://www.phorest.me/api"
PHOREST_ORIGIN: Final = "https://www.phorest.com"
SALON_SLUG: Final = "moranterue1"
HEADERS: Final[dict[str, str]] = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.phorest.me+json;version=1",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "Origin": PHOREST_ORIGIN,
    "Referer": f"{PHOREST_ORIGIN}/",
}


@lru_cache(maxsize=1)
def get_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(HEADERS)
    return s


def configure_session(session: requests.Session) -> None:
    salon_page = f"{PHOREST_ORIGIN}/salon/{SALON_SLUG}"
    response = session.get(salon_page, headers=HEADERS)
    response.raise_for_status()

    # Find the current _app chunk (hash changes)
    # Looks for: src="/_next/static/chunks/pages/_app-12345abcde.js"
    match_app_js = re.search(
        r'src="([^"]+/_next/static/chunks/pages/_app-[^"]+\.js)"', response.text
    )
    if not match_app_js:
        raise RuntimeError("Could not find _app chunk script URL in salon page HTML")

    app_js_url = urljoin(PHOREST_ORIGIN, match_app_js.group(1))

    js_response = session.get(app_js_url, headers=HEADERS)
    js_response.raise_for_status()

    # Token appears in the bundle as: "xw":"<32 hex>"
    match_token = re.search(r'"xw"\s*:\s*"([a-f0-9]{32})"', js_response.text)
    if not match_token:
        raise RuntimeError('Could not find token in _app JS (pattern: "xw":"…")')

    token = match_token.group(1)

    # Update session headers with the new token
    session.headers.update(
        {
            "Authorization": f'Token token="{token}"',
        }
    )


def api_get(url: str, params: dict[str, Any] | None = None) -> Any:
    s = get_session()
    response = s.get(url, params=params)

    if response.status_code == 401:
        configure_session(s)
        response = s.get(url, params=params)

    response.raise_for_status()
    return response.json()


def api_post(url: str, payload: dict[str, Any] | None = None) -> Any:
    s = get_session()
    response = s.post(url, json=payload)

    if response.status_code == 401:
        configure_session(s)
        response = s.post(url, json=payload)

    response.raise_for_status()
    return response.json()


def get_businesses() -> dict[str, str]:
    settings = api_get(f"{API_URL}/settings/salons/{SALON_SLUG}")
    mem_business_id = settings["data"]["attributes"]["mem_business_id"]

    branches = api_get(f"{API_URL}/businesses/{mem_business_id}")["linked"]["branches"]

    return {b["address"]["street_address_1"]: b["domain_name"] for b in branches}


def get_staffs(salon_slug: str) -> dict[str, Any]:
    staffs = api_get(
        f"https://{salon_slug}.phorest.me/api/staffs", params={"order": "+internet_pos"}
    )["staffs"]
    return {
        s["first_name"]: {
            "id": s["id"],
            "disqualified_service_ids": set(s["disqualified_service_ids"]),
        }
        for s in staffs
        if not s["hide_from_online_bookings"]
    }


def get_services(
    salon_slug: str, staff: dict[str, Any] | None = None
) -> dict[str, str]:
    services = api_get(f"https://{salon_slug}.phorest.me/api/services")
    if staff is None:
        return {s["name"]: s["id"] for s in services["services"]}
    ignore = staff["disqualified_service_ids"]
    return {s["name"]: s["id"] for s in services["services"] if s["id"] not in ignore}


def get_slots(
    salon_slug: str, staff_id: str, service_id: str, days: int
) -> dict[str, list[str]]:
    start_time, end_time = days_to_datetime(days)
    payload = {
        "availability_requests": {
            "start_time": start_time,
            "end_time": end_time,
            "client_service_selections": [
                {
                    "client_id": "guest_0",
                    "service_selections": [
                        {
                            "service_id": service_id,
                            "staff_id": staff_id,
                        }
                    ],
                }
            ],
        }
    }
    slots = api_post(
        f"https://{salon_slug}.phorest.me/api/availability_requests", payload
    )
    slots_avail = defaultdict(list)
    for slot in slots["availability_slots"]:
        for client_schedule in slot["client_schedules"]:
            for sched in client_schedule["service_schedules"]:
                if sched["alternative_staff_member"]:
                    continue
                date_str, time_str = utc_to_local(sched["start_time"])
                slots_avail[date_str].append(time_str)
    return slots_avail


def choose(title: str, options: dict[str, Any]) -> Any:
    keys = list(options.keys())

    print(f"\n{title}")
    for i, key in enumerate(keys, start=1):
        print(f"  {i}. {key}")

    while True:
        choice = input("Choose number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(keys):
            return options[keys[int(choice) - 1]]
        print("Invalid choice, try again.")


def get_markdown(days: int) -> str | None:
    # Salon
    salon_slug = os.getenv("MORANTE_SALON_SLUG")
    if not salon_slug:
        businesses = get_businesses()
        salon_slug = choose("Choose salon", businesses)
        os.environ["MORANTE_SALON_SLUG"] = salon_slug

    # Staff
    staff_id = os.getenv("MORANTE_STAFF_ID")
    service_id = os.getenv("MORANTE_SERVICE_ID")
    if not staff_id or not service_id:
        staffs = get_staffs(salon_slug)
        staff = choose("Choose staff", staffs)
        staff_id = staff["id"]
        print(staff_id)
        os.environ["MORANTE_STAFF_ID"] = staff_id

        services = get_services(salon_slug, staff)
        service_id = choose("Choose service", services)
        print(service_id)
        os.environ["MORANTE_SERVICE_ID"] = service_id

    slots = get_slots(salon_slug, staff_id, service_id, days)
    return cached_slots(slots)
