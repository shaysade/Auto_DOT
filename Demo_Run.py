import streamlit as st
import pandas as pd

def tests_suite():
    st.title("Tests Suite")
    st.write("Welcome to the home page!")
    st.file_uploader("Upload your PRD")
    if(st.button("Generate Tests")):
        # Define a class to hold test case information
        class TestCase:
            def __init__(self, id, title, description, steps, expectedResult):
                self.id = id
                self.title = title
                self.description = description
                self.steps = steps
                self.expectedResult = expectedResult

        # Example test cases (abbreviated details for brevity)
        test_cases = [
            TestCase("TC1", "Search Functionality Verification", "Verify that the search functionality returns relevant results based on the entered keyword.",
                    ["Navigate to eBay homepage", "Enter 'vintage watch' in the search bar", "Press the search button"],
                    "The results page displays listings related to 'vintage watch'."),
            TestCase("TC2", "Filter Application in Search Results", "Check if applying filters refines the search results accurately.",
                    ["Perform a search for 'laptops'", "Apply a 'Brand' filter for 'Apple'", "Apply a price range filter", "Hit apply"],
                    "Results show only Apple laptops within the specified price range."),
            # Add other test cases here...
        ]

        # Streamlit app layout
        st.title('eBay Regression Test Cases')

        for tc in test_cases:
            with st.expander(f"{tc.id}: {tc.title}"):
                st.write(f"**Description:** {tc.description}")
                st.write("**Steps:**")
                for step in tc.steps:
                    st.write(f"- {step}")
                st.write(f"**Expected Result:** {tc.expectedResult}")

        # This uses st.expander to make each test case collapsible for better navigation.

            
def automation_studio():
    st.title("Automation Studio")
    st.write("Here's you will create run and manage all you automation tests!")
    
# Page dictionary
pages = {
    "Tests Suite": tests_suite,
    "Automation Studio": automation_studio,
}
# Sidebar navigation
st.sidebar.title("Auto Dot - Your Quality Operating System")         
page = st.sidebar.selectbox("Choose a page", list(pages.keys()))

# Call the page function
pages[page]()

# Initialize data storage
# data = bl.mock_data()

# if 'tab_names' not in st.session_state:
#     st.session_state.tab_names = []
# if 'data' not in st.session_state:
#     st.session_state.data = {}

# # Streamlit UI
# #st.title('Streamlit App with Tabs and Charts')
# st.sidebar.header("Dot.ai")
# if st.sidebar.button("Add Analysis"):
#     with st.form("my_form"):
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             #st.markdown("#### What happened? ####")
#             st.selectbox("What happened?",options = ["KPI drop", "KPI increase", "Funnel changed", "User journey change"], key='change_type')
#             st.selectbox("Where?",options = ["Orders", "Sales", "Engagment", "COGS"], index = None, key='kpi_name')
#             #st.text_input("Give us more details so we know what data to look for")
#             st.text("When did it happen?")
#             datetime_range_picker( unit="days", key='range_picker')
        
#         with col2:
#             st.header("Data")
#             nodes = [{"label": "Amplitude", "value": "slack"},
#                     {
#                         "label": "BigQuery",
#                         "value": "BigQuery",
#                         "children": [
#                             {"label": "Orders", "value": "orders"},
#                             {"label": "Inventory", "value": "inventory"},
#                             {"label": "Events", "value": "events"},
#                         ],
#                     }]
#             tree_select(nodes=nodes)   
#             #col2.write(tree_select)  

#         with col3:
#             st.header("Hints")
#             st.selectbox("Seasonality",options =bl.seasonalities, index = 0, key='Seasonality')
#             st.text_input("Where to look")
#             st.text_input("What to ignore")
#             st.text_input("Additional hint")
        
#         st.form_submit_button('Analyze', on_click=bl.add_kpi )


# # Create tabs
# #tabs = st.sidebar.radio("Select Tab:", ('Home', 'Add Tab'))

# #if tabs == 'Home':
# #    st.write("Welcome to the Home tab!")

# selected_tab = st.sidebar.selectbox("Session", st.session_state.tab_names,index=0)
# if selected_tab:
#     col1,col2 = st.columns([8,1])
#     seasonality = st.session_state.data[selected_tab]["seasonality"]
#     col2.selectbox(label=" Seasonality" ,options = bl.seasonalities, index=bl.seasonalities.index(seasonality))
#     insights = st.session_state.data[selected_tab]["insights"]
#     for insight in insights:
#         expander = st.expander(insight["name"])
#         bl.render_insight(expander,selected_tab,insight)
              
#     cont = st.container()
#     columns = cont.columns([1,1,8])
#     columns[0].button("Next Insights", key = "next_insignts", on_click=bl.next_insights, args=[selected_tab])
#     columns[1].button("Generate Report", key = "generate_report", on_click=bl.generate_summary, args=[selected_tab])

#     st.write("#")
#     st.write("#")
#     st.write("#")
#     with st.expander("Checked and looks usual"):
#         for item in ["Cancellation rate","Shipping times","Session length"]:
#             st.checkbox(item)
#         st.button("Show anyway")

# def comment1():
#     if len(st.session_state.tab_names) > 0:
#         tabs = st.tabs(st.session_state.tab_names)
#         for i in range(0,len(tabs)):
#             insights = st.session_state.data[st.session_state.tab_names[i]]
#             for insight in insights:
#                 expander = tabs[i].expander(insight["name"])
#                 bl.render_insight(expander,insight)
                
#             cont = tabs[i].container()
#             columns = cont.columns([1,1,10])
#             columns[0].button("Next Insights", key = "next_insignts_", on_click=bl.next_insights, args=[i])
#             columns[1].button("Generate Report", key = "generate_report", on_click=bl.generate_summary, args=[i])

#         tabs[i].write("#")
#         tabs[i].write("#")
#         tabs[i].write("#")
#         with tabs[i].expander("Checked and looks usual"):
#             for item in ["Cancellation rate","Shipping times","Session length"]:
#                 st.checkbox(item)
#             st.button("Show anyway")

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
                