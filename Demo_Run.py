import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor
import subprocess
import json


def quiality_dashboad():
    st.title("Quiality Dashboad")
    # Mock data for demonstration purposes
    manual_test_coverage = 85  # percent
    automation_feature_coverage = 75  # percent
    latest_run_success_rate = 92  # percent
    number_of_open_bugs = 23
    main_app_kpis = {
        'Login Feature': '95% uptime',
        'Data Processing': '99.9% accuracy',
        'User Management': 'Less than 1 second response time'
    }

    # Creating the Quality Dashboard window
    st.title('Quality Dashboard')

    # Test coverage pie chart
    st.header('Test Coverage')
    fig, ax = plt.subplots()
    ax.pie([manual_test_coverage, 100-manual_test_coverage], labels=['Manual', 'Not Covered'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

    # Automation feature coverage bar chart
    st.header('Automation Feature Coverage')
    fig, ax = plt.subplots()
    ax.bar(['Automation Coverage', 'Remaining'], [automation_feature_coverage, 100-automation_feature_coverage])
    st.pyplot(fig)

    # Latest run success rate using Streamlit's metric widget
    st.header('Latest Run Success Rate')
    st.metric(label="Success Rate", value=f"{latest_run_success_rate}%", delta="From previous run")

    # Number of open bugs using Streamlit's metric widget
    st.header('Number of Open Bugs')
    st.metric(label="Open Bugs", value=f"{number_of_open_bugs}")

    # Main app KPIs linked to feature areas
    st.header('Main App KPIs Linked to Feature Areas')
    for feature, kpi in main_app_kpis.items():
        st.subheader(feature)
        st.write(kpi)

    # You can also use Streamlit's expander to make the dashboard more compact
    with st.expander("See detailed KPI metrics"):
        for feature, kpi in main_app_kpis.items():
            st.text(f"{feature}: {kpi}")



# def run_playwright_sync():
#     result = ""
#     try:
#         with sync_playwright() as p:
#             browser = p.chromium.launch(headless=False)  # Adjust headless as needed
#             page = browser.new_page()
#             page.goto('https://www.ebay.com')
#             page.fill('input[id="gh-ac"]', 'vintage watch')
#             page.click('input[id="gh-btn"]')
#             page.wait_for_navigation()
#             # Verify the results...
#             if 'vintage watch' in page.title().lower():
#                 result = "Test Passed: The results page displays listings related to 'vintage watch'."
#             else:
#                 result = "Test Failed: The page title does not contain 'vintage watch'."
#             browser.close()
#     except Exception as e:
#         result = f"An error occurred: {str(e)}"
#     return result

# def test_ebay_search_for_vintage_watch():
#     # Run Playwright in a separate thread
#     with ThreadPoolExecutor() as executor:
#         future = executor.submit(run_playwright_sync)
#         result = future.result()  # Wait for completion
#         st.write(result)


# def test_ebay_search_for_vintage_watch():
#     with sync_playwright() as p:
#         # Launch the browser
#         browser = p.chromium.launch(headless=False)  # Set headless=False to see the browser
#         page = browser.new_page()

#         # Step 1: Navigate to eBay homepage
#         page.goto('https://www.ebay.com')

#         # Step 2: Enter 'vintage watch' in the search bar
#         page.fill('input[id="gh-ac"]', 'vintage watch')

#         # Step 3: Press the search button
#         page.click('input[id="gh-btn"]')
#         page.wait_for_navigation()

#         # Expected Result: The results page displays listings related to 'vintage watch'.
#         assert 'vintage watch' in page.title().lower(), "The page title does not contain 'vintage watch'"

#         # Optionally, check if listings are indeed displayed
#         # This example assumes there's a class for listing items, you'll need to replace '.listing-item' with the correct selector
#         listings_count = page.locator('.s-item').count()
#         assert listings_count > 0, "No listings found for 'vintage watch'."

#         # Close the browser
#         browser.close()                    
                            

def tests_suite():
    st.title("Tests Suite")
    # To ensure uniqueness, you can use a key for the file uploader. But since you need it only once, it's not necessary here.
    st.file_uploader("Upload your PRD", key="unique_prd_uploader")
    st.text_input("Enter your site URL", key="unique_site_url_input")
    
    if st.button("Generate Tests", key="generate_tests_button"):
        st.session_state['generate_tests'] = True

    if 'generate_tests' in st.session_state and st.session_state['generate_tests']:
        class TestCase:
            def __init__(self, id, title, description, steps, expectedResult):
                self.id = id
                self.title = title
                self.description = description
                self.steps = steps
                self.expectedResult = expectedResult

        test_cases = [
            TestCase("TC1", "Search Functionality Verification", "Verify that the search functionality returns relevant results based on the entered keyword.",
                     ["Navigate to eBay homepage", "Enter 'vintage watch' in the search bar", "Press the search button"],
                     "The results page displays listings related to 'vintage watch'."),
            TestCase("TC2", "Filter Application in Search Results", "Check if applying filters refines the search results accurately.",
                     ["Perform a search for 'laptops'", "Apply a 'Brand' filter for 'Apple'", "Apply a price range filter", "Hit apply"],
                     "Results show only Apple laptops within the specified price range."),
            # Add other test cases here...
        ]

        st.title('eBay Regression Test Cases')
        for tc in test_cases:
            with st.expander(f"{tc.id}: {tc.title}"):
                st.write(f"**Description:** {tc.description}")
                st.write("**Steps:**")
                for step in tc.steps:
                    st.write(f"- {step}")
                st.write(f"**Expected Result:** {tc.expectedResult}")

                # Define a unique key for each button using the test case ID
                button_key = f"button_{tc.id}"
                if st.button("Automate This TC", key=button_key):
                    call_demo_script()
                    # st.session_state[button_key] = True

        # Check if any button was pressed and execute the related function
        # for tc in test_cases:
        #     button_key = f"button_{tc.id}"
        #     if button_key in st.session_state and st.session_state[button_key]:
        #         test_ebay_search_for_vintage_watch()
        #         # Optionally, reset the button's state if needed
        #         st.session_state[button_key] = False
                
# Ensure to call your main function
# if __name__ == "__main__":
#     tests_suite()

def call_demo_script():
    try:
        # Ensure the correct path to the script if it's not in the same directory
        result = subprocess.run(["python", "demo_script.py"], capture_output=True, text=True, check=True)
        if result.stdout:
            st.write(result.stdout)
        if result.stderr:
            st.error("Error: " + result.stderr)
    except subprocess.CalledProcessError as e:
        st.error(f"Subprocess error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        
# def run_playwright_sync():
#     try:
#         # Assuming "playwright_script.py" is your Playwright script
#         result = subprocess.run(["python", "demo_script.py"], capture_output=True, text=True)
#         return result.stdout
#     except Exception as e:
#         return f"An error occurred: {str(e)}"
                      
def automation_studio():
    st.title("Automation Studio")
    st.write("Here's you will create run and manage all you automation tests!")
        # Initialize session state to store the table with mock data if it doesn't exist
    if 'execution_table' not in st.session_state:
        # Initialize with some mock data
        mock_data = [
            {'Run ID': '001', 'Description': 'Data backup', 'Status': 'Completed', 'Result': 'Success'},
            {'Run ID': '002', 'Description': 'System update', 'Status': 'Running', 'Result': 'N/A'},
            {'Run ID': '003', 'Description': 'Data migration', 'Status': 'Pending', 'Result': 'N/A'},
            {'Run ID': '004', 'Description': 'Security scan', 'Status': 'Completed', 'Result': 'Failure'}
        ]
        st.session_state.execution_table = pd.DataFrame(mock_data)

    # Function to add a new row to the execution table
    def add_run(run_id, description, status, result):
        new_row = {'Run ID': run_id, 'Description': description, 'Status': status, 'Result': result}
        st.session_state.execution_table = st.session_state.execution_table.append(new_row, ignore_index=True)

    # User input fields
    with st.form("new_run_form", clear_on_submit=True):
        st.write("Add a New Automation Run")
        run_id = st.text_input("Run ID", key="run_id")
        description = st.text_input("Description", key="description")
        status = st.selectbox("Status", ["Pending", "Running", "Completed", "Failed"], key="status")
        result = st.selectbox("Result", ["Success", "Failure", "N/A"], key="result")
        
        # Form submit button
        submitted = st.form_submit_button("Add Run")
        if submitted:
            add_run(run_id, description, status, result)

    # Display the execution table
    st.write("Automation Run Execution Table:")
    st.dataframe(st.session_state.execution_table)
    

# Page navigation setup
def setup_page_navigation():
    pages = {
        "Tests Suite": tests_suite,
        "Automation Studio": automation_studio,
        "Quality Dashboard": quiality_dashboad,
    }
    st.sidebar.title("Auto Dot - Your Quality Operating System")         
    page = st.sidebar.selectbox("Choose a page", list(pages.keys()))

    # Call the page function
    pages[page]()

if __name__ == "__main__":
    setup_page_navigation()


# # Page dictionary
# pages = {
#     "Tests Suite": tests_suite,
#     "Automation Studio": automation_studio,
#     "Quality Dashboard": quiality_dashboad,
# }
# # Sidebar navigation
# st.sidebar.title("Auto Dot - Your Quality Operating System")         
# page = st.sidebar.selectbox("Choose a page", list(pages.keys()))

# # Call the page function
# pages[page]()

