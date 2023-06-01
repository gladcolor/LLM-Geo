import unittest
import  LLM_Geo_Constants as constants
import LLM_Geo_kernel
import helper
import pickle
import os
import networkx as nx
from LLM_Geo_kernel import Solution
import sys
import traceback

class MyTestCase(unittest.TestCase):
    def test_get_LLM_response_for_graph(self):
        # Case 4: COVID-19 prevalence
        TASK = r"""1) Draw map matrix of South Carolina counties' monthly COVID-19 infection ratio with a weekly smooth in 2021.
        2) the infection ratio = (infection of this month / county popultion).
        """

        # API_DOC_LOCATION = [(1, r'https://raw.githubusercontent.com/gladcolor/LLM-Geo/master/COVID-19/CensusData_API_DOC.txt')]
        API_DOC_LOCATION = [(1, r'./COVID-19/CensusData_API_DOC.txt')]

        # [(Input_data_index, API_cocumentation_path)]

        DATA_LOCATIONS = [
            "COVID-19 data case in 2021 (county-level): https://github.com/nytimes/covid-19-data/raw/master/us-counties-2021.csv. It is a CSV file; there are 5 columns: date (format: 2021-02-01),county,state,fips,cases,deaths",
            "Population data: use Python library CensusData to obtain data. ",
            ]

        # add the API documentation to DATA_LOCATION
        for idx, path in API_DOC_LOCATION:
            with open(path, 'r', encoding='utf-8') as f:
                docs = f.readlines()
            docs = '\n'.join(docs)

            DATA_LOCATIONS[idx] += "The documentation is: \n" + docs

        task_name ='COVID-19_infection_rate'

        save_dir = os.path.join(os.getcwd(), task_name)
        os.makedirs(save_dir, exist_ok=True)

        # create graph
        # model=r"gpt-3.5-turbo"
        model = r"gpt-4"
        solution = Solution(
            task=TASK,
            task_name=task_name,
            save_dir=save_dir,
            data_locations=DATA_LOCATIONS,
            model=model,
        )
        print("Prompt to get solution graph:\n")
        print(solution.graph_prompt)

        response_for_graph = solution.get_LLM_response_for_graph()
        solution.graph_response = response_for_graph
        solution.save_solution()
        print()
        print("Code to generate solution graph: \n")
        print(solution.code_for_graph)

        self.assertEqual(True, True)  # add assertion here

    def test_get_ancestor_code(self):
        with open(r'E:\Research\LLM-Geo\Resident_at_risk_counting\Resident_at_risk_counting.pkl', 'rb') as f:
            solution = pickle.load(f)
        operations = solution.operations

        for idx, operation in enumerate(operations):
            print(operation['node_name'])
            ancestor_operations = solution.get_ancestor_operations(operation['node_name'])
            ancestor_operation_codes = '\n'.join([oper['operation_code'] for oper in ancestor_operations])
            print(ancestor_operations)
            print(f"operation {operation['node_name']}: \n", ancestor_operation_codes)

            descendant_operations = solution.get_descendant_operations(operation['node_name'])
            descendant_operations_definition = solution.get_descendant_operations_definition(descendant_operations)
            # print(f"descendant_operations_definition \n", descendant_operations_definition)

        self.assertEqual(True, True)  # add assertion here

    def test_get_prompt_for_an_opearation(self):
        # with open(r'E:\Research\LLM-Geo\Resident_at_risk_counting\Resident_at_risk_counting.pkl', 'rb') as f:
        with open(r'F:\Research\LLM-Geo\Resident_at_risk_counting\Resident_at_risk_counting.pkl', 'rb') as f:
            solution = pickle.load(f)

        solution.load_graph_file()
        solution.get_LLM_responses_for_operations()
        operations = solution.operations

        self.assertEqual(True, True)  # add assertion here

    def test_extractcontent_content_from_LLM_reply(self):
        prompt = 'Write a python program to compute the delta time. The code should be inside a python code block between : ```python\n```.'
        response = helper.get_LLM_reply(prompt=prompt)
        content = helper.extract_content_from_LLM_reply(response)
        print()
        print('-------------- Content ---------------: \n', content, '\n')
        code = helper.extract_code(response=response)
        print("-------------- Code ---------------: \n", code)
        self.assertEqual(True, True)




    def error_test(self):
        code = """a = 1/0
                """
        exec(code)
    def test_Error_exception(self):
        try:
            self.error_test()
        except Exception as e:
            error_class = e.__class__.__name__
            detail = e.args[0]
            cl, exc, tb = sys.exc_info()
            # message = traceback.StackSummary.extract(tb)
            # print(message)
            #

            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_details = traceback.extract_tb(exc_traceback)

            filename = traceback_details[-1].filename
            line_number = traceback_details[-1].lineno
            function_name = traceback_details[-1].name
            print(f"Exception occurred in file: {filename}")
            print(f"Line number: {line_number}")
            print(f"Function that caused the exception: {function_name}")
            print(f"Exception type: {exc_type.__name__}")
            print(f"Exception message: {exc_value}")

            line = traceback_details[0].line
            print(f"Line of code that caused the exception: {line}")

        self.assertEqual(True, True)



if __name__ == '__main__':
    unittest.main()


