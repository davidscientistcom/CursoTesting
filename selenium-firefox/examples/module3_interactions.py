from __future__ import annotations

from common import run_examples_from_cli

# --- EXAMPLE START: example_13_checkbox_and_textarea ---
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_13_checkbox_and_textarea() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("forms.html"))
        driver.find_element(By.ID, "username").send_keys("qa_real")
        driver.find_element(By.ID, "remember-me").click()
        bio = driver.find_element(By.ID, "bio")
        bio.send_keys("Necesito automatizar paso a paso con Selenium y Firefox")
        driver.find_element(By.ID, "submit-form").click()
        remember = driver.find_element(By.ID, "result-remember").text
        saved_bio = driver.find_element(By.ID, "result-bio").text
        assert remember == "sí"
        assert "automatizar" in saved_bio
        return saved_bio
# --- EXAMPLE END: example_13_checkbox_and_textarea ---


# --- EXAMPLE START: example_14_js_alert_accept ---
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_14_js_alert_accept() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("windows.html"))
        driver.find_element(By.ID, "show-alert").click()
        alert = driver.switch_to.alert
        text = alert.text
        alert.accept()
        assert text == "Alerta de laboratorio Selenium"
        return text
# --- EXAMPLE END: example_14_js_alert_accept ---


# --- EXAMPLE START: example_15_confirm_dismiss ---
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_15_confirm_dismiss() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("windows.html"))
        driver.find_element(By.ID, "show-confirm").click()
        alert = driver.switch_to.alert
        alert.dismiss()
        status = driver.find_element(By.ID, "dialog-status").text
        assert status == "Confirm cancelado"
        return status
# --- EXAMPLE END: example_15_confirm_dismiss ---


# --- EXAMPLE START: example_16_prompt_fill ---
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_16_prompt_fill() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("windows.html"))
        driver.find_element(By.ID, "show-prompt").click()
        alert = driver.switch_to.alert
        alert.send_keys("alias_firefox")
        alert.accept()
        status = driver.find_element(By.ID, "dialog-status").text
        assert "alias_firefox" in status
        return status
# --- EXAMPLE END: example_16_prompt_fill ---


# --- EXAMPLE START: example_17_new_tab_switch ---
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common import firefox_driver, lab_url, wait


def example_17_new_tab_switch() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("windows.html"))
        original = driver.current_window_handle
        driver.find_element(By.ID, "open-report-tab").click()
        wait(driver, 4).until(EC.number_of_windows_to_be(2))
        new_handle = [handle for handle in driver.window_handles if handle != original][0]
        driver.switch_to.window(new_handle)
        title = driver.find_element(By.ID, "popup-title").text
        driver.find_element(By.ID, "popup-close").click()
        status = driver.find_element(By.ID, "popup-status").text
        assert title == "Ventana auxiliar del laboratorio"
        assert status == "Revisado"
        driver.close()
        driver.switch_to.window(original)
        return title
# --- EXAMPLE END: example_17_new_tab_switch ---


# --- EXAMPLE START: example_18_iframe_interaction ---
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_18_iframe_interaction() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("frames.html"))
        driver.switch_to.frame("navigation-frame")
        nav_title = driver.find_element(By.ID, "frame-nav-title").text
        driver.switch_to.default_content()
        driver.switch_to.frame("content-frame")
        note = driver.find_element(By.ID, "frame-note")
        note.send_keys("Nota escrita dentro del iframe")
        driver.find_element(By.ID, "frame-save").click()
        output = driver.find_element(By.ID, "frame-output").text
        assert nav_title == "Menú del frame"
        assert "Nota escrita" in output
        return output
# --- EXAMPLE END: example_18_iframe_interaction ---


# --- EXAMPLE START: example_19_hover_menu ---
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from common import firefox_driver, lab_url, wait


def example_19_hover_menu() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("actions.html"))
        target = driver.find_element(By.ID, "hover-target")
        ActionChains(driver).move_to_element(target).perform()
        panel = wait(driver, 3).until(EC.visibility_of_element_located((By.ID, "hover-panel")))
        assert "Menú visible" in panel.text
        return panel.text
# --- EXAMPLE END: example_19_hover_menu ---


# --- EXAMPLE START: example_20_drag_and_drop ---
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from common import firefox_driver, lab_url, wait


def example_20_drag_and_drop() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("actions.html"))
        source = driver.find_element(By.ID, "drag-chip")
        target = driver.find_element(By.ID, "drop-zone")
        ActionChains(driver).drag_and_drop(source, target).perform()
        status = wait(driver, 3).until(EC.text_to_be_present_in_element((By.ID, "drop-status"), "completado"))
        assert status is True
        return driver.find_element(By.ID, "drop-status").text
# --- EXAMPLE END: example_20_drag_and_drop ---


# --- EXAMPLE START: example_21_double_click ---
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from common import firefox_driver, lab_url


def example_21_double_click() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("actions.html"))
        box = driver.find_element(By.ID, "double-box")
        ActionChains(driver).double_click(box).perform()
        status = driver.find_element(By.ID, "double-status").text
        assert status.endswith("1")
        return status
# --- EXAMPLE END: example_21_double_click ---


# --- EXAMPLE START: example_22_context_click ---
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from common import firefox_driver, lab_url


def example_22_context_click() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("actions.html"))
        zone = driver.find_element(By.ID, "context-zone")
        ActionChains(driver).context_click(zone).perform()
        status = driver.find_element(By.ID, "context-status").text
        assert status == "Click derecho capturado"
        return status
# --- EXAMPLE END: example_22_context_click ---


# --- EXAMPLE START: example_23_scroll_to_reveal ---
from selenium.webdriver.common.by import By

from common import firefox_driver, lab_url


def example_23_scroll_to_reveal() -> str:
    with firefox_driver() as driver:
        driver.get(lab_url("actions.html"))
        button = driver.find_element(By.ID, "scroll-button")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        button.click()
        status = driver.find_element(By.ID, "scroll-status").text
        assert status == "Objetivo activado tras scroll"
        return status
# --- EXAMPLE END: example_23_scroll_to_reveal ---


EXAMPLES = {
    "example_13_checkbox_and_textarea": example_13_checkbox_and_textarea,
    "example_14_js_alert_accept": example_14_js_alert_accept,
    "example_15_confirm_dismiss": example_15_confirm_dismiss,
    "example_16_prompt_fill": example_16_prompt_fill,
    "example_17_new_tab_switch": example_17_new_tab_switch,
    "example_18_iframe_interaction": example_18_iframe_interaction,
    "example_19_hover_menu": example_19_hover_menu,
    "example_20_drag_and_drop": example_20_drag_and_drop,
    "example_21_double_click": example_21_double_click,
    "example_22_context_click": example_22_context_click,
    "example_23_scroll_to_reveal": example_23_scroll_to_reveal,
}


if __name__ == "__main__":
    run_examples_from_cli(EXAMPLES)