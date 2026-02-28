"""
pages/sidebar_page.py

SidebarPage — the navigation drawer (hamburger sidebar) in Tasks.org.

Locators are derived from hamburger_sidebar.xml (Appium Inspector dump).
"""

from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class SidebarPage(BasePage):
    """
    Encapsulates locators and actions for the hamburger navigation drawer.

    The sidebar is opened from HomePage.open_sidebar().

    Typical flow:
        home.open_sidebar()
        sidebar = SidebarPage(driver)
        assert sidebar.is_sidebar_visible()
        sidebar.tap_today()
    """

    # ------------------------------------------------------------------
    # Locators — sourced from hamburger_sidebar.xml (Appium Inspector)
    # ------------------------------------------------------------------

    # "My Tasks" row text in the sidebar
    MY_TASKS_TEXT = "My Tasks"

    # "Filters" row text
    FILTERS_TEXT = "Filters"

    # "Today" row text
    TODAY_TEXT = "Today"

    # "Recently modified" row text
    RECENTLY_MODIFIED_TEXT = "Recently modified"

    # "Tags" row text
    TAGS_TEXT = "Tags"

    # "Places" row text
    PLACES_TEXT = "Places"

    # "Local lists" section header text
    LOCAL_LISTS_TEXT = "Local lists"

    # "Default list" row text (first local list)
    DEFAULT_LIST_TEXT = "Default list"

    # Close navigation menu: content-desc="Close navigation menu"
    CLOSE_SIDEBAR = (AppiumBy.ACCESSIBILITY_ID, "Close navigation menu")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def is_sidebar_visible(self) -> bool:
        """Return True if the sidebar is open (My Tasks label is visible)."""
        return self.is_text_visible(self.MY_TASKS_TEXT)

    def tap_my_tasks(self) -> None:
        """Tap the 'My Tasks' row to go to the main task list."""
        self.click_by_text(self.MY_TASKS_TEXT)

    def tap_today(self) -> None:
        """Tap the 'Today' row to navigate to today's tasks."""
        self.click_by_text(self.TODAY_TEXT)

    def tap_filters(self) -> None:
        """Tap the 'Filters' row to open the Filters screen."""
        self.click_by_text(self.FILTERS_TEXT)

    def tap_tags(self) -> None:
        """Tap the 'Tags' row to open the Tags screen."""
        self.click_by_text(self.TAGS_TEXT)

    def tap_default_list(self) -> None:
        """Tap the 'Default list' row to navigate to that list."""
        self.click_by_text(self.DEFAULT_LIST_TEXT)

    def close_sidebar(self) -> None:
        """Close the navigation drawer by tapping the close affordance."""
        self.driver.find_element(*self.CLOSE_SIDEBAR).click()

    def is_today_visible(self) -> bool:
        """Return True if the 'Today' option is visible in the sidebar."""
        return self.is_text_visible(self.TODAY_TEXT)

    def is_filters_visible(self) -> bool:
        """Return True if the 'Filters' option is visible in the sidebar."""
        return self.is_text_visible(self.FILTERS_TEXT)

    def is_default_list_visible(self) -> bool:
        """Return True if the 'Default list' entry is visible in the sidebar."""
        return self.is_text_visible(self.DEFAULT_LIST_TEXT)

    def is_local_lists_section_visible(self) -> bool:
        """Return True if the 'Local lists' section header is visible."""
        return self.is_text_visible(self.LOCAL_LISTS_TEXT)
