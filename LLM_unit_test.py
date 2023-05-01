import unittest
import  LLM_Geo_Constants as constants
import LLM_Geo_kernel
import helper
import pickle
import os
import networkx as nx

class MyTestCase(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()


