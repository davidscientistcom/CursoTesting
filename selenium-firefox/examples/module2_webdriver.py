from __future__ import annotations

from common import run_examples_from_cli

# --- EXAMPLE START: example_07_firefox_setup_and_url_assert ---
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_07_firefox_setup_and_url_assert() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("windows.html"))
        assert driver.current_url.endswith("/lab/windows.html")
        assert driver.find_element(By.ID, "show-alert").is_displayed()
        return driver.current_url
# --- EXAMPLE END: example_07_firefox_setup_and_url_assert ---


# --- EXAMPLE START: example_08_find_elements_and_iteration ---
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_08_find_elements_and_iteration() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("forms.html"))
        cards = driver.find_elements(By.CLASS_NAME, "selector-card")
        titles = [card.find_element(By.TAG_NAME, "h3").text for card in cards]
        assert titles == ["Selector card A", "Selector card B", "Selector card C"]
        return ", ".join(titles)
# --- EXAMPLE END: example_08_find_elements_and_iteration ---


# --- EXAMPLE START: example_09_basic_form_submit ---
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_09_basic_form_submit() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("forms.html"))
        driver.find_element(By.ID, "username").send_keys("curso_selenium")
        driver.find_element(By.ID, "password").send_keys("super-secreto")
        driver.find_element(By.ID, "submit-form").click()
        username = driver.find_element(By.ID, "result-username").text
        assert username == "curso_selenium"
        return username
# --- EXAMPLE END: example_09_basic_form_submit ---


# --- EXAMPLE START: example_10_select_dropdown_and_radio ---
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from common import firefox_driver, lab_url


def example_10_select_dropdown_and_radio() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("forms.html"))
        Select(driver.find_element(By.ID, "role-select")).select_by_value("lead")
        Select(driver.find_element(By.ID, "country-select")).select_by_value("mx")
        driver.find_element(By.ID, "plan-enterprise").click()
        driver.find_element(By.ID, "accept-terms").click()
        driver.find_element(By.ID, "submit-form").click()
        role = driver.find_element(By.ID, "result-role").text
        plan = driver.find_element(By.ID, "result-plan").text
        terms = driver.find_element(By.ID, "result-terms").text
        assert role == "lead"
        assert plan == "enterprise"
        assert terms == "aceptados"
        return f"Rol={role} | Plan={plan}"
# --- EXAMPLE END: example_10_select_dropdown_and_radio ---


# --- EXAMPLE START: example_11_handle_nosuch_element ---
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_11_handle_nosuch_element() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("forms.html"))
        try:
            driver.find_element(By.ID, "elemento-que-no-existe")
        except NoSuchElementException:
            return "NoSuchElementException capturada correctamente"
        raise AssertionError("La excepción no se produjo")
# --- EXAMPLE END: example_11_handle_nosuch_element ---


# --- EXAMPLE START: example_12_safe_try_except_finally ---
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common import build_driver, lab_url, wait


def example_12_safe_try_except_finally() -> str:
    driver = build_driver()
    outcome = "sin resultado"
    try:
        driver.get(lab_url("waits.html"))
        wait(driver, 1).until(EC.visibility_of_element_located((By.ID, "missing-node")))
    except TimeoutException:
        outcome = "TimeoutException capturada"
    except Exception as exc:
        outcome = f"Excepción genérica capturada: {exc.__class__.__name__}"
    finally:
        driver.quit()
    return outcome
# --- EXAMPLE END: example_12_safe_try_except_finally ---


EXAMPLES = {
    "example_07_firefox_setup_and_url_assert": example_07_firefox_setup_and_url_assert,
    "example_08_find_elements_and_iteration": example_08_find_elements_and_iteration,
    "example_09_basic_form_submit": example_09_basic_form_submit,
    "example_10_select_dropdown_and_radio": example_10_select_dropdown_and_radio,
    "example_11_handle_nosuch_element": example_11_handle_nosuch_element,
    "example_12_safe_try_except_finally": example_12_safe_try_except_finally,
}


if __name__ == "__main__":
    run_examples_from_cli(EXAMPLES)