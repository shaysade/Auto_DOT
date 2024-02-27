Demo_Run
import streamlit as st
import pandas as pd
from streamlit_datetime_range_picker import datetime_range_picker
from traitlets import default
import bl
from streamlit_tree_select import tree_select
import extra_streamlit_components as stx

st.set_page_config(layout="wide") 
# Initialize data storage
data = bl.mock_data()

if 'tab_names' not in st.session_state:
    st.session_state.tab_names = []
if 'data' not in st.session_state:
    st.session_state.data = {}

# Streamlit UI
#st.title('Streamlit App with Tabs and Charts')
st.sidebar.header("Dot.ai")
if st.sidebar.button("Add Analysis"):
    with st.form("my_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            #st.markdown("#### What happened? ####")
            st.selectbox("What happened?",options = ["KPI drop", "KPI increase", "Funnel changed", "User journey change"], key='change_type')
            st.selectbox("Where?",options = ["Orders", "Sales", "Engagment", "COGS"], index = None, key='kpi_name')
            #st.text_input("Give us more details so we know what data to look for")
            st.text("When did it happen?")
            datetime_range_picker( unit="days", key='range_picker')
        
        with col2:
            st.header("Data")
            nodes = [{"label": "Amplitude", "value": "slack"},
                    {
                        "label": "BigQuery",
                        "value": "BigQuery",
                        "children": [
                            {"label": "Orders", "value": "orders"},
                            {"label": "Inventory", "value": "inventory"},
                            {"label": "Events", "value": "events"},
                        ],
                    }]
            tree_select(nodes=nodes)   
            #col2.write(tree_select)  

        with col3:
            st.header("Hints")
            st.selectbox("Seasonality",options =bl.seasonalities, index = 0, key='Seasonality')
            st.text_input("Where to look")
            st.text_input("What to ignore")
            st.text_input("Additional hint")
        
        st.form_submit_button('Analyze', on_click=bl.add_kpi )


# Create tabs
#tabs = st.sidebar.radio("Select Tab:", ('Home', 'Add Tab'))

#if tabs == 'Home':
#    st.write("Welcome to the Home tab!")

selected_tab = st.sidebar.selectbox("Session", st.session_state.tab_names,index=0)
if selected_tab:
    col1,col2 = st.columns([8,1])
    seasonality = st.session_state.data[selected_tab]["seasonality"]
    col2.selectbox(label=" Seasonality" ,options = bl.seasonalities, index=bl.seasonalities.index(seasonality))
    insights = st.session_state.data[selected_tab]["insights"]
    for insight in insights:
        expander = st.expander(insight["name"])
        bl.render_insight(expander,selected_tab,insight)
              
    cont = st.container()
    columns = cont.columns([1,1,8])
    columns[0].button("Next Insights", key = "next_insignts", on_click=bl.next_insights, args=[selected_tab])
    columns[1].button("Generate Report", key = "generate_report", on_click=bl.generate_summary, args=[selected_tab])

    st.write("#")
    st.write("#")
    st.write("#")
    with st.expander("Checked and looks usual"):
        for item in ["Cancellation rate","Shipping times","Session length"]:
            st.checkbox(item)
        st.button("Show anyway")

def comment1():
    if len(st.session_state.tab_names) > 0:
        tabs = st.tabs(st.session_state.tab_names)
        for i in range(0,len(tabs)):
            insights = st.session_state.data[st.session_state.tab_names[i]]
            for insight in insights:
                expander = tabs[i].expander(insight["name"])
                bl.render_insight(expander,insight)
                
            cont = tabs[i].container()
            columns = cont.columns([1,1,10])
            columns[0].button("Next Insights", key = "next_insignts_", on_click=bl.next_insights, args=[i])
            columns[1].button("Generate Report", key = "generate_report", on_click=bl.generate_summary, args=[i])

        tabs[i].write("#")
        tabs[i].write("#")
        tabs[i].write("#")
        with tabs[i].expander("Checked and looks usual"):
            for item in ["Cancellation rate","Shipping times","Session length"]:
                st.checkbox(item)
            st.button("Show anyway")

# Display existing tabs
def comment_two():
    """if data:
        st.sidebar.subheader('Existing Tabs:')
        selected_tab = st.sidebar.radio('', [item['tab_name'] for item in data])

        # Display selected tab
        selected_data = [item for item in data if item['tab_name'] == selected_tab][0]
        with st.sidebar:
            st.title(selected_tab)
            st.write("Data for this tab:")
            st.write(selected_data['chart_data'])

            st.subheader('Charts:')
            for chart in selected_data['charts']:
                st.pyplot(chart)"""
                