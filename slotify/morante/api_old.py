# from __future__ import annotations

# import re
# from urllib.parse import urljoin

# import requests

# PHOREST_ORIGIN = "https://www.phorest.com"


# class PhorestClient:
#     def __init__(self, salon_slug: str) -> None:
#         self.salon_slug = salon_slug
#         self.session = requests.Session()
#         self._configure_session()

#     def _configure_session(self) -> None:
#         headers = {
#             "User-Agent": "Mozilla/5.0",
#             "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
#         }

#         salon_page = f"{PHOREST_ORIGIN}/salon/{self.salon_slug}"
#         html = self.session.get(
#             salon_page,
#             headers=headers,
#             timeout=30,
#         )
#         html.raise_for_status()

#         # Find the current _app chunk (hash changes)
#         m = re.search(
#             r'src="([^"]+/_next/static/chunks/pages/_app-[^"]+\.js)"', html.text
#         )
#         if not m:
#             raise RuntimeError("Could not find _app chunk script URL in salon page HTML")

#         app_js_url = urljoin(PHOREST_ORIGIN, m.group(1))

#         js = self.session.get(app_js_url, headers=headers)
#         js.raise_for_status()

#         # Token appears in the bundle as: "xw":"<32 hex>"
#         m2 = re.search(r'"xw"\s*:\s*"([a-f0-9]{32})"', js.text)
#         if not m2:
#             raise RuntimeError('Could not find token in _app JS (pattern: "xw":"…")')

#         token = m2.group(1)
#         self.session.headers.update(
#             {
#                 "User-Agent": "Mozilla/5.0",
#                 "Accept": "application/vnd.phorest.me+json;version=1",
#                 "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
#                 "Origin": PHOREST_ORIGIN,
#                 "Referer": PHOREST_ORIGIN + "/",
#                 "Authorization": f'Token token="{token}"',
#             }
#         )

#     def get_businesses(self) -> dict[str, str]:
#         settings = self.session.get(
#             f"https://phorest.me/api/settings/salons/{self.salon_slug}"
#         ).json()
#         mem_business_id = settings["data"]["attributes"]["mem_business_id"]

#         business = self.session.get(
#             f"https://phorest.me/api/businesses/{mem_business_id}"
#         ).json()
#         return {b["domain_name"]: b["id"] for b in business["linked"]["branches"]}


# _client: PhorestClient | None = None


# def get_client(salon_slug: str = "moranterue1") -> PhorestClient:
#     global _client
#     if _client is None:
#         _client = PhorestClient(salon_slug)
#     return _client


# def get_businesses() -> dict[str, str]:
#     return get_client().get_businesses()
