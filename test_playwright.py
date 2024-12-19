import re
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("https://playwright.dev/")
    print("ran in function 1")
    expect(page).to_have_title(re.compile("Playwright"))
    
def test_get_started_link(page: Page):
    """
    Test to verify the 'Get Started' link on the Playwright homepage.

    This test performs the following steps:
    1. Navigates to the Playwright homepage.
    2. Clicks on the 'Get Started' link.
    3. Verifies that the 'Installation' heading is visible on the resulting page.

    Args:
        page (Page): A Playwright Page object representing the browser page.

    Raises:
        AssertionError: If the 'Installation' heading is not visible after clicking the 'Get Started' link.
    """
    page.goto("https://playwright.dev/")
    page.get_by_role("link", name="Get Started").click()
    print("ran in function 2")
    expect(page.get_by_role("heading" , name="Installation")).to_be_visible()