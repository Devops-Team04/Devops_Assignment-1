"""
TC08 — Search button is visible and tappable on the home screen.

GIVEN  the home screen is displayed
WHEN   the user taps the Search button
THEN   the action must complete without error (search UI is invoked)
"""

from pages.home_page import HomePage


def test_search_button_is_tappable(driver):
    home = HomePage(driver)

    assert home.is_accessibility_id_visible("Search"), \
        "Expected the Search button to be visible on the home screen."

    home.tap_search_button()
