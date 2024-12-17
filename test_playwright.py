import re
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("https://playwright.dev/")
    print("ran in function 1")
    expect(page).to_have_title(re.compile("Playwright"))
    
def test_get_started_link(page: Page):
    page.goto("https://playwright.dev/")
    page.get_by_role("link", name="Get Started").click()
    print("ran in function 2")
    expect(page.get_by_role("heading" , name="Installation")).to_be_visible()