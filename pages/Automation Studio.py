from cgi import test
from classes import TestCase
import streamlit as st
import pandas as pd
import DAL
import json
from streamlit_antd_components import  ChipItem, chip

st.set_page_config(layout="wide")


st.title("Automation Studio")
suites = DAL.get_test_suites()
suite = st.sidebar.selectbox(label = "Test Suites", options = suites["suite_name"], key = "suite_selector")
if suite:
    details_tab, cases_tab, runs_tab = st.tabs(["Suite Details","Test Cases", "Runs"])
    suite_id = suites[suites.suite_name == st.session_state.suite_selector].suite_id.iloc[0]
    test_cases = DAL.get_test_cases(suite_id)
    for test_case in test_cases:
        steps = json.loads(test_case["steps"]) if isinstance(test_case["steps"], str) else test_case["steps"]
        tc = TestCase(test_case["case_id"], test_case["title"], test_case["precondition"], test_case["description"], steps, test_case["expected_outcome"])
        tc.render(cases_tab)

    runs = DAL.get_runs(suite_id=suite_id)
    with runs_tab:
        selected_run_statuses = chip(
            items=[ChipItem(label=status) for status in runs.status.unique()], align='center', multiple=True
        )
    if len(selected_run_statuses) > 0:
        runs = runs[runs.status.isin(selected_run_statuses)]
    runs["Select"] = False
    edited_runs_df  = runs_tab.data_editor(runs, key = "runs_editor", use_container_width=True, hide_index  = True, disabled = ["run_title","started_at","status"] ,column_order=("Select", "run_title","started_at","status"),
                    column_config={"Select": st.column_config.CheckboxColumn("Select", disabled=False)})
    selected_run_ids = edited_runs_df[edited_runs_df.Select].run_id.tolist()
    if len(selected_run_ids) > 0:
        runs_tab.markdown("**Results**")
        test_df = DAL.get_results(selected_run_ids)
        runs_tab.data_editor(test_df,disabled=True,use_container_width=True,hide_index  = True,column_order=("CaseName", "case_code","created_at","status"))

    if runs_tab.button("New Run"):
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
