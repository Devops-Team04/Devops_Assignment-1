"""
conftest.py — Root-level Pytest configuration.

Mirrors the driver setup from demo/driver.py but exposes it as a
pytest fixture so every test file can request it via dependency injection.
"""

import os
import time
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException

APPIUM_URL = "http://127.0.0.1:4723"
# Detect CI environment (set by GitHub Actions automatically)
IS_CI = os.environ.get("CI", "").lower() == "true"


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
    # Auto-grant all runtime permission dialogs (e.g. notifications on Android 13)
    options.auto_grant_permissions = True

    return options


def _dismiss_onboarding(driver) -> None:
    """
    Attempt to dismiss any first-run dialogs / onboarding screens that
    Tasks.org shows on a fresh install.  Tries common button labels;
    safe to call even when no dialogs are present.
    """
    dismiss_texts = [
        "GET IT", "Get it", "GET STARTED", "Get started",
        "SKIP", "Skip", "OK", "Ok", "ALLOW", "Allow",
        "CONTINUE", "Continue", "DONE", "Done",
        "AGREE", "Agree", "NEXT", "Next", "ACCEPT", "Accept",
    ]
    for _ in range(8):          # up to 8 passes to clear stacked dialogs
        dismissed = False
        for label in dismiss_texts:
            try:
                btn = driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().text("{label}")'
                )
                btn.click()
                time.sleep(0.8)
                dismissed = True
                break
            except (NoSuchElementException, Exception):
                continue
        if not dismissed:
            break   # nothing left to dismiss
    time.sleep(1)


@pytest.fixture(scope="session", autouse=True)
def setup_app_once():
    """
    Session-scoped fixture that runs exactly once per test session.

    In CI the app is freshly installed and has never been launched, so
    Tasks.org will show its first-run onboarding UI.  This fixture:
      1. Opens one Appium session (no_reset=True, auto_grant_permissions=True)
      2. Waits for the app to be ready
      3. Dismisses any onboarding / permission dialogs
      4. Quits the session

    After this, all per-test driver fixtures start with the app already
    initialised and land directly on the My Tasks home screen.
    """
    d = webdriver.Remote(APPIUM_URL, options=get_options())
    try:
        d.implicitly_wait(5)          # short wait — we just want to dismiss dialogs
        time.sleep(5)                  # give the app time to fully render
        _dismiss_onboarding(d)
    finally:
        try:
            d.terminate_app("org.tasks")
        except Exception:
            pass
        d.quit()
    time.sleep(1)


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
