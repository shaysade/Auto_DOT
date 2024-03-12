test_cases_prompts = """ You are an test automation engineer co-pilot. You need to generate test cases from a PRD document and a site html.
                        The site name is: {url_name} 
                        the site html is: {html_content}
                        The PRD text is: {prd_text}
                        
                        
                        Generate 10 test cases. For each test case provide a title, a description, a precondition, a list of steps and an expected result
                        return a json in the right format. The steps are just a list of strings"""

test_cases_from_pw_script =  """ You are an test automation engineer co-pilot. You need to generate test cases from a playwright code.
                        The code is: {playwright_code} 

                        Generate 10 test cases for the happy flow, 10 negative tests and 10 edge case tests.
                        For each test case provide a title, a description, a precondition, a list of steps and an expected result
                        return a json in the right format. The steps are just a list of strings"""
                        
auto_test_from_testcase_text =  """ You are an test automation engineer co-pilot. You need to generate a playwright code from this text testcase
                        The testcaseb text is: {testcase_text} 
                        use this generated recorded playwritght code to add relevant selector to the testcase code 
                        here is the code: {playwright_code} 
                        Generate the code with a before and after method use a testing framwork make sure you are doing all 
                        test precondition and clean test data after test ended, use wait condition to element to be visible and enabled
                        use assert for verification steps , if test failed make sure you write the failure and also write is test passed"""                        