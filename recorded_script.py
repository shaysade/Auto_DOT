from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.ebay.com/")
    page.get_by_placeholder("Search for anything").click()
    page.get_by_placeholder("Search for anything").fill("hat")
    page.get_by_placeholder("Search for anything").press("Enter")
    page.get_by_text("ILS 27.23").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Classic Adjustable Baseball").click()
    page1 = page1_info.value
    page1.get_by_test_id("x-atc-action").get_by_test_id("ux-call-to-action").click()
    page1.get_by_label("Please select a Colors").select_option("1")
    page1.get_by_test_id("x-atc-action").get_by_test_id("ux-call-to-action").click()
    expect(page1.get_by_label("Your shopping cart contains 1")).to_be_visible()
    page1.get_by_label("Your shopping cart contains 1").click()
    page1.get_by_label("Your shopping cart contains 1").click()
    expect(page1.locator("#gh-btn")).to_contain_text("Search")
    expect(page1.locator("[data-test-id=\"list-summary\"]").get_by_role("combobox")).to_have_value("1");
    page1.get_by_role("button", name="Ship to").click()
    page1.get_by_role("button", name="Done").click()
    page1.close()
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
