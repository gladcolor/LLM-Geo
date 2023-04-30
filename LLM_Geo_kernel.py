import LLM_Geo_Constants as constants
import helper
import os
import requests
import networkx as nx
import pandas as pd
import geopandas as gpd
from pyvis.network import Network
import openai
import pickle


class Solution():
    """
    class for the solution. Carefully maintain it.  
    
    by Huan Ning, 2023-04-28
    """
    def __init__(self, 
                 task, 
                 task_name,
                 save_dir,                
                 role=constants.graph_role,
                 model=r"gpt-3.5-turbo",
                 data_locations=[],
                 
                ):        
        self.task = task        
        self.solution_graph = None
        self.graph_response = None
        self.role = role
        self.data_locations=data_locations
        self.task_name = task_name   
        self.save_dir = save_dir
        self.code_for_graph = ""
        self.graph_file = os.path.join(self.save_dir, f"{self.task_name}.graphml")
        self.source_nodes = None
        self.sink_nodes = None
        self.operations = []
        self.assembly_prompt = ""
        
        self.parent_solution = None
        self.model = model
        
        self.assembly_LLM_response = ""
        self.code_for_assembly = ""
        self.graph_prompt = ""
         
        self.data_locations_str = '\n'.join([f"{idx + 1}. {line}" for idx, line in enumerate(self.data_locations)])     
        
        graph_requirement = constants.graph_requirement.copy()
        graph_requirement.append(f"Save the network into GraphML format, save it at: {self.graph_file}")
        graph_requirement_str =  '\n'.join([f"{idx + 1}. {line}" for idx, line in enumerate(graph_requirement)])
        
        graph_prompt = f'Your role: {self.role} \n' + \
               f'Task: {constants.graph_task_prefix} \n {self.task} \n' + \
               f'Data locations (each data is a node): {self.data_locations_str} \n' + \
               f'Your reply needs to meet these requirements: \n {graph_requirement_str} \n \n' + \
               f'Reply example: {constants.graph_reply_exmaple}'  
        
        self.graph_prompt = graph_prompt
        
    def get_LLM_response_for_graph(self):
        response = helper.get_LLM_reply(
                                        prompt=self.graph_prompt,
                                        system_role=self.role,
                                        model=self.model,
                                         )
        self.graph_response = response
        try:
            self.code_for_graph = helper.extract_code(response=self.graph_response, verbose=False)
        except Exception as e:
            self.code_for_graph = ""
            print("Extract graph Python code rom LLM failed.")

        return self.graph_response
        
    def load_graph_file(self, file=""):
        G = None
        if os.path.exists(file):
            self.graph_file = file
            G = nx.read_graphml(self.graph_file)
        else:
            
            if file == "" and os.path.exists(self.graph_file):
                G = nx.read_graphml(self.graph_file)
            else:
                print("Do not find the given graph file:", file)
                return None
        
        self.solution_graph = G
        
        self.source_nodes = helper.find_source_node(self.solution_graph)
        self.sink_nodes = helper.find_sink_node(self.solution_graph)
         
        return self.solution_graph 
              
    def get_prompts_for_operations(self):
        assert self.solution_graph, "Do not find solution graph!"
        def_list, data_node_list = helper.generate_function_def_list(self.solution_graph)

        
        for idx, function_def in enumerate(def_list): 
            operation_dict = function_def.copy()
            pre_requirements = [
                                f'The function description is: {function_def["description"]}',
                                f'The function definition is: {function_def["function_definition"]}',
                                f'The function return line is: {function_def["return_line"]}'
                               ]
            
            operation_requirement_str = '\n'.join([f"{idx + 1}. {line}" for idx, line in enumerate(
                pre_requirements + constants.operation_requirement)])
            
            operation_prompt = f'Your role: {constants.operation_role} \n' + \
                               f'operation_task: {constants.operation_task_prefix} {function_def["description"]} \n' + \
                               f'This function is one step to solve the question: {self.task} \n' + \
                               f'Data locations: {self.data_locations_str} \n' + \
                               f'Reply example: {constants.operation_reply_exmaple} \n' + \
                               f'Your reply needs to meet these requirements: \n {operation_requirement_str} \n \n' + \
                               f"All functions for the question are (node_name is function name): \n {def_list}"
            
            operation_dict['operation_prompt'] = operation_prompt 
            self.operations.append(operation_dict)
        return self.operations

    
    def get_LLM_responses_for_operations(self):
         
        if len(self.operations) == 0:
            self.get_prompts_for_operations()
            
        for idx, operation in enumerate(self.operations):
            
            print(f"{idx + 1} / {len(self.operations)}, {operation['node_name']}")
            prompt = operation['operation_prompt']
            
            if prompt == "":
                 self.get_prompts_for_operations()
            # print("prompt: \n", self.model, prompt)
            
            response = helper.get_LLM_reply(
                          prompt=prompt,
                          system_role=constants.operation_role,
                          model=self.model,
                          # model=r"gpt-4",
                         )
            # print(response)
            operation['response'] = response
            try:
                operation_code = helper.extract_code(response=operation['response'], verbose=False)
            except Exception as e:
                operation_code = ""
            operation['operation_code'] = operation_code
            
        return self.operations
            
            
    def prompt_for_assembly_program(self):
        all_operation_code_str = '\n'.join([operation['operation_code'] for operation in self.operations])
        # operation_code = solution.operations[-1]['operation_code']
        # assembly_prompt = f"" + \

        assembly_requirement = '\n'.join([f"{idx + 1}. {line}" for idx, line in enumerate(constants.assembly_requirement)])

        assembly_prompt = f"Your role: {constants.assembly_role} \n" + \
                          f"Your task is: use the given Python functions, return a complete Python program to solve the question: \n {self.task}" + \
                          f"Requirement: \n {assembly_requirement} \n" + \
                          f"Data location: \n {self.data_locations_str} \n" + \
                          f"Code: \n {all_operation_code_str}"
        
        self.assembly_prompt = assembly_prompt
        return self.assembly_prompt
    
    
    def get_LLM_assembly_response(self):
        self.prompt_for_assembly_program()
        assembly_LLM_response = helper.get_LLM_reply(self.assembly_prompt,
                          system_role=constants.assembly_role,
                          model=self.model,
                          # model=r"gpt-4",
                         )
        self.assembly_LLM_response = assembly_LLM_response
        self.code_for_assembly = helper.extract_code(self.assembly_LLM_response)
        
        try:
            code_for_assembly = helper.extract_code(response=self.assembly_LLM_response, verbose=False)
        except Exception as e:
                code_for_assembly = ""
        self.code_for_assembly = code_for_assembly
        
        return self.assembly_LLM_response
    
    def save_solution(self):
#         , graph=True
        new_name = os.path.join(self.save_dir, f"{self.task_name}.pkl")
        with open(new_name, "wb") as f:
            pickle.dump(self, f)
            
        # print("Saved solution as:", new_name)

