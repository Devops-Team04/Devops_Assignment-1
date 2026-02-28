"""
pages/base_page.py

BasePage — root class for all Page Objects.

Uses AppiumBy + UiSelector (same pattern as the working demo tests)
so locators are reliable on Compose-heavy UIs.
"""

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Common Appium actions shared by all Page Objects."""

    DEFAULT_TIMEOUT = 15

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    # ------------------------------------------------------------------
    # Low-level finders
    # ------------------------------------------------------------------

    def find_by_text(self, text: str):
        """Wait for and return an element matched by UiSelector text."""
        return self.wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')
            )
        )

    def find_by_accessibility_id(self, desc: str):
        """Wait for and return an element matched by content-desc."""
        return self.wait.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, desc))
        )

    def find_by_hint(self, hint: str):
        """Wait for and return an EditText matched by its hint attribute (XPath)."""
        return self.wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.XPATH, f'//android.widget.EditText[@hint="{hint}"]')
            )
        )

    def find_by_resource_id(self, resource_id: str):
        """Wait for and return an element matched by resource-id."""
        return self.wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, resource_id))
        )

    # ------------------------------------------------------------------
    # Visibility checks
    # ------------------------------------------------------------------

    def is_text_visible(self, text: str, timeout: int = 10) -> bool:
        """Return True if an element with the given text is visible."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(
                    (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')
                )
            )
            return True
        except TimeoutException:
            return False

    def is_accessibility_id_visible(self, desc: str, timeout: int = 10) -> bool:
        """Return True if an element with the given content-desc is visible."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(
                    (AppiumBy.ACCESSIBILITY_ID, desc)
                )
            )
            return True
        except TimeoutException:
            return False

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def click_by_text(self, text: str) -> None:
        """Find element by text and click it."""
        self.find_by_text(text).click()

    def click_by_accessibility_id(self, desc: str) -> None:
        """Find element by content-desc and click it."""
        self.find_by_accessibility_id(desc).click()

    def type_into_hint(self, hint: str, text: str) -> None:
        """Clear and type text into an EditText identified by its hint."""
        field = self.find_by_hint(hint)
        field.clear()
        field.send_keys(text)

    def press_back(self) -> None:
        """Press the Android hardware Back button."""
        self.driver.back()

    def hide_keyboard(self) -> None:
        """Dismiss the soft keyboard safely."""
        try:
            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
        except Exception:
            pass
