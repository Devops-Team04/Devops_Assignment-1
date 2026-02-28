"""
pages/task_page.py

TaskPage — the add-task / edit-task screen in Tasks.org.

Locators are derived from addTask.xml (Appium Inspector dump).
"""

from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class TaskPage(BasePage):
    """
    Encapsulates locators and actions for the new/edit task screen.

    Typical flow:
        task = TaskPage(driver)
        task.enter_title("Buy groceries")
        task.save_task()
    """

    # ------------------------------------------------------------------
    # Locators — sourced from addTask.xml (Appium Inspector)
    # ------------------------------------------------------------------

    # Task name EditText: hint="Task name"
    TITLE_HINT = "Task name"

    # Description EditText: hint="Description"
    DESCRIPTION_HINT = "Description"

    # Save button: content-desc="Save" (android.view.View wrapping a Button)
    SAVE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Save")

    # "No due date" row text — visible by default on the add-task screen
    NO_DUE_DATE_TEXT = "No due date"

    # "No start date" row text — visible by default
    NO_START_DATE_TEXT = "No start date"

    # "Add subtask" label
    ADD_SUBTASK_TEXT = "Add subtask"

    # "Add tags" label
    ADD_TAGS_TEXT = "Add tags"

    # "Default list" chip shown on the new-task screen
    DEFAULT_LIST_TEXT = "Default list"

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def enter_title(self, title: str) -> None:
        """Type *title* into the Task name field."""
        self.type_into_hint(self.TITLE_HINT, title)
        self.hide_keyboard()

    def enter_description(self, text: str) -> None:
        """Type *text* into the Description field."""
        self.type_into_hint(self.DESCRIPTION_HINT, text)
        self.hide_keyboard()

    def save_task(self) -> None:
        """Tap the Save button to persist the task and return to home."""
        self.driver.find_element(*self.SAVE_BUTTON).click()

    def is_no_due_date_shown(self) -> bool:
        """Return True if the 'No due date' default row is visible."""
        return self.is_text_visible(self.NO_DUE_DATE_TEXT)

    def is_no_start_date_shown(self) -> bool:
        """Return True if the 'No start date' default row is visible."""
        return self.is_text_visible(self.NO_START_DATE_TEXT)

    def is_add_subtask_shown(self) -> bool:
        """Return True if the 'Add subtask' option is visible."""
        return self.is_text_visible(self.ADD_SUBTASK_TEXT)

    def is_add_tags_shown(self) -> bool:
        """Return True if the 'Add tags' option is visible."""
        return self.is_text_visible(self.ADD_TAGS_TEXT)


