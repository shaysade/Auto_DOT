from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.ebay.com/")
    page.get_by_placeholder("Search for anything").click()
    page.get_by_placeholder("Search for anything").fill("hat")
    page.get_by_placeholder("Search for anything").press("Enter")
    page.get_by_role("link", name="Men's Hats - apply Category filter", exact=True).click()
    page.get_by_role("link", name="Snapback - apply Style filter").click()
    page.get_by_text("ILS 28.04 to ILS").nth(1).click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Animal Farm Trucker Mesh").first.click()
    page1 = page1_info.value
    page1.get_by_test_id("x-atc-action").get_by_test_id("ux-call-to-action").click()
    page1.get_by_label("Please select a Color").select_option("10")
    page1.get_by_test_id("x-atc-action").get_by_test_id("ux-call-to-action").click()
    page1.locator("[data-test-id=\"cta-bottom\"]").click()
    page1.get_by_role("button", name="Continue as guest").click()
    page1.close()
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
