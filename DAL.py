import streamlit as st
from st_supabase_connection import SupabaseConnection
import pandas as pd
import json
from datetime import datetime

@st.cache_resource
def db_connection():
    return st.connection("supabase",type=SupabaseConnection)

def get_test_suites():
    return pd.DataFrame(db_connection().table("TestSuites").select("*").execute().data)

def get_test_cases(suite_id):
    return db_connection().table("TestCases").select("*").eq("suite_id",suite_id).execute().data

def get_runs(suite_id):
    return pd.DataFrame(db_connection().table("TestRuns").select("*").eq("suite_id",suite_id).execute().data)

def get_runs():
    return pd.DataFrame(db_connection().table("TestRuns").select("*").order("started_at",desc=True).execute().data)


def get_results(run_ids):
    df =  pd.DataFrame(db_connection().table("TestResults")
                       .select("TestCases(title), status, created_at, case_code, test_result_id")
                       .in_("run_id",run_ids)
                       .execute().data)
    df["CaseName"] = df.TestCases.str['title']
    df["Environment"] = "Production" #TODO hard coded need to delete
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

def add_run(test_run):
    test_run_dict = test_run.__dict__.copy()
    del test_run_dict["run_id"]
    if test_run_dict["started_at"] is None:
        test_run_dict["started_at"] = datetime.now().isoformat()
    res = db_connection().table("TestRuns").insert(test_run_dict).execute()
    return res.data[0]


def add_case_run(case_run):
    case_run_dict = case_run.__dict__.copy()
    del case_run_dict["test_result_id"]
    if case_run_dict["created_at"] is None:
        case_run_dict["created_at"] = datetime.now().isoformat()
    db_connection().table("TestResults").insert(case_run_dict).execute()