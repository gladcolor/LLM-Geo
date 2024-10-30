import sys
import os
import time
import pandas as pd
import geopandas as gpd
import rasterio
import rasterio.features
import rasterio.warp

from pydantic import BaseModel
from openai import OpenAI

import configparser
import json
from collections import OrderedDict


module_path = os.path.abspath(os.path.join('..', 'helper'))
if module_path not in sys.path:
    sys.path.append(module_path)

module_path = os.path.abspath(os.path.join('.', 'data_eye_constants'))
if module_path not in sys.path:
    sys.path.append(module_path)

import sys
# sys.path.append(".")
# import data_eye_constants as constants
import data_eye_constants as eye_constants

# import helper

config = configparser.ConfigParser()
config.read('config.ini')

# use your KEY.
OpenAI_key = config.get('API_Key', 'OpenAI_key')

client = OpenAI(api_key=OpenAI_key)


def get_data_overview(data_location_dict):
    data_locations = data_location_dict['data_locations']
    # print()
    for data in data_locations:
        try:
            meta_str = ''
            format_ = data['format']
            data_path = data['location']

            # print("data_path:", data_path)

            if format_ in eye_constants.vector_formats:
                meta_str = see_vector(data_path)

            if format_ in eye_constants.table_formats:
                meta_str = see_table(data_path)

            if format_ in eye_constants.raster_formats:
                meta_str = see_raster(data_path)

            data['meta_str'] = meta_str

        except Exception as e:
            print("Error in get_data_overview()", data, e)
    return data_location_dict

def add_data_overview_to_data_location(task, data_location_list, model = r'gpt-4o-2024-08-06'):
    prompt = get_prompt_to_pick_up_data_locations(task=task,
                                                  data_locations=data_location_list)
    response = get_LLM_reply(prompt=prompt,
                                    model=model)
    # pprint.pp(result.choices[0].message)
    attributes_json = json.loads(response.choices[0].message.content)
    get_data_overview(attributes_json)

    for idx, data in enumerate(attributes_json['data_locations']):
        meta_str = data['meta_str']
        data_location_list[idx] += data_location_list[idx] + " Data overview: " + meta_str
    return attributes_json, data_location_list

def get_prompt_to_pick_up_data_locations(task, data_locations):
    data_locations_str = '\n'.join([f"{idx + 1}. {line}" for idx, line in enumerate(data_locations)])
    prompt = f'Your mission: {eye_constants.mission_prefix} \n\n' + \
             f'Given task description: {task} \n' + \
             f'Data location: \n{data_locations_str}'
    return prompt
def see_table(file_path):
    # print("OK")
    # print(file_path)
    # print(file_path[-3:])
    df = None
    if file_path[-4:].lower() == '.csv':
        # print(file_path)
        df = pd.read_csv(file_path)
        sample_df = pd.read_csv(file_path, dtype=str)
    # get_df_types_str
    types_str = '| '.join([f"{col}: {dtype}, {sample_df.iloc[0][col]} " for col, dtype in df.dtypes.items()])
    types_str = f"column names, data types, and sample values (column_name: data_type, sample value |):[{types_str}]"
    meta_str = types_str

    return meta_str

def _get_df_types_str(df):
    samples = df.sample(1)
    # print("samples:", samples)
    types_str = '| '.join([f"{col}: {dtype}, {samples.iloc[0][col]}" for col, dtype in df.dtypes.items()])
    types_str = f"column names, data types, and sample values (column_name: data_type, sample value |):[{types_str}]"
    return types_str

def see_vector(file_path):
    gdf = gpd.read_file(file_path)
    types_str = _get_df_types_str(gdf.drop(columns='geometry'))
    # print(gdf.crs)
    crs_summary = str(gdf.crs)  # will be "EPSG:4326", but the original information would be long
    crs_summary = crs_summary.replace('\n', '\t')
    meta_str = str({"column names and data types": types_str, "Coordinate reference system": crs_summary})

    return meta_str

def see_raster(file_path, statistics=False, approx=False):
    with rasterio.open(file_path) as dataset:
        raster_str = _get_raster_str(dataset, statistics=statistics, approx=approx)

    return raster_str

# def _get_raster_str(dataset, statistics=False, approx=False):  # receive rasterio object
#     raster_dict = dataset.meta
#     raster_dict["band_count"] = raster_dict.pop("count") # rename the key
#     raster_dict["bounds"] = dataset.bounds
#     if statistics:
#         band_stat_dict = {}
#         for i in range(1, raster_dict["band_count"] + 1):
#               # need time to do that
#             band_stat_dict[f"band_{i}"] = dataset.stats(i, approx=approx)
#         raster_dict["statistics"] = band_stat_dict
#
#     resolution = (dataset.transform[0], dataset.transform[4])
#     raster_dict["resolution"] = resolution
#     # print("dataset.crs:", dataset.crs)

def _get_raster_str(dataset, statistics=False, approx=False):  # receive rasterio object
    raster_dict = dataset.meta
    raster_dict["band_count"] = raster_dict.pop("count") # rename the key
    raster_dict["bounds"] = dataset.bounds
    if statistics:
        band_stat_dict = {}
        for i in range(1, raster_dict["band_count"] + 1):
              # need time to do that
            band_stat_dict[f"band_{i}"] = dataset.stats(indexes=i, approx=approx)
        raster_dict["statistics"] = band_stat_dict

    resolution = (dataset.transform[0], dataset.transform[4])
    raster_dict["resolution"] = resolution
    # print("dataset.crs:", dataset.crs)

    crs = dataset.crs

    if crs:
        if dataset.crs.is_projected:
            raster_dict["unit"] = dataset.crs.linear_units
        else:
            raster_dict["unit"] = "degree"
    else:
        raster_dict["Coordinate reference system"] = "unknown"
    # print("dataset.crs:", dataset.crs)

    raster_str = str(raster_dict)
    return raster_str

# beta vervsion of using structured output. # https://cookbook.openai.com/examples/structured_outputs_intro
# https://platform.openai.com/docs/guides/structured-outputs/examples
def get_LLM_reply(prompt,
                  model=r"gpt-4o",
                  verbose=True,
                  temperature=1,
                  stream=True,
                  retry_cnt=3,
                  sleep_sec=10,
                  ):
    # Generate prompt for ChatGPT
    # url = "https://github.com/gladcolor/LLM-Geo/raw/master/overlay_analysis/NC_tract_population.csv"
    # prompt = prompt + url

    # Query ChatGPT with the prompt
    # if verbose:
    #     print("Geting LLM reply... \n")
    count = 0
    isSucceed = False
    while (not isSucceed) and (count < retry_cnt):
        try:
            count += 1
            response = client.beta.chat.completions.parse(model=model,
                                                      messages=[
                                                          {"role": "system", "content": eye_constants.role},
                                                          {"role": "user", "content": prompt},
                                                      ],
                                                      temperature=temperature,
                                                      response_format=eye_constants.Data_locations,
                                                       )
        except Exception as e:
            # logging.error(f"Error in get_LLM_reply(), will sleep {sleep_sec} seconds, then retry {count}/{retry_cnt}: \n", e)
            print(f"Error in get_LLM_reply(), will sleep {sleep_sec} seconds, then retry {count}/{retry_cnt}: \n",
                  e)
            time.sleep(sleep_sec)

    return response
