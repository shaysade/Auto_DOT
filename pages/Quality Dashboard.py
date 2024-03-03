from operator import index
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Quiality Dashboad")
# Mock data for demonstration purposes
manual_test_coverage = 85  # percent
automation_feature_coverage = 75  # percent
latest_run_success_rate = 92  # percent
number_of_open_bugs = 23
main_app_kpis = {
    'Login Feature': '95% uptime',
    'Data Processing': '99.9% accuracy',
    'User Management': 'Less than 1 second response time'
}


# Test coverage pie chart
st.header('Test Coverage')
fig, ax = plt.subplots()
ax.pie([manual_test_coverage, 100-manual_test_coverage], labels=['Manual', 'Not Covered'], autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig)

# Automation feature coverage bar chart
st.header('Automation Feature Coverage')
fig, ax = plt.subplots()
ax.bar(['Automation Coverage', 'Remaining'], [automation_feature_coverage, 100-automation_feature_coverage])
st.pyplot(fig)

# Latest run success rate using Streamlit's metric widget
st.header('Latest Run Success Rate')
st.metric(label="Success Rate", value=f"{latest_run_success_rate}%", delta="From previous run")

# Number of open bugs using Streamlit's metric widget
st.header('Number of Open Bugs')
st.metric(label="Open Bugs", value=f"{number_of_open_bugs}")

# Main app KPIs linked to feature areas
st.header('Main App KPIs Linked to Feature Areas')
for feature, kpi in main_app_kpis.items():
    st.subheader(feature)
    st.write(kpi)

# You can also use Streamlit's expander to make the dashboard more compact
with st.expander("See detailed KPI metrics"):
    for feature, kpi in main_app_kpis.items():
        st.text(f"{feature}: {kpi}")
