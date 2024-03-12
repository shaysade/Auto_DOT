import time
from playwright.sync_api import Playwright, sync_playwright, expect

class TestEbaySearchAddToCart:
    def setup_method(self, method):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.goto("https://www.ebay.com/")

    def test_search_and_add_to_cart(self):
        # Step 1: Click on the search bar
        self.page.get_by_placeholder("Search for anything").click()

        # Step 2: Enter 'hay' in the search bar
        self.page.get_by_placeholder("Search for anything").fill("hay")

        # Step 3: Click on the 'Search' button
        self.page.get_by_role("button", name="Search").click()
        time.sleep(2)
        # Step 4: Click on the specific product link
        with self.page.expect_popup() as page1_info:
            self.page.get_by_role("link", name="Timothy Hay - Hay4Pets - 3").click()
        page1 = page1_info.value
        time.sleep(3)

        # Ensure the new page has loaded
        #expect(page1).to_have_url(containing="ebay.com")

        # Step 5: Select a size
        page1.wait_for_selector('select[name="Size"]')
        page1.get_by_label("Please select a Size").select_option("1")

        # Step 6: Click on the 'Add to Cart' button
        add_to_cart_button = page1.get_by_test_id("x-atc-action").get_by_test_id("ux-call-to-action")
        add_to_cart_button.click()

        # Wait for the cart update
        page1.wait_for_selector('text="Added to cart"')

        # Expected Result: Item is successfully added to the cart
        expect(page1.get_by_test_id("cart-count")).to_have_text("1")

        # Verification step
        cart_text = page1.get_by_test_id("cart-count").text_content()
        assert "1" in cart_text, "Item was not successfully added to the cart"

    def teardown_method(self, method):
        self.page.close()
        self.context.close()
        self.browser.close()

# Running the test
if __name__ == "__main__":
    test = TestEbaySearchAddToCart()
    test.setup_method(method="test_search_and_add_to_cart")
    try:
        test.test_search_and_add_to_cart()
        print("Test Passed: Item was successfully added to the cart.")
    except AssertionError as e:
        print(f"Test Failed: {e}")
    finally:
        test.teardown_method(method="test_search_and_add_to_cart")
