"""
pages/home_page.py

HomePage — the main task-list screen of Tasks.org.

Locators are derived from home.xml (Appium Inspector dump).
All locators use AppiumBy so they can be trivially updated.
"""

from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class HomePage(BasePage):
    """
    Encapsulates locators and actions for the Tasks.org home screen.

    Typical flow:
        home = HomePage(driver)
        home.tap_fab()            # opens the new-task editor
        home.open_sidebar()       # opens the hamburger navigation drawer
    """

    # ------------------------------------------------------------------
    # Locators — sourced from home.xml (Appium Inspector)
    # ------------------------------------------------------------------

    # FAB: content-desc="Create new task", resource-id="org.tasks:id/fab"
    FAB = (AppiumBy.ACCESSIBILITY_ID, "Create new task")

    # Toolbar title text visible on home screen
    TOOLBAR_TITLE_TEXT = "My Tasks"

    # Bottom-bar search button: content-desc="Search", resource-id="org.tasks:id/menu_search"
    SEARCH_BUTTON = (AppiumBy.ID, "org.tasks:id/menu_search")

    # Bottom-bar sort button: content-desc="Sort", resource-id="org.tasks:id/menu_sort"
    SORT_BUTTON = (AppiumBy.ID, "org.tasks:id/menu_sort")

    # Hamburger button: first ImageButton in the home screen hierarchy
    # (no content-desc / resource-id on this element, so matched by class + instance)
    HAMBURGER_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.ImageButton").instance(0)')

    # Empty-state label when no tasks exist
    EMPTY_STATE_TEXT = "There are no tasks here."

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def tap_fab(self) -> None:
        """Tap the floating action button to open the add-task screen."""
        self.click_by_accessibility_id("Create new task")

    def is_home_screen_visible(self) -> bool:
        """Return True when the 'My Tasks' toolbar title is on screen."""
        return self.is_text_visible(self.TOOLBAR_TITLE_TEXT)

    def is_task_in_list(self, task_title: str) -> bool:
        """Return True if a task with the given title appears in the list."""
        return self.is_text_visible(task_title, timeout=5)

    def open_sidebar(self) -> None:
        """Tap the hamburger button to open the navigation drawer."""
        self.driver.find_element(*self.HAMBURGER_BUTTON).click()

    def tap_search_button(self) -> None:
        """Tap the Search button in the bottom app bar."""
        self.driver.find_element(*self.SEARCH_BUTTON).click()

    def tap_sort_button(self) -> None:
        """Tap the Sort button in the bottom app bar."""
        self.driver.find_element(*self.SORT_BUTTON).click()

    def is_empty_state_visible(self) -> bool:
        """Return True when the no-tasks empty-state text is shown."""
        return self.is_text_visible(self.EMPTY_STATE_TEXT)
