test_cases_prompts = """ You are an test automation engineer co-pilot. You need to generate test cases from a PRD document and playwright code
                        Pay attention to additional instruction provided

                        The PRD text is: {prd_text}

                        Playwright code: {playwright_recordings}

                        Generate 10 test cases for the happy flow, 10 negative tests and 10 edge case tests.
                        For each test case provide a title, a description, a precondition, a list of steps and an expected result
                        return a json in the right format. The steps are just a list of strings
                        
                        Additional Instructions: {additional_instructions}
                        """

test_cases_from_pw_script =  """ You are an test automation engineer co-pilot. You need to generate test cases from a playwright code.
                        The code is: {playwright_code} 

                        Generate 10 test cases for the happy flow, 10 negative tests and 10 edge case tests.
                        For each test case provide a title, a description, a precondition, a list of steps and an expected result
                        return a json in the right format. The steps are just a list of strings"""