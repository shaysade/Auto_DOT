import datetime
import requests
import json
import streamlit as st
import openai
from classes import TestCase
from datetime import datetime
import prompts
from playwright.sync_api import Playwright, sync_playwright, expect

@st.cache_resource
def get_llm(together = False):
    if together:
        return openai.OpenAI(api_key=st.secrets.Together.api_key, base_url="https://api.together.xyz/v1")
    else:
        return openai.OpenAI(api_key=st.secrets.OpenAI.api_key)

def get_mixtral_completion(prompt):
    llm = get_llm(together=True)
    print(datetime.now())
    return llm.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        #model = "mistralai/Mistral-7B-Instruct-v0.1",
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=3000,
        response_format={ "type": "json_object" },
    ).choices[0].message.content


def get_gpt4_completion(prompt):
    return get_llm().chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=3000,
        response_format={ "type": "json_object" },
    ).choices[0].message.content

def get_gpt3_completion(prompt):
    return get_llm().chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=3000,
        response_format={ "type": "json_object" },
    ).choices[0].message.content

def generate_auto_test_case(testcase_text,playwright_code):
    prompt = prompts.auto_test_from_testcase_text.format(playwright_code = playwright_code,testcase_text = testcase_text )
    generated_code = get_gpt3_completion(prompt)

def generate_test_cases(url, prd, playwright_code, additional_instructions):
    recordings_str = "".join([f"Recording {i+1}: {playwright_code[i]}  \n \n \n" for i in range(0, len(playwright_code))])
    prompt = prompts.test_cases_prompts.format(prd_text=prd, playwright_recordings=recordings_str, additional_instructions=additional_instructions)
    print(datetime.now())
    generated_test_cases = get_gpt3_completion(prompt)
    print(datetime.now())
    test_cases_dict = json.loads(generated_test_cases)

    # Use .get() to safely access 'test_cases' key, defaulting to an empty list if not found
    test_cases_json = test_cases_dict.get("test_cases", [])

    # Now we proceed with creating TestCase objects only if test_cases_json is not empty
    if test_cases_json:
        test_cases = [TestCase(id=None, **test_case) for test_case in test_cases_json]
    else:
        test_cases = []
        # Optionally, handle the case where no test cases are generated (e.g., log a warning or inform the user)
    
    return test_cases


# def generate_test_cases(url, prd, playwright_code, additional_instructions):
#     #html = requests.get(url = url).text
#     recordings_str = "".join([f"Recording {i+1}: {playwright_code[i]}  \n \n \n" for i in range(0,len(playwright_code))])
#     prompt = prompts.test_cases_prompts.format(prd_text = prd, playwright_recordings = recordings_str, additional_instructions = additional_instructions)
#     print(datetime.now())
#     generated_test_cases = get_gpt3_completion(prompt)
#     print(datetime.now())
#     test_cases_dict = json.loads(generated_test_cases)
#     test_cases = [TestCase(id = None,**test_case) for test_case in test_cases_dict["test_cases"]]
#     return test_cases


def create_code_from_case(case,url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
