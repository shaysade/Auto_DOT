from playwright.sync_api import sync_playwright

def run_playwright_sync():
    result = ""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # Consider headless mode for automated runs
            page = browser.new_page()
            page.goto('https://www.ebay.com')
            page.fill('input[id="gh-ac"]', 'vintage watch')
            page.click('input[id="gh-btn"]')
            # Verify the results...
            if 'vintage watch' in page.title().lower():
                result = "Test Passed: The results page displays listings related to 'vintage watch'."
            else:
                result = "Test Failed: The page title does not contain 'vintage watch'."
            browser.close()
    except Exception as e:
        result = f"An error occurred: {str(e)}"
    return result

if __name__ == "__main__":
    test_result = run_playwright_sync()
    print(test_result)
