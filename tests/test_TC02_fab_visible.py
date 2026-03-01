"""
TC02 — 'Create new task' FAB button is visible on the home screen.

GIVEN  the app is on the home screen
WHEN   the screen is fully loaded
THEN   the floating action button with content-desc 'Create new task' must exist
"""

from pages.home_page import HomePage


def test_fab_create_task_is_visible(driver):
    home = HomePage(driver)
    assert home.is_accessibility_id_visible("Create new task"), \
        "Expected the 'Create new task' FAB to be visible on the home screen."
