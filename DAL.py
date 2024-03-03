import streamlit as st
from st_supabase_connection import SupabaseConnection
import pandas as pd
import json

@st.cache_resource
def db_connection():
    return st.connection("supabase",type=SupabaseConnection)

def get_test_suites():
    return pd.DataFrame(db_connection().table("TestSuites").select("*").eq("user_id",2).execute().data)

def get_test_cases(suite_id):
    return db_connection().table("TestCases").select("*").eq("suite_id",suite_id).execute().data

def get_runs(suite_id):
    return pd.DataFrame(db_connection().table("TestRuns").select("*").eq("suite_id",suite_id).execute().data)

def get_results(run_ids):
    df =  pd.DataFrame(db_connection().table("TestResults")
                       .select("TestCases(title), status, created_at, case_code")
                       .in_("run_id",run_ids)
                       .execute().data)
    df["CaseName"] = df.TestCases.str['title']
    return df

def update_case(test_case):
    #test_case["steps"] = json.dumps(test_case["steps"])
    db_connection().table('TestCases').update(test_case.__dict__).eq('case_id', test_case.case_id).execute()
    #test_case["steps"] = json.loads(test_case["steps"])

def insert_case(test_case):
    test_case_dict = test_case.__dict__.copy()
    del test_case_dict["case_id"]
    db_connection().table('TestCases').insert(test_case_dict).execute()

def insert_suite(name, description):
    res = db_connection().table('TestSuites').insert({"suite_name": name, "suite_description" : description}).execute()
    return res.data[0]["suite_id"]