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
    Tasks.org shows on a fresh install.  Tries exact text, textContains,
    and coordinate taps as fallback; safe to call when no dialogs present.
    """
    dismiss_texts = [
        "GET IT", "Get it", "GET STARTED", "Get started",
        "SKIP", "Skip", "OK", "Ok", "ALLOW", "Allow",
        "CONTINUE", "Continue", "DONE", "Done",
        "AGREE", "Agree", "NEXT", "Next", "ACCEPT", "Accept",
        "BEGIN", "Begin", "START", "Start", "CLOSE", "Close",
    ]
    for pass_num in range(10):      # up to 10 passes to clear stacked dialogs
        dismissed = False
        # Strategy 1: exact text match
        for label in dismiss_texts:
            try:
                btn = driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().text("{label}")'
                )
                btn.click()
                time.sleep(1.0)
                dismissed = True
                print(f"[onboarding] dismissed via exact text: '{label}' (pass {pass_num})")
                break
            except (NoSuchElementException, Exception):
                continue
        if dismissed:
            continue
        # Strategy 2: textContains for partial matches
        for fragment in ["Get", "Start", "Skip", "Continue", "Accept", "Allow", "Next"]:
            try:
                btn = driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().textContains("{fragment}")'
                )
                btn.click()
                time.sleep(1.0)
                dismissed = True
                print(f"[onboarding] dismissed via textContains: '{fragment}' (pass {pass_num})")
                break
            except (NoSuchElementException, Exception):
                continue
        if dismissed:
            continue
        # Strategy 3: coordinate tap at bottom-centre (common button position)
        # Nexus 6 profile: 1440 x 2560  → centre-bottom ≈ (720, 2050)
        if pass_num < 3:
            try:
                size = driver.get_window_size()
                cx = size['width'] // 2
                cy = int(size['height'] * 0.80)
                driver.tap([(cx, cy)])
                time.sleep(1.0)
                print(f"[onboarding] coordinate tap at ({cx},{cy}) (pass {pass_num})")
                continue   # keep trying passes after a coord tap
            except Exception:
                pass
        break   # nothing dismissed and no coord tap — done
    time.sleep(1)


@pytest.fixture(scope="session", autouse=True)
def setup_app_once():
    """
    Session-scoped fixture that runs exactly once per test session.

    Only active in CI (IS_CI=True).  On a fresh emulator the app will show
    its first-run onboarding UI; this fixture dismisses it before any test
    runs.  Locally the app is already set up so this is a no-op.

    All operations are wrapped in try/except so a failure here never blocks
    the individual per-test fixtures.
    """
    if not IS_CI:
        yield
        return          # skip entirely on local machines

    # Primary onboarding bypass is handled by the CI workflow script:
    # it writes org.tasks_preferences.xml with p_first_start=false via
    # `adb root` before pytest runs.  This fixture is a safety-net in case
    # the SharedPreferences approach doesn't cover all dialogs.
    print("[setup_app_once] Starting onboarding safety-net session...")
    d = None
    try:
        d = webdriver.Remote(APPIUM_URL, options=get_options())
        d.implicitly_wait(10)
        print("[setup_app_once] Appium session opened. Waiting 12s for app to render...")
        time.sleep(12)          # give the app extra time to fully render
        _dismiss_onboarding(d)
        print("[setup_app_once] Onboarding dismissal complete.")
    except Exception as exc:
        # Log the error so it appears in CI logs for diagnosis
        print(f"[setup_app_once] WARNING: exception during onboarding dismissal: {exc}")
    finally:
        if d is not None:
            try:
                d.terminate_app("org.tasks")
            except Exception:
                pass
            try:
                d.quit()
            except Exception:
                pass    # session may already be gone — that's fine
    print("[setup_app_once] Done. Handing off to individual tests.")
    time.sleep(2)
    yield


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
