from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver import get_driver

def test_continue_without_sync():
    driver = get_driver()
    wait = WebDriverWait(driver, 20)

    # Click "Continue without sync" button
    continue_button = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Continue without sync")')
        )
    )
    continue_button.click()

    driver.quit()