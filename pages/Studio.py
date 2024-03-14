import DAL
import streamlit as st
import json
from classes import TestCase, TestRun, CaseRun
from datetime import datetime

st.set_page_config(layout="wide")

def tc_dict_to_tc(test_case):
    steps = json.loads(test_case["steps"]) if isinstance(test_case["steps"], str) else test_case["steps"]
    tc = TestCase(test_case["case_id"], test_case["title"], test_case["precondition"], test_case["description"], steps, test_case["expected_outcome"])
    return tc
suites = DAL.get_test_suites()
suite = st.sidebar.selectbox(label = "Test Suites", options = suites["suite_name"], key = "suite_selector")
if suite:
    container = st.container()
    suite_id = suites[suites.suite_name == st.session_state.suite_selector].suite_id.iloc[0]
    test_cases_dicts = DAL.get_test_cases(suite_id)
    test_cases = [tc_dict_to_tc(tc_dict) for tc_dict in test_cases_dicts]
    for test_case in test_cases:
        #steps = json.loads(test_case["steps"]) if isinstance(test_case["steps"], str) else test_case["steps"]
        #tc = TestCase(test_case["case_id"], test_case["title"], test_case["precondition"], test_case["description"], steps, test_case["expected_outcome"])
        test_case.render(container)

    new_run_name = st.text_input("Run name", f"{st.session_state.suite_selector} - {datetime.now()}")
    if st.button("Run Suite"):
        new_run = TestRun(None,suite_id,new_run_name,"Pending")
        new_run.persist()
        for test_case in test_cases:
            case_run = CaseRun(None,new_run.run_id,test_case.case_id,status="Failed")
            case_run.persist()