import datetime
import requests
import json
import streamlit as st
import openai
from classes import TestCase
from datetime import datetime
test_cases_prompts = """ You are an test automation engineer co-pilot. You need to generate test cases from a PRD document and a site html.
                        The site name is: {url_name} 
                        the site html is: {html_content}
                        The PRD text is: {prd_text}
                        
                        
                        Generate 10 test cases. For each test case provide a title, a description, a precondition, a list of steps and an expected result
                        return a json in the right format. The steps are just a list of strings"""

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
        #model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        model="gpt-4-0125-preview",
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=3000,
        response_format={ "type": "json_object" },
    )


def generate_test_cases(url, prd):
    #html = requests.get(url = url).text
    prompt = test_cases_prompts.format(url_name = url, html_content = None, prd_text = prd)
    print(datetime.now())
    generated_test_cases = get_mixtral_completion(prompt)
    print(datetime.now())
    test_cases_dict = json.loads(generated_test_cases)
    test_cases = [TestCase(id = None,**test_case) for test_case in test_cases_dict["test_cases"]]
    return test_cases