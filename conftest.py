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
    Tasks.org shows on a fresh install.

    Sets implicit_wait(0) so that each failed element search is instant
    instead of waiting the full timeout.  This makes scanning through
    ~20 labels take seconds, not minutes.
    """
    # Save current implicit wait and set to 0 for fast scanning
    driver.implicitly_wait(0)

    # Ordered by likelihood for Tasks.org — "Continue without sync" is
    # the very first onboarding button shown on a fresh install.
    dismiss_texts = [
        "Continue without sync",
        "OK", "Ok",
        "SKIP", "Skip",
        "GET STARTED", "Get started",
        "GET IT", "Get it",
        "CONTINUE", "Continue",
        "DONE", "Done",
        "ALLOW", "Allow",
        "AGREE", "Agree",
        "NEXT", "Next",
        "ACCEPT", "Accept",
        "BEGIN", "Begin",
        "START", "Start",
        "CLOSE", "Close",
    ]
    for pass_num in range(5):      # up to 5 passes to clear stacked dialogs
        dismissed = False
        for label in dismiss_texts:
            try:
                btn = driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().text("{label}")'
                )
                btn.click()
                time.sleep(2)
                dismissed = True
                print(f"[onboarding] dismissed via text: '{label}' (pass {pass_num})")
                break
            except (NoSuchElementException, Exception):
                continue
        if not dismissed:
            break   # nothing left to dismiss
    time.sleep(1)
    # Restore a reasonable implicit wait for the caller
    driver.implicitly_wait(20 if IS_CI else 10)


@pytest.fixture(scope="session", autouse=True)
def setup_app_once():
    """
    Session-scoped fixture that runs exactly once per test session.

    In CI the onboarding is already bypassed by the workflow script
    (SharedPreferences p_first_start=false + adb pre-launch).  This
    fixture is a lightweight safety-net that opens one session to warm
    up the app and confirm it reaches the home screen before tests run.
    Locally this is a no-op.
    """
    if not IS_CI:
        yield
        return          # skip entirely on local machines

    print("[setup_app_once] Dismissing onboarding on fresh CI emulator...")
    d = None
    try:
        d = webdriver.Remote(APPIUM_URL, options=get_options())
        print("[setup_app_once] Session opened. Waiting 10s for app to fully render...")
        time.sleep(10)
        print(f"[setup_app_once] Current activity: {d.current_activity}")
        # Dump page source for diagnosis (visible in CI pytest output with -s)
        try:
            src = d.page_source[:2000]
            print(f"[setup_app_once] Page source (first 2000 chars):\n{src}")
        except Exception:
            pass
        _dismiss_onboarding(d)
        print("[setup_app_once] Onboarding dismissal complete.")
        time.sleep(3)
        print(f"[setup_app_once] Post-dismissal activity: {d.current_activity}")
    except Exception as exc:
        print(f"[setup_app_once] WARNING: {exc}")
    finally:
        if d is not None:
            try:
                d.quit()
            except Exception:
                pass
    print("[setup_app_once] Done.")
    time.sleep(2)
    yield


@pytest.fixture
def driver():
    """
    Function-scoped Appium WebDriver fixture.
    Each test gets a fresh driver instance → full independence guaranteed.
    """
    d = webdriver.Remote(APPIUM_URL, options=get_options())
    # CI emulators are slower — give more time to find elements.
    d.implicitly_wait(20 if IS_CI else 10)
    # Guarantee a clean home screen regardless of previous session state.
    # force_app_launch alone can't clear Android's saved Activity state,
    # so we terminate and relaunch the app explicitly.
    time.sleep(1)
    d.terminate_app("org.tasks")
    time.sleep(2)
    d.activate_app("org.tasks")
    # CI needs more time after activation for the app to fully render.
    time.sleep(6 if IS_CI else 2)
    yield d
    d.quit()
