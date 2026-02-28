"""
Driver Manager — Appium WebDriver initialization.
"""
from appium import webdriver
from appium.options.android import UiAutomator2Options

def get_driver():
    """Create and return a configured Appium WebDriver instance."""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emulator-5554"
    options.app_package = "org.tasks"
    options.app_activity = "com.todoroo.astrid.activity.MainActivity"
    options.automation_name = "UiAutomator2"
    options.no_reset = True

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    driver.implicitly_wait(60000)
    return driver