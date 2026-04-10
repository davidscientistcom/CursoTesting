from __future__ import annotations

from common import run_examples_from_cli

# --- EXAMPLE START: example_01_open_home ---
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_01_open_home() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("index.html"))
        title = driver.title
        heading = driver.find_element(By.TAG_NAME, "h1").text
        assert "Selenium Practice Lab" in title
        assert "romper menos" in heading
        return f"Página abierta: {title}"
# --- EXAMPLE END: example_01_open_home ---


# --- EXAMPLE START: example_02_find_by_id ---
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_02_find_by_id() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("index.html"))
        search_input = driver.find_element(By.ID, "global-search")
        search_input.clear()
        search_input.send_keys("esperas explícitas")
        driver.find_element(By.ID, "run-home-search").click()
        result = driver.find_element(By.ID, "home-search-result").text
        assert "esperas explícitas" in result
        return result
# --- EXAMPLE END: example_02_find_by_id ---


# --- EXAMPLE START: example_03_find_by_name ---
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_03_find_by_name() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("forms.html"))
        username = driver.find_element(By.NAME, "username")
        username.send_keys("lucentia")
        role = driver.find_element(By.NAME, "role")
        assert role.tag_name == "select"
        return f"Campo name localizado: {username.get_attribute('id')}"
# --- EXAMPLE END: example_03_find_by_name ---


# --- EXAMPLE START: example_04_find_by_css ---
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_04_find_by_css() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("forms.html"))
        cards = driver.find_elements(By.CSS_SELECTOR, ".selector-card")
        special = driver.find_element(By.CSS_SELECTOR, ".selector-card.special-card")
        assert len(cards) == 3
        assert "Selector card C" in special.text
        return f"Tarjetas selector-card: {len(cards)}"
# --- EXAMPLE END: example_04_find_by_css ---


# --- EXAMPLE START: example_05_find_by_xpath ---
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_05_find_by_xpath() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("waits.html"))
        button = driver.find_element(By.XPATH, "//button[normalize-space()='Cargar perfil tardío']")
        assert button.get_attribute("id") == "load-profile"
        return button.text
# --- EXAMPLE END: example_05_find_by_xpath ---


# --- EXAMPLE START: example_06_navigation_and_getters ---
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_06_navigation_and_getters() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("index.html"))
        driver.find_element(By.LINK_TEXT, "Formularios").click()
        assert driver.current_url.endswith("/lab/forms.html")
        assert "Formularios" in driver.title
        return f"Título: {driver.title} | URL: {driver.current_url}"
# --- EXAMPLE END: example_06_navigation_and_getters ---


EXAMPLES = {
    "example_01_open_home": example_01_open_home,
    "example_02_find_by_id": example_02_find_by_id,
    "example_03_find_by_name": example_03_find_by_name,
    "example_04_find_by_css": example_04_find_by_css,
    "example_05_find_by_xpath": example_05_find_by_xpath,
    "example_06_navigation_and_getters": example_06_navigation_and_getters,
}


if __name__ == "__main__":
    run_examples_from_cli(EXAMPLES)