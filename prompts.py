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

rca_example = """
***Application Logs Review*** No errors were logged during the test execution time, suggesting the application server did not encounter any internal errors.

***Test Script Review*** The test script was reviewed for any recent changes. No changes were made to the login functionality test scripts in the last update cycle.

***Environment Check*** The staging environment was checked for any recent updates. It was found that a new version of the login service was deployed a day before the test execution.

***Network Analysis*** Network logs during the test period showed no signs of connectivity issues or latency spikes.

***Service Dependency Check*** The login service's dependencies were reviewed and all were found to be operational. However, it was noted that the user authentication module had undergone a major update in the recent deployment.

***Configuration Comparison*** Comparing the configurations between the last successful test run and the current failed test revealed that the endpoint for the authentication service had been inadvertently changed during the recent deployment.

## Root Cause
The root cause of the failed automation test was identified as an incorrect configuration of the authentication service endpoint in the staging environment following a recent deployment. This misconfiguration prevented the login service from communicating with the authentication module, resulting in a failure to authenticate users."""