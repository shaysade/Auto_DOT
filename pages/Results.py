from cgi import test
from classes import TestCase
import streamlit as st
import pandas as pd
import DAL
import json
from streamlit_antd_components import  ChipItem, chip
import plotly.express as px
import numpy as np
import prompts

st.set_page_config(layout="wide")


runs = DAL.get_runs()

with st.sidebar:
    selected_run_statuses = chip(
        items=[ChipItem(label=status) for status in runs.status.unique()], align='center', multiple=True, size="sm", radius="sm"
    )
    if len(selected_run_statuses) > 0:
        runs = runs[runs.status.isin(selected_run_statuses)]
    selected_run = st.selectbox(options = runs.to_dict(orient="records"), label="Select Run",format_func= lambda x: x["run_title"])


#if len(selected_run_statuses) > 0:
#    runs = runs[runs.status.isin(selected_run_statuses)]
#runs["Select"] = False
#edited_runs_df  = st.data_editor(runs, key = "runs_editor", use_container_width=True, hide_index  = True, disabled = ["run_title","started_at","status"] ,column_order=("Select", "run_title","started_at","status"),
#                column_config={"Select": st.column_config.CheckboxColumn("Select", disabled=False)})
selected_run_id = selected_run["run_id"]
#if len(selected_run_ids) > 0:
st.markdown("**Results**")
test_df = DAL.get_results([selected_run_id])
fig = px.pie(test_df.status.value_counts().reset_index(), values='count', names='status', title='Status breakdown')
chart_columns = st.columns(2)
chart_columns[0].plotly_chart(fig,use_container_width=True)
failed_tests = test_df[test_df.status == "Failed"]
failed_tests['failure_status'] = np.random.choice(['New Fail', 'Repeated Fail', 'Production Bug'], size=len(failed_tests))
fig2 = px.pie(failed_tests.failure_status.value_counts().reset_index(), values='count', names='failure_status', title='Failure breakdown')
chart_columns[1].plotly_chart(fig2,use_container_width=True)
st.header("Failed Tests")
for _ , failed_test in failed_tests.iterrows():
    expander = st.expander(label = failed_test["CaseName"])
    columns = expander.columns(2)
    columns[0].text("Logs")
    columns[0].code("fhgfsdfhkdshf")

    columns[1].text("Test Code")
    columns[1].code("fhgfsdfhkdshf")

    expander.markdown("## Root cause analysis")
    expander.markdown(prompts.rca_example)
    expander.button("Auto repair", key = f"failed_test_repair_{failed_test.test_result_id}" )



a =   """"""
