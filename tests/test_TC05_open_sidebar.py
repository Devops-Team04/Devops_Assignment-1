"""
TC05 — Open the hamburger sidebar and verify it is visible.

GIVEN  the app is on the home screen
WHEN   user taps the hamburger button
THEN   the navigation sidebar must open and 'My Tasks' must be visible inside it
"""

from pages.home_page import HomePage
from pages.sidebar_page import SidebarPage


def test_open_sidebar_shows_navigation(driver):
    home = HomePage(driver)
    sidebar = SidebarPage(driver)

    home.open_sidebar()

    assert sidebar.is_sidebar_visible(), \
        "Expected the sidebar to open and display the 'My Tasks' navigation item."
