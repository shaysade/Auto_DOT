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
..\..\..\AppData\Local\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\_pytest\assertion\rewrite.py:178: in exec_module
    exec(co, module.__dict__)
test_add_product_to_cart.py:48: in <module>
    test_add_product_to_basket(playwright)
test_add_product_to_cart.py:12: in test_add_product_to_basket
    page.wait_for_load_state('networkidle')
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\playwright\sync_api\_generated.py:8736: in wait_for_load_state
    self._sync(self._impl_obj.wait_for_load_state(state=state, timeout=timeout))
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\playwright\_impl\_page.py:516: in wait_for_load_state
    return await self._main_frame.wait_for_load_state(**locals_to_params(locals()))
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\playwright\_impl\_frame.py:243: in wait_for_load_state
    return await self._wait_for_load_state_impl(state, timeout)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\playwright\_impl\_frame.py:271: in _wait_for_load_state_impl
    await waiter.result()
E   playwright._impl._errors.Error: Target page, context or browser has been closed"""
       
def generage_insights():
    insights = []
    insight1 = {}
    insight2 = {}
    insight3 = {}
        
    insight1["Title"] = ["10 of your tests failed on a similar error"]
    num = 0
    for failed_test in failed_tests.iterrows():
        insight1["test_cases"][++num] = failed_test
        num = num+1
        if num == 3:
            continue
    insights.append(insight1)

    insight2["Title"] = ["3 of your tests failed only on your environment"]
    num = 2
    for failed_test in failed_tests.iterrows():
        insight2["test_cases"][num] = failed_test
        num = num+1
        if num == 5:
            continue
    insights.append(insight2)

    insight3["Title"] = ["4 of your tests failed on other environments also"]
    num = 3
    for failed_test in failed_tests.iterrows():
        insight3["test_cases"][num] = failed_test
        num = num+1
        if num == 7:
            continue
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
#render_insights

col1, col2 = st.expander("10 of your tests failed on a similar error").columns([3,3])
col1.header("Test list")
col1.write("Add to Cart and Modify Quantity")
col1.write("Verify Homepage Load Speed")
col2.header("Log")
col2.write(error)

col1, col2 = st.expander("3 of your tests failed only on your environment").columns([3,3])
col1.header("Test list")
col1.write("Add to Cart and Modify Quantity")
col1.write("Verify Homepage Load Speed")
col2.header("Log")
col2.write(error)

col1, col2 = st.expander("4 of your tests failed on other environments also").columns([3,3])
col1.header("Test list")
col1.write("Add to Cart and Modify Quantity")
col1.write("Verify Homepage Load Speed")
col2.header("Environment")
col2.write("Production")
col2.write("Production")


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
