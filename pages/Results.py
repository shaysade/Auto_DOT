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

def render_insights():
    insights = generage_insights
    for insight in insights.iterrows():
        col1, col2, col3 =st.expander(insight["Title"]).columns([1,3,3])
        # col1.header("Data")
        # col1.write(insight["data"])
        # col2.header("Trend")
        # col2.plotly_chart(px.line(data_frame=insight["data"],x= insight["data"].columns[0], y = insight["data"].columns[2] ))
        # col3.header("Vs Benchmark")
        # col3.plotly_chart(px.bar(x=["benchmark", "this week"], y =[insight["data"].iloc[:-1, 2].mean(), insight["data"].iloc[-1, 2]] ))  
        # cont = st.expander.container()
        # columns = cont.columns([1,1,1,6])
error = """
    return await self._wait_for_load_state_impl(state, timeout)
    AppData\Local\Programs\Python\Python311\Lib\site-packages\playwright\_impl\_frame.py:271
    await waiter.result()
    playwright._impl._errors.Error: Target page, context or browser has been closed"""
       
def generate_insights():
    insights = []
    
    insight1 = {"Title": "10 tests failed on a similar error", "TestCases": {}}
    insight2 = {"Title": "3 tests failed only on your environment", "TestCases": {}}
    insight3 = {"Title": "4 tests failed on other environments also", "TestCases": {}}
    
    num = 0
    for _, failed_test in failed_tests.iterrows():
        insight1["TestCases"][num] = failed_test.to_dict()
        num += 1
        if num >= 9:
            break
    
    num = 2
    for _, failed_test in failed_tests.iterrows():
        insight2["TestCases"][num] = failed_test.to_dict()
        num += 1
        if num >= 5:
            break
    
    num = 3
    for _, failed_test in failed_tests.iterrows():
        insight3["TestCases"][num] = failed_test.to_dict()
        num += 1
        if num >= 7:
            break
    
    insights.append(insight1)
    insights.append(insight2)
    insights.append(insight3)
    
    return insights


#if len(selected_run_statuses) > 0:
#    runs = runs[runs.status.isin(selected_run_statuses)]
#runs["Select"] = False
#edited_runs_df  = st.data_editor(runs, key = "runs_editor", use_container_width=True, hide_index  = True, disabled = ["run_title","started_at","status"] ,column_order=("Select", "run_title","started_at","status"),
#                column_config={"Select": st.column_config.CheckboxColumn("Select", disabled=False)})
selected_run_id = selected_run["run_id"]
#if len(selected_run_ids) > 0:
st.title("Results")
test_df = DAL.get_results([selected_run_id])
fig = px.pie(test_df.status.value_counts().reset_index(), values='count', names='status', title='Status breakdown')
chart_columns = st.columns(2)
chart_columns[0].plotly_chart(fig,use_container_width=True)
failed_tests = test_df[test_df.status == "Failed"]
failed_tests['failure_status'] = np.random.choice(['New Fail', 'Repeated Fail', 'Production Bug'], size=len(failed_tests))
fig2 = px.pie(failed_tests.failure_status.value_counts().reset_index(), values='count', names='failure_status', title='Failure breakdown')
chart_columns[1].plotly_chart(fig2,use_container_width=True)
st.header("Failed Tests Analysis")

#render_insights()
insights = generate_insights()
for insight in insights:
    col1, col2 ,col3= st.expander(insight["Title"]).columns([3,3,3])
    col1.header("Test list")
    col2.header("Environment")
    col3.header("Error")
    for test in insight["TestCases"].values():
        col1.write(test["CaseName"])
        col2.write(test["Environment"])
        col3.write(Exception(error))
        
    
    # #col1.write("Verify Homepage Load Speed")
    # col2.header(insight[""])
    # col2.write(Exception(error))

    # col1, col2 = st.expander("3 tests failed only on your environment").columns([3,3])
    # col1.header("Test list")
    # col1.write("Add to Cart and Modify Quantity")
    # col1.write("Verify Homepage Load Speed")
    # col2.header("Log")
    # col2.write(error)

    # col1, col2 = st.expander("4 tests failed on other environments also").columns([3,3])
    # col1.header("Test list")
    # col1.write("Add to Cart and Modify Quantity")
    # col1.write("Verify Homepage Load Speed")
    # col2.header("Environment")
    # col2.write("Production")
    # col2.write("Production")


# insights = generage_insights
# for insight in insights:
#     col1, col2, col3 =st.expander(insight["Title"]).columns([1,3,3])
    # col1.header("Data")
    # col1.write(insight["data"])
    # col2.header("Trend")
    # col2.plotly_chart(px.line(data_frame=insight["data"],x= insight["data"].columns[0], y = insight["data"].columns[2] ))
    # col3.header("Vs Benchmark")
    # col3.plotly_chart(px.bar(x=["benchmark", "this week"], y =[insight["data"].iloc[:-1, 2].mean(), insight["data"].iloc[-1, 2]] ))  
    # cont = st.expander.container()
    # columns = cont.columns([1,1,1,6])



    

    # for _ , failed_test in failed_tests.iterrows():
#     expander = st.expander(label = failed_test["CaseName"])
#     columns = expander.columns(2)
#     columns[0].text("Logs")
#     columns[0].code("fhgfsdfhkdshf")

#     columns[1].text("Test Code")
#     columns[1].code("fhgfsdfhkdshf")

#     expander.markdown("## Root cause analysis")
#     expander.markdown(prompts.rca_example)
#     expander.button("Auto repair", key = f"failed_test_repair_{failed_test.test_result_id}" )



a =   """"""
