import re
from functools import lru_cache
from typing import Any, Final, Optional
from urllib.parse import urljoin

import requests

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


def call_api(url: str, params: Optional[dict[str, Any]] = None) -> Any:
    s = get_session()
    response = s.get(url, params=params)

    if response.status_code == 401:
        configure_session(s)
        response = s.get(url, params=params)

    response.raise_for_status()
    return response.json()


def get_businesses() -> dict[str, str]:
    settings = call_api(f"{API_URL}/settings/salons/{SALON_SLUG}")
    mem_business_id = settings["data"]["attributes"]["mem_business_id"]

    business = call_api(f"{API_URL}/businesses/{mem_business_id}")
    branches = business["linked"]["branches"]

    return {b["domain_name"]: b["id"] for b in branches}


def get_staffs(salon_slug: str) -> dict[str, Any]:
    staffs = call_api(
        f"https://{salon_slug}.phorest.me/api/staffs", params={"order": "+internet_pos"}
    )
    return {
        s["first_name"]: {
            "id": s["id"],
            "disqualified_service_ids": set(s["disqualified_service_ids"]),
        }
        for s in staffs["staffs"]
        if not s["hide_from_online_bookings"]
    }


def get_services(salon_slug: str) -> Any:
    services = call_api(f"https://{salon_slug}.phorest.me/api/services")
    return {s["id"]: s["name"] for s in services["services"]}


if __name__ == "__main__":
    staff = get_staffs("moranterue1")["Leandro"]
    services = get_services("moranterue1")
    print(len(services))
    services = set(services.keys()) - staff["disqualified_service_ids"]
    print(len(services))
