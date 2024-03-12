import streamlit as st
import pandas as pd
import server
import subprocess         
import DAL
import user_recording_script
import streamlit_antd_components as sac
from classes import TestCase

st.set_page_config(layout="wide")

if "current_step" not in st.session_state:
    st.session_state["current_step"] = 1
if "recordings" not in st.session_state:
    st.session_state["recordings"] = []
if 'suite_name' not in st.session_state:
    st.session_state.suite_name = ""
if 'description' not in st.session_state:
    st.session_state.description = ""

def update_step():
    st.session_state["current_step"] = st.session_state.steps +1

sac.steps(
    items=[
        sac.StepsItem(title='Suite Name'),
        sac.StepsItem(title='Suite Input',disabled = st.session_state.current_step < 2),
        sac.StepsItem(title='step 3', disabled=st.session_state.current_step < 3)
    ],key = "steps", index=st.session_state.current_step -1, return_index = True, on_change= update_step
)

def generate_test_cases():
    prd =  st.session_state.unique_prd_uploader.getvalue().decode("utf-8") if st.session_state.unique_prd_uploader is not None else None
    test_cases = server.generate_test_cases(st.session_state.unique_site_url_input, prd,st.session_state.recordings, st.session_state.txt_additional_instructions)
    st.session_state["test_suite"] = {"suite_name":st.session_state.suite_name, "description": st.session_state.description, "url" : st.session_state.unique_site_url_input}
    st.session_state['new_cases'] = test_cases     
    st.session_state.current_step = 3  

def render_step1():
    with st.form("step1_form"):
        suite_name = st.text_input("Suite Name")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Next")
        if submitted:
            st.session_state.current_step = 2
            st.session_state["suite_name"] = suite_name
            st.session_state["description"] = description
            st.rerun()

def render_step_2():
    with st.container():
        uploaded_file = st.file_uploader("Upload your PRD", type=['pdf', 'docx','text','txt'], key="unique_prd_uploader")
        for recordings in st.session_state.recordings:
            st.text("Recording captured")
        site_url_input = st.text_input("Enter your site URL", key="unique_site_url_input")
        record_submitted = st.button("Record" if len(st.session_state.recordings) ==0 else "Record another")
        if record_submitted and site_url_input:
            pw_code = user_recording_script.start_playwright_recording(start_url=site_url_input)
            st.session_state.recordings.append(pw_code)
            st.rerun()
        st.text_input("Focus", key="txt_additional_instructions")
        if st.button("Generate Cases"):
            generate_test_cases()
            st.rerun()

# Decide which step to display
if st.session_state.current_step == 1:
    render_step1()
elif st.session_state.current_step == 2:
    render_step_2()
    
if "new_cases" in  st.session_state:
    st.header(st.session_state.test_suite["suite_name"])
    st.text(st.session_state.test_suite["description"])
    cases = st.session_state['new_cases']
    for case in cases:
        expander = case.render(st)
        if expander.button("Generate Code", key = f"automate_button_case_{case.case_id}"):
            expander.code("##show a new code")
    columns = st.columns([1,1,1,5])
    if columns[0].button("Generate more"):
        pass
    if columns[1].button("Add test case manually"):
        new_case = TestCase(None,"New Case","","","","")
        st.session_state.new_cases.append(new_case)
        st.rerun()
    if columns[2].button("Add recording"):
        pass

    if st.button("Save Suite"):
        suite_id = DAL.insert_suite(st.session_state.test_suite["suite_name"],st.session_state.test_suite["description"])
        for case in cases:
            case.suite_id = suite_id
            case.persist()









