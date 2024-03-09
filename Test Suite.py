import streamlit as st
import pandas as pd
import server
import subprocess         
import DAL
import user_recording_script

st.set_page_config(layout="wide")

def call_user_recording_script(start_url):
    try:
        # Correctly separated command arguments
        result = subprocess.run(["python", "user_recording_script.py", start_url], capture_output=True, text=True, check=True)
        #result = user_recording_script.start_playwright_recording(start_url=start_url)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Error: " + result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Subprocess error: {e}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def generate_test_cases(suite_name, suite_desc):
    with open('recorded_script.py', 'r') as file:
        pw_code = file.read()
    prd =  st.session_state.unique_prd_uploader.getvalue().decode("utf-8") if st.session_state.unique_prd_uploader is not None else None
    test_cases = server.generate_test_cases(st.session_state.unique_site_url_input, 
                                            prd,
                                            pw_code)
    st.session_state["test_suite"] = {"Name":st.session_state.suite_name, "Description": st.session_state.description}
    st.session_state['new_cases'] = test_cases                                         


# Initialize session state variables
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1

def render_step1():
    st.title("New Test Suite")
    with st.form("step1_form"):
        suite_name = st.text_input("Suite Name", key="suite_name")
        description = st.text_area("Description", key="description")
        option = st.selectbox("Choose an option:", ["", "Upload PRD", "Create from Recording"], key="option")
        submitted = st.form_submit_button("Next")
        if submitted:
            if option:
                # Now we just update the session state based on the user's interaction with the form
                st.session_state.current_step = 2
                st.session_state.choice = option

# Function to render Step 2 for "Upload PRD"
def render_step2_upload_prd():
    with st.form("upload_prd_form"):
        uploaded_file = st.file_uploader("Upload your PRD", type=['pdf', 'docx'], key="unique_prd_uploader")
        generate_tests_submitted = st.form_submit_button("Generate Tests")
        if generate_tests_submitted and uploaded_file is not None:
            # Call your actual function to handle the uploaded PRD file
            generate_test_cases(uploaded_file)

# Function to render Step 2 for "Create from Recording"
def render_step2_create_from_recording():
    with st.form("create_recording_form"):
        site_url_input = st.text_input("Enter your site URL", key="unique_site_url_input")
        record_submitted = st.form_submit_button("Record")
        if record_submitted and site_url_input:
            # Call your actual function to start the recording
            call_user_recording_script(site_url_input)

# Decide which step to display
if st.session_state.current_step == 1:
    render_step1()
elif st.session_state.current_step == 2:
    if st.session_state.choice == "Upload PRD":
        render_step2_upload_prd()
    elif st.session_state.choice == "Create from Recording":
        render_step2_create_from_recording()




# if "new_cases" in  st.session_state:
#     st.header(st.session_state.test_suite["Name"])
#     st.text(st.session_state.test_suite["Name"])
#     cases = st.session_state['new_cases']
#     for case in cases:
#         case.render(st)
#     if st.button("Save Suite"):
#         suite_id = DAL.insert_suite(st.session_state.test_suite["Name"],st.session_state.test_suite["Description"])
#         for case in cases:
#             case.suite_id = suite_id
#             case.persist()
# else:
#     st.title("New Test Suite")

#     column1, column2 = st.columns(2)

#     with column1:
#         suite_name = st.text_input("Suite Name", key="suite_name")
#         prd_uploader = st.file_uploader("Upload your PRD", key="unique_prd_uploader")
      

#     with column2:
#         suite_desc = st.text_input("Description", key="description")
#         site_url_input = st.text_input("Enter your site URL", key="unique_site_url_input")
#           # Add a spacer to push the button down so it aligns with the button in column2
#         st.write("")
#         st.write("")        

#     # Placing the buttons after the columns to attempt alignment
#     generate_tests_button = column1.button("Generate Tests", key="generate_tests_button")
#     record_button = column2.button("Record", key="record_button")

#     if generate_tests_button:
#         # Assuming generate_test_cases is a function you've defined elsewhere
#         generate_test_cases(suite_name, suite_desc)

#     if record_button:
#         # Assuming call_user_recording_script is a function you've defined elsewhere
#         call_user_recording_script(site_url_input)



# def call_demo_script():
#     try:
#         # Ensure the correct path to the script if it's not in the same directory
#         result = subprocess.run(["python", "demo_script.py"], capture_output=True, text=True, check=True)
#         if result.stdout:
#             st.write(result.stdout)
#         if result.stderr:
#             st.error("Error: " + result.stderr)
#     except subprocess.CalledProcessError as e:
#         st.error(f"Subprocess error: {e}")
#     except Exception as e:
#         st.error(f"An error occurred: {str(e)}")

a = """if 'generate_tests' in st.session_state and st.session_state['generate_tests']:
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
            """


        
                      
 


