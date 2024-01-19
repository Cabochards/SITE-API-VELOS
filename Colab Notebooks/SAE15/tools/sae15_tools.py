import json
import urllib.request
import requests
import pandas as pd
import geopandas as gpd

def load_json_data(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        json_data = response.json()
        return json_data
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def loadVelibInformation():
    url = 'https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json'
    return load_json_data(url)

def loadVelibStatus():
    url = 'https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json'
    return load_json_data(url)

def getVelibStations(json_data):
    return json_data.get('data', {}).get('stations', [])

def exportToGeoDF(data_df):
    geom = gpd.points_from_xy(data_df["lon"], data_df["lat"])
    data_geodf = gpd.GeoDataFrame(data_df, crs="EPSG:4326", geometry=geom)
    return data_geodf
