"""
TC10 — Sidebar contains a 'Default list' navigation option.

GIVEN  the sidebar is open
WHEN   the user inspects the navigation menu
THEN   the 'Default list' entry must be present and visible
"""

from pages.home_page import HomePage
from pages.sidebar_page import SidebarPage


def test_sidebar_contains_default_list(driver):
    home = HomePage(driver)
    sidebar = SidebarPage(driver)

    home.open_sidebar()

    assert sidebar.is_default_list_visible(), \
        "Expected the 'Default list' option to be visible in the navigation sidebar."
