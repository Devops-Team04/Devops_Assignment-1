"""
TC09 — New task form shows 'No due date' by default.

GIVEN  the user opens the Add Task screen via the FAB
WHEN   the form is displayed for a brand-new task
THEN   the due-date field must read 'No due date'
"""

from pages.home_page import HomePage
from pages.task_page import TaskPage


def test_new_task_shows_no_due_date_by_default(driver):
    home = HomePage(driver)
    task = TaskPage(driver)

    home.tap_fab()

    assert task.is_no_due_date_shown(), \
        "Expected the new-task form to display 'No due date' as the default due-date value."
