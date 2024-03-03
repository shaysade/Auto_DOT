import random
import streamlit as st
import DAL
import json

class TestCase:
    def __init__(self, id, title, description, precondition, steps, expected_result):
        self.case_id = id if id else random.randint(-10000,-1)
        self.title = title
        self.precondition = precondition
        self.description = description
        self.steps = steps
        self.expected_outcome = expected_result

    def persist(self):
        if self.case_id > 0:
            DAL.update_case(self)
        else:
            self.case_id = None
            DAL.insert_case(self)

    def render(self,widget):
        with widget.expander(f"{self.case_id}: {self.title}"):
            columns = st.columns([5,1])
            edit_mode = columns[1].toggle("Edit", value=False, key = f"toggle_edit_{self.case_id}")
            with columns[0]:
                if edit_mode:
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
                

            # Define a unique key for each button using the test case ID
            #button_key = f"button_{self.id}"
            #if st.button("Automate This TC"):
            #    pass