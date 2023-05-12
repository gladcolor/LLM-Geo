# Autonomous GIS: the next-generation AI-powered GIS


# Introduction
![imLarge Language Models (LLMs), such as ChatGPT, demonstrate a strong understanding of human natural language and have been explored and applied in various fields, including reasoning, creative writing, code generation, translation, and information retrieval. 

By adopting LLM as the reasoning core, we propose Autonomous GIS, an AI-powered geographic information system (GIS) that leverages the LLM’s general abilities in natural language understanding, reasoning and coding for addressing spatial problems with automatic spatial data collection, analysis and visualization. We envision that autonomous GIS will need to achieve five autonomous goals including **self-generating, self-organizing, self-verifying, self-executing, and self-growing**. 

We introduce the design principles of autonomous GIS to achieve these five autonomous goals from the aspects of **information sufficiency, LLM ability, and agent architecture**. We developed a prototype system called LLM-Geo using GPT-4 API in a Python environment, demonstrating what an autonomous GIS looks like and how it delivers expected results without human intervention using two case studies. 

For both case studies, LLM-Geo successfully returned accurate results, including aggregated numbers, graphs, and maps, significantly reducing manual operation time. Although still lacking several important modules such as logging and code testing, LLM-Geo demonstrates a potential path towards next-generation AI-powered GIS. We advocate for the GIScience community to dedicate more effort to the research and development of autonomous GIS, making spatial analysis easier, faster, and more accessible to a broader audience.g_1.png](img_1.png)
h1: 

See our paper here: Autonomous GIS: the next-generation AI-powered GIS, [https://arxiv.org/abs/2305.06453](https://arxiv.org/abs/2305.06453)

Note:  We are still developing LLM-Geo, and the ideas presented in the paper may change due to the rapid development of AI. For instance, the token limitation appears to have been overcome by [Claude](https://www.anthropic.com/index/100k-context-windows) (released on 2023-05-11). We hope LLM-Geo can inspire GIScience professionals to further investigate more on autonomous GIS.    

# Installation

Clone or download the repository, rename `your_config.ini` as `config.ini`. Then put your OpenAI API key in the `config.ini` file. Please use GPT-4, the lower versions such as 3.5 do no have enougth reaasoning ability to generate correct solution grahp and operation code.


# How to use

Download all files, put your question to the `TASK` variable in LLM-Geo4.ipynb, then runn all cells.

Set the `task_name` in the notebook. Space is not allowed. LLM-Geo will create the fold using the `task_name' to save results.

# Case 1: Counting population living near hazardous wastes.


