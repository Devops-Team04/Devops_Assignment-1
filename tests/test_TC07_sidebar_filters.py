"""
TC07 — Sidebar contains a 'Filters' navigation option.

GIVEN  the sidebar is open
WHEN   the user inspects the navigation menu
THEN   a 'Filters' option must be present and visible
"""

from pages.home_page import HomePage
from pages.sidebar_page import SidebarPage


def test_sidebar_contains_filters_option(driver):
    home = HomePage(driver)
    sidebar = SidebarPage(driver)

    home.open_sidebar()

    assert sidebar.is_filters_visible(), \
        "Expected the 'Filters' option to be visible in the navigation sidebar."
