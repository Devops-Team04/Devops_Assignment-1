"""
conftest.py — Root-level Pytest configuration.

Mirrors the driver setup from demo/driver.py but exposes it as a
pytest fixture so every test file can request it via dependency injection.
"""

import time
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

APPIUM_URL = "http://127.0.0.1:4723"


def get_options() -> UiAutomator2Options:
    """Return configured UiAutomator2Options for the Tasks.org app."""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emulator-5554"
    options.app_package = "org.tasks"
    options.app_activity = "com.todoroo.astrid.activity.MainActivity"
    options.automation_name = "UiAutomator2"
    options.no_reset = True          # preserve app data; skip onboarding
    options.force_app_launch = True  # always restart app to home screen per session
    return options


@pytest.fixture
def driver():
    """
    Function-scoped Appium WebDriver fixture.
    Each test gets a fresh driver instance → full independence guaranteed.
    """
    d = webdriver.Remote(APPIUM_URL, options=get_options())
    d.implicitly_wait(10)
    # Guarantee a clean home screen regardless of previous session state.
    # force_app_launch alone can't clear Android's saved Activity state,
    # so we terminate and relaunch the app explicitly.
    time.sleep(1)
    d.terminate_app("org.tasks")
    time.sleep(1)
    d.activate_app("org.tasks")
    time.sleep(2)
    yield d
    d.quit()
