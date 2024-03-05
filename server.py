import datetime
import requests
import json
import streamlit as st
import openai
from classes import TestCase
from datetime import datetime
import prompts

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


def generate_test_cases(url, prd, playwright_code):
    #html = requests.get(url = url).text
    if len(playwright_code) > 0:
        prompt = prompts.test_cases_from_pw_script.format(playwright_code = playwright_code)
    else:
        prompt = prompts.test_cases_prompts.format(url_name = url, html_content = None, prd_text = prd)
    print(datetime.now())
    generated_test_cases = get_gpt3_completion(prompt)
    print(datetime.now())
    test_cases_dict = json.loads(generated_test_cases)
    test_cases = [TestCase(id = None,**test_case) for test_case in test_cases_dict["test_cases"]]
    return test_cases