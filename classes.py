import random
import streamlit as st
import DAL
import json
import uuid


class TestCase:
    def __init__(self, id, title, description, precondition, steps, expected_result):
        self.case_id = id if id is not None else str(uuid.uuid4())
        self.title = title
        self.precondition = precondition
        self.description = description
        self.steps = steps
        self.expected_outcome = expected_result

    def persist(self):
        # Assuming DAL methods are properly handling insert/update based on case_id
        if isinstance(self.case_id, str) and not self.case_id.isdigit():
            # New case with UUID case_id
            self.case_id = DAL.insert_case(self)
        else:
            # Existing case with numeric case_id
            DAL.update_case(self)


    def render(self,widget):
        expander = widget.expander(self.title)
        with expander:
            columns = st.columns([5,1])
            edit_mode = columns[1].toggle("Edit", value=False, key = f"toggle_edit_{self.case_id}")
            with columns[0]:
                if edit_mode:
                    self.title = st.text_input("**Title:**", self.title)
                    self.description = st.text_input("**Description:**", self.description,)
                    self.precondition = st.text_input("**Precondition:**", self.precondition)
                    steps_str = "\n".join(self.steps)
                    self.steps = st.text_area("**Steps:**",steps_str).split("\n")
                    self.expected_outcome = st.text_input("**Expected Result:**", self.expected_outcome)
                    if self.case_id > 0:
                        if st.button("Save", key = f"save_button_{self.case_id}"):
                            self.persist()
                else:
                    st.write(f"**Description:** {self.description}")
                    st.write(f"**Precondition:** {self.precondition}")
                    st.write("**Steps:**")
                    for step in self.steps:
                        st.write(f"- {step}")
                    st.write(f"**Expected Result:** {self.expected_outcome}")
                
        return expander

class TestCode:
    def __init__(self, code):
        self.code = code
    
# class TestCode():self.case_id = id if id is not None else str(uuid.uuid4())
#     def __init__(self, code):
#         self.code = code

class TestRun():
    def __init__(self, run_id, suite_id, run_title, status = None, started_at = None, completed_at =None):
        self.run_id = run_id if run_id else random.randint(-10000,-1)
        self.run_title = run_title
        self.suite_id = int(suite_id)
        self.status = status
        self.started_at = started_at
        self.completed_at = completed_at

    def persist(self):
        if self.run_id > 0:
            pass
        else:
            self.run_id = None
            result = DAL.add_run(self)
            self.run_id = result["run_id"]


class CaseRun():
    def __init__(self, test_result_id ,run_id, case_id, status = None, created_at = None, logs = None):
        self.test_result_id = test_result_id if test_result_id else random.randint(-10000,-1)
        self.run_id = int(run_id)
        self.case_id = int(case_id)
        self.status = status
        self.created_at = created_at
        self.logs = logs

    def persist(self):
        if self.test_result_id > 0:
            pass
        else:
            self.test_result_id = None
            DAL.add_case_run(self)