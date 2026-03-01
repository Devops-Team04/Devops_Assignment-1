"""
TC06 — Sidebar contains a 'Today' navigation option.

GIVEN  the sidebar is open
WHEN   the user inspects the navigation menu
THEN   a 'Today' option must be present and visible
"""

from pages.home_page import HomePage
from pages.sidebar_page import SidebarPage


def test_sidebar_contains_today_option(driver):
    home = HomePage(driver)
    sidebar = SidebarPage(driver)

    home.open_sidebar()

    assert sidebar.is_today_visible(), \
        "Expected the 'Today' option to be visible in the navigation sidebar."
