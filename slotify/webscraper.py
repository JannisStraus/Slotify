import platform
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


def search_slot() -> str:
    url = (
        "https://www.phorest.com/salon/moranterue1"
        "/book/service-selection?showSpecialOffers=false"
    )
    elements: list[WebElement | tuple[str, str]] = [
        (By.CSS_SELECTOR, "#onetrust-close-btn-container"),
        (
            By.XPATH,
            "//button[@data-testid='serviceCategory' and .//div[text()='Herren Schneiden + Styling']]",
        ),
        (
            By.XPATH,
            "//div[@data-testid='serviceItem' and .//div[text()='Schnitt - Herren']]",
        ),
        (By.XPATH, "//div[@data-testid='staffMembersTab' and .//div[text()='Team']]"),
        (
            By.XPATH,
            "//div[@data-testid='staffMemberButton_k6L11Ok7Os-Xf8S8MpwtAg' and .//div[text()='Leandro']]",
        ),
        (By.XPATH, "//button[@data-testid='bookButton']"),
    ]
    out_element = (By.XPATH, "//div[@data-testid='availabilityAgenda']")
    return firefox(url, elements, out_element)


def firefox(
    url: str,
    elements: list[WebElement | tuple[str, str]],
    out_element: WebElement | tuple[str, str],
    *,
    remote_url: str = "http://localhost:4444/wd/hub",  # TODO
) -> str:
    options = Options()
    options.add_argument("--headless")
    service = None
    if platform.system() not in {"Windows", "Darwin"}:
        options.binary_location = "usr/bin/firefox"
        service = Service("usr/local/bin/geckodriver")

    with webdriver.Firefox(options=options, service=service) as drv:
        drv.get(url)
        for mark in elements:
            btn = WebDriverWait(drv, 10).until(EC.element_to_be_clickable(mark))
            _ = btn.location_once_scrolled_into_view
            time.sleep(0.5)
            btn.click()
        html = WebDriverWait(drv, 10).until(EC.presence_of_element_located(out_element))
        time.sleep(0.5)
        inner_html = html.get_attribute("innerHTML")
        if not inner_html:
            raise LookupError()
        return str(inner_html)
