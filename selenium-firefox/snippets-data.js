window.COURSE_SNIPPET_FILES = {
    "examples/module1_intro.py": `from __future__ import annotations

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
`,
    "examples/module2_webdriver.py": `from __future__ import annotations

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
`,
    "examples/module3_interactions.py": `from __future__ import annotations

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
`,
    "examples/module4_waits.py": `from __future__ import annotations

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
`,
};