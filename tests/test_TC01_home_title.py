"""
TC01 — Home screen displays 'My Tasks' title.

GIVEN  the app is launched
WHEN   the home screen loads
THEN   the toolbar must display the text 'My Tasks'
"""

from pages.home_page import HomePage


def test_home_screen_shows_my_tasks_title(driver):
    home = HomePage(driver)
    assert home.is_home_screen_visible(), \
        "Expected 'My Tasks' title to be visible on the home screen."
