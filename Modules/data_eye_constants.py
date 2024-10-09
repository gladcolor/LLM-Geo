from pydantic import BaseModel
# from openai import OpenAI

table_formats = ["CSV", 'Parquet', "TXT"]
vector_formats = ["ESRI shapefile", "GeoPackage", "KML"]
raster_formats = ["Tiff", "JPEG", "PNG", "ERDAS IMG", "JP2", "HDF5" "HDF"]

support_formats = table_formats + vector_formats + raster_formats


role = r'''A professional Geo-information scientist and programmer good at Python. You have worked on Geographic information science more than 20 years, and know every detail and pitfall when processing spatial data and coding. You are a very careful person to follow instruction exactly in work.
'''

mission_prefix = fr'''You will be provided with brief geospatial data description and locations for a spatial analysis task.
You need to extract the data path, URL, API, an format from a task and data description. Every given data should be included, and keep the original order.
Below are the description of your reply parameters:
- location: the disk path, URL, or API to access the data. Such as r"C:\test.zip".
- format: the format of data, which belongs one of {support_formats}.
'''
# ['TXT', 'CSV', 'Parquet', 'ESRI shapefile', 'KML', 'HDF', 'HDF5', 'LAS/LAZ', 'XLS', 'GML', 'GeoPackage', 'Tiff', 'JPEG', 'JP2', 'PNG', 'ERDAS IMG", 'URL', 'REST API', 'other']

class Data(BaseModel):
    location: str
    format: str


class Data_locations(BaseModel):
    data_locations: list[Data]


print("mission_prefix:", mission_prefix)
