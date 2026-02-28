from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver import get_driver

def test_create_new_task():
    driver = get_driver()
    wait = WebDriverWait(driver, 20)

    # Click "Create new task" button
    create_task_button = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ACCESSIBILITY_ID, "Create new task")
        )
    )
    create_task_button.click()

    driver.quit()