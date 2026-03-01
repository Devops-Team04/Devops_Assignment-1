"""
TC03 — Add a simple task and verify it appears in the task list.

GIVEN  the app is on the home screen
WHEN   user taps FAB → types a task name → taps Save
THEN   the task title must be visible in the home task list
"""

from pages.home_page import HomePage
from pages.task_page import TaskPage


def test_add_simple_task_appears_in_list(driver):
    task_title = "TC03 Buy milk and eggs"

    home = HomePage(driver)
    task = TaskPage(driver)

    home.tap_fab()
    task.enter_title(task_title)
    task.save_task()

    assert home.is_task_in_list(task_title), \
        f"Expected task '{task_title}' to appear in the list after saving."
