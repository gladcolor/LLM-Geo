# Autonomous GIS: the next-generation AI-powered GIS
GIS stands for Geographic Information System; one of its major functionality is to conduct spatial analysis, manually, in the current stage. However, we implement **Autonomous GIS**, which aims to execute spatial analysis autonomously with little or no human intervention. 



# Introduction
Large Language Models (LLMs), such as ChatGPT, demonstrate a strong understanding of human natural language and have been explored and applied in various fields, including reasoning, creative writing, code generation, translation, and information retrieval. 

By adopting LLM as the reasoning core, we implement Autonomous GIS, an AI-powered geographic information system (GIS) that leverages the LLM’s general abilities in natural language understanding, reasoning and coding for addressing spatial problems with automatic spatial data collection, analysis and visualization. We envision that autonomous GIS will need to achieve five autonomous goals including **self-generating, self-organizing, self-verifying, self-executing, and self-growing**. We developed a prototype system called LLM-Geo using GPT-4 API in a Python environment, demonstrating what an autonomous GIS looks like and how it delivers expected results without human intervention using two case studies. 

For two case studies, LLM-Geo successfully returned accurate results, including aggregated numbers, graphs, and maps, significantly reducing manual operation time. Although still lacking several important modules such as logging and code testing, LLM-Geo demonstrates a potential path towards next-generation AI-powered GIS. We advocate for the GIScience community to dedicate more effort to the research and development of autonomous GIS, making spatial analysis easier, faster, and more accessible to a broader audience. 

![img_1.png](images/img_1.png)
Overall workflow of LLM-Geo


See our paper here: Autonomous GIS: the next-generation AI-powered GIS, [https://arxiv.org/abs/2305.06453](https://arxiv.org/abs/2305.06453). If you find our work is useful, please cite as: `Autonomous GIS: the next-generation AI-powered GIS. Zhenlong Li and Huan Ning. 2023. https://doi.org/10.48550/arXiv.2305.06453`

Note:  We are still developing LLM-Geo, and the ideas presented in the paper may change due to the rapid development of AI. For instance, the token limitation appears to have been overcome by [Claude](https://www.anthropic.com/index/100k-context-windows) (released on 2023-05-11). We hope LLM-Geo can inspire GIScience professionals to further investigate more on autonomous GIS.    

# Installation

Clone or download the repository, rename `your_config.ini` as `config.ini`. Then put your OpenAI API key in the `config.ini` file. Please use GPT-4, the lower versions such as 3.5 do no have enougth reaasoning ability to generate correct solution grahp and operation code.

If you have difficulties to install `GeoPandas` in Windows, refer to this [post](https://geoffboeing.com/2014/09/using-geopandas-windows/). 


# How to use
- Download all files, put your question to the `TASK` variable in LLM-Geo4.ipynb.
- Set the `task_name` in the notebook. Space is not allowed. LLM-Geo will create the fold using the `task_name' to save results.
- Run all cells.

# Case study
These case studies are carefully design to show the concepts of autonomous GIS. Please use GPT-4; the lower version of GPT will fail to generate correct code and results. Note everytime GPT-4 generate different outputs, so your results may look different. Per our test, the generated program may not success everytime, but there 80% chance to run successfully. If input the generated prompts to the ChatGPT-4 chat box rather than API, the success rate will higher. We will improve the overall workflow of LLM-Geo, currently we do not push entire historical conversation (i.e., sufficient information) to GPT-4 API.

## Case 1: Counting population living near hazardous wastes.
This spatial problem is to find out the population living with hazardous wastes and map their distribution. The study area is North Carolina, United States (US). We input the task (question) to LLM-Geo as:
```
Task:
1) Find out the total population that lives within a tract that contain hazardous waste facilities. The study area is North Carolina, US.
2) Generate a map to show the spatial distribution of population at the tract level and highlight the borders of tracts that have hazardous waste facilities.

Data locations: 
1. NC hazardous waste facility ESRI shape file location: https://github.com/gladcolor/LLM- Geo/raw/master/overlay_analysis/Hazardous_Waste_Sites.zip
2. NC tract boundary shapefile location: https://github.com/gladcolor/LLM-Geo/raw/master/overlay_analysis/tract_shp_37.zip. The tract id column is 'Tract'
3. NC tract population CSV file location: https://github.com/gladcolor/LLM-Geo/raw/master/overlay_analysis/NC_tract_population.csv. The population is stored in 'TotalPopulation' column. The tract ID column is 'GEOID'
```
The results are: (a) Solution graph, (b) assembly program (Python codes), and (c) returned population count and generated map. 
![img_2.png](images/img_2.png)


## Case 2: Human mobility data retrieval and trend visualization.
This task is to investigate the mobility changes during COVID-19 pandemic in France 2020. First, we asked LLM-Geo to retrieve mobility data from the ODT Explorer using [REST API](https://github.com/GIBDUSC/ODT_Flow), and then compute and visualize the monthly change rate compared to January 2020. . We input the task (question) to LLM-Geo as:
```
Task: 
1) Show the monthly change rates of population mobility for each administrative regions in a France map. Each month is a sub-map in a map matrix. The base of the change rate is January 2020. 
2) Draw a line chart to show the monthly change rate trends of all administrative regions.

Data locations: 
1. ESRI shapefile for France administrative regions: https://github.com/gladcolor/LLM-Geo/raw/master/REST_API/France.zip. The 'GID_1' column is the administrative region code, 'NAME_1' column is the administrative region name.
2. REST API URL with parameters for mobility data access: http://gis.cas.sc.edu/GeoAnalytics/REST?operation=get_daily_movement_for_all_places&source=twitter&scale=world_first_level_admin&begin=01/01/2020&end=12/31/2020. The response is in CSV format. There are three columns in the response: place, date (format:2020-01-07), and intra_movement. 'place' column is the administrative region code, France administrative regions start with 'FRA'.
```
The results are: (a) Solution graph, (b) map matrix showing the spatial distribution of mobility change rate, (c) line chart showing the trend of the mobility change rate, (d) assembly program. 
![img_2.png](images/img_3.png)


# To Do
- Add more case studies.
- Improve the prompt generation.
- Implement autonomous data collection module.

