import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def quiality_dashboad():
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

    # Creating the Quality Dashboard window
    st.title('Quality Dashboard')

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
        # Initialize session state to store the table with mock data if it doesn't exist
    if 'execution_table' not in st.session_state:
        # Initialize with some mock data
        mock_data = [
            {'Run ID': '001', 'Description': 'Data backup', 'Status': 'Completed', 'Result': 'Success'},
            {'Run ID': '002', 'Description': 'System update', 'Status': 'Running', 'Result': 'N/A'},
            {'Run ID': '003', 'Description': 'Data migration', 'Status': 'Pending', 'Result': 'N/A'},
            {'Run ID': '004', 'Description': 'Security scan', 'Status': 'Completed', 'Result': 'Failure'}
        ]
        st.session_state.execution_table = pd.DataFrame(mock_data)

    # Function to add a new row to the execution table
    def add_run(run_id, description, status, result):
        new_row = {'Run ID': run_id, 'Description': description, 'Status': status, 'Result': result}
        st.session_state.execution_table = st.session_state.execution_table.append(new_row, ignore_index=True)

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

    # Display the execution table
    st.write("Automation Run Execution Table:")
    st.dataframe(st.session_state.execution_table)
    
# Page dictionary
pages = {
    "Tests Suite": tests_suite,
    "Automation Studio": automation_studio,
    "Quality Dashboard": quiality_dashboad,
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
                