"""
TC04 — Add a task with a description and verify it appears in the list.

GIVEN  the app is on the home screen
WHEN   user taps FAB → enters title and description → taps Save
THEN   the task title must be visible in the home task list
"""

from pages.home_page import HomePage
from pages.task_page import TaskPage


def test_add_task_with_description(driver):
    task_title = "TC04 Prepare project report"
    task_desc = "Include charts, summary and appendix."

    home = HomePage(driver)
    task = TaskPage(driver)

    home.tap_fab()
    task.enter_title(task_title)
    task.enter_description(task_desc)
    task.save_task()

    assert home.is_task_in_list(task_title), \
        f"Expected task '{task_title}' to appear in the list after saving with description."
