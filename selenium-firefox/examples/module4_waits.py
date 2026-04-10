from __future__ import annotations

from common import run_examples_from_cli

# --- EXAMPLE START: example_24_wait_fail_demo ---
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_24_wait_fail_demo() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("waits.html"))
        driver.find_element(By.ID, "load-profile").click()
        try:
            driver.find_element(By.ID, "delayed-profile")
        except NoSuchElementException:
            return "Fallo esperado sin espera explícita"
        raise AssertionError("El ejemplo debía fallar antes de que el DOM terminara de cargar")
# --- EXAMPLE END: example_24_wait_fail_demo ---


# --- EXAMPLE START: example_25_explicit_wait_fix ---
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common import firefox_driver, lab_url, wait


def example_25_explicit_wait_fix() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("waits.html"))
        driver.find_element(By.ID, "load-profile").click()
        profile = wait(driver, 4).until(EC.visibility_of_element_located((By.ID, "delayed-profile")))
        assert "Perfil tardío" in profile.text
        return profile.text
# --- EXAMPLE END: example_25_explicit_wait_fix ---


# --- EXAMPLE START: example_26_implicit_wait_example ---
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_26_implicit_wait_example() -> str:
    with firefox_driver(implicit_wait=3) as driver:
        driver.get(lab_url("waits.html"))
        driver.find_element(By.ID, "load-profile").click()
        profile = driver.find_element(By.ID, "delayed-profile")
        assert "espera explícita" in profile.text
        return profile.text
# --- EXAMPLE END: example_26_implicit_wait_example ---


# --- EXAMPLE START: example_27_wait_until_button_enabled ---
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common import firefox_driver, lab_url, wait


def example_27_wait_until_button_enabled() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("waits.html"))
        button = wait(driver, 4).until(EC.element_to_be_clickable((By.ID, "unlock-button")))
        button.click()
        status = driver.find_element(By.ID, "unlock-status").text
        assert status == "Botón habilitado"
        return status
# --- EXAMPLE END: example_27_wait_until_button_enabled ---


# --- EXAMPLE START: example_28_wait_for_async_results ---
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common import firefox_driver, lab_url, wait


def example_28_wait_for_async_results() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("waits.html"))
        driver.find_element(By.ID, "run-async-search").click()
        wait(driver, 4).until(EC.visibility_of_element_located((By.ID, "result-list")))
        results = driver.find_elements(By.CLASS_NAME, "result-item")
        assert len(results) == 3
        return f"Resultados visibles: {len(results)}"
# --- EXAMPLE END: example_28_wait_for_async_results ---


# --- EXAMPLE START: example_29_wait_for_toast_appear_and_disappear ---
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common import firefox_driver, lab_url, wait


def example_29_wait_for_toast_appear_and_disappear() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("waits.html"))
        driver.find_element(By.ID, "trigger-toast").click()
        wait(driver, 4).until(EC.visibility_of_element_located((By.ID, "sync-toast")))
        wait(driver, 4).until(EC.invisibility_of_element_located((By.ID, "sync-toast")))
        status = driver.find_element(By.ID, "toast-status").text
        assert status == "Toast oculto"
        return status
# --- EXAMPLE END: example_29_wait_for_toast_appear_and_disappear ---


# --- EXAMPLE START: example_30_wait_for_table_rows ---
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common import firefox_driver, lab_url, wait


def example_30_wait_for_table_rows() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("waits.html"))
        driver.find_element(By.ID, "load-orders").click()
        wait(driver, 4).until(EC.text_to_be_present_in_element((By.ID, "orders-status"), "Pedidos cargados"))
        rows = driver.find_elements(By.CSS_SELECTOR, "#orders-body tr")
        assert len(rows) == 3
        return f"Filas cargadas: {len(rows)}"
# --- EXAMPLE END: example_30_wait_for_table_rows ---


EXAMPLES = {
    "example_24_wait_fail_demo": example_24_wait_fail_demo,
    "example_25_explicit_wait_fix": example_25_explicit_wait_fix,
    "example_26_implicit_wait_example": example_26_implicit_wait_example,
    "example_27_wait_until_button_enabled": example_27_wait_until_button_enabled,
    "example_28_wait_for_async_results": example_28_wait_for_async_results,
    "example_29_wait_for_toast_appear_and_disappear": example_29_wait_for_toast_appear_and_disappear,
    "example_30_wait_for_table_rows": example_30_wait_for_table_rows,
}


if __name__ == "__main__":
    run_examples_from_cli(EXAMPLES)