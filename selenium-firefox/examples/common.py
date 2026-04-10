from __future__ import annotations

import os
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Callable

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = os.getenv("SELENIUM_LAB_URL", "http://127.0.0.1:8765/lab")
FIREFOX_CANDIDATES = [
    os.getenv("FIREFOX_BINARY", ""),
    "/snap/firefox/current/usr/lib/firefox/firefox",
    "/usr/lib/firefox/firefox",
]


def lab_url(path: str = "index.html") -> str:
    clean_path = path.lstrip("/")
    return f"{BASE_URL}/{clean_path}"


def build_driver(*, implicit_wait: float = 0, headless: bool | None = None) -> webdriver.Firefox:
    options = Options()
    effective_headless = os.getenv("HEADLESS", "0") == "1" if headless is None else headless
    if effective_headless:
        options.add_argument("-headless")

    for candidate in FIREFOX_CANDIDATES:
        if candidate and Path(candidate).is_file():
            options.binary_location = candidate
            break

    driver = webdriver.Firefox(options=options)
    driver.set_window_size(1440, 1100)
    if implicit_wait:
        driver.implicitly_wait(implicit_wait)
    return driver


@contextmanager
def firefox_driver(*, implicit_wait: float = 0, headless: bool | None = None):
    driver = build_driver(implicit_wait=implicit_wait, headless=headless)
    try:
        yield driver
    finally:
        driver.quit()


def wait(driver, timeout: float = 5) -> WebDriverWait:
    return WebDriverWait(driver, timeout)


def run_examples_from_cli(example_map: dict[str, Callable[[], str]]) -> None:
    if len(sys.argv) < 2:
        available = "\n".join(f"- {name}" for name in example_map)
        raise SystemExit(f"Uso: python {Path(sys.argv[0]).name} <example_name>\nDisponibles:\n{available}")

    example_name = sys.argv[1]
    if example_name not in example_map:
        raise SystemExit(f"Ejemplo desconocido: {example_name}")

    print(example_map[example_name]())