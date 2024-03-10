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

def generate_test_cases():
    with open('recorded_script.py', 'r') as file:
        pw_code = file.read()
    prd = ""
    #prd =  st.session_state.unique_prd_uploader.getvalue().decode("utf-8") if st.session_state.unique_prd_uploader is not None else None
    test_cases = server.generate_test_cases(st.session_state.unique_site_url_input, 
                                            prd,
                                            pw_code)
    st.session_state["test_suite"] = {"Name":st.session_state.suite_name, "Description": st.session_state.description, "url" : st.session_state.unique_site_url_input}
    st.session_state['new_cases'] = test_cases     

    st.session_state.current_step = 3                                    


# Initialize session state variables
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'suite_name' not in st.session_state:
    st.session_state.suite_name = ""
if 'description' not in st.session_state:
    st.session_state.description = ""

def render_step1():
    st.title("New Test Suite")
    with st.form("step1_form"):
        suite_name = st.text_input("Suite Name", key="suite_name")
        description = st.text_area("Description", key="description")
        option = st.selectbox("Choose an option:", ["", "Upload PRD", "Create from Recording"], key="option")
        submitted = st.form_submit_button("Next")
        if submitted:
            if option:
                st.session_state.current_step = 2
                st.session_state.choice = option
                st.rerun()

# Function to render Step 2 for "Upload PRD"
def render_step2_upload_prd():
    with st.form("upload_prd_form"):
        uploaded_file = st.file_uploader("Upload your PRD", type=['pdf', 'docx','text','txt'], key="unique_prd_uploader")
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
            generate_test_cases()
            st.rerun()


if "new_cases" in  st.session_state:
    st.header(st.session_state.test_suite["Name"])
    st.text(st.session_state.test_suite["Name"])
    cases = st.session_state['new_cases']
    for case in cases:
        expander = case.render(st)
        if expander.button("Generate Code", key = f"automate_button_case_{case.case_id}"):
            expander.code("##show a new code")
    if st.button("Save Suite"):
        suite_id = DAL.insert_suite(st.session_state.test_suite["Name"],st.session_state.test_suite["Description"])
        for case in cases:
            case.suite_id = suite_id
            case.persist()

# Decide which step to display
if st.session_state.current_step == 1:
    render_step1()
elif st.session_state.current_step == 2:
    if st.session_state.choice == "Upload PRD":
        render_step2_upload_prd()
    elif st.session_state.choice == "Create from Recording":
        render_step2_create_from_recording()




