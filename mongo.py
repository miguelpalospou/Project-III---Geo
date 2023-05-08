import json
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster

from pymongo import MongoClient
import pandas as pd
import time
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
import pandas as pd

def connecting():
    client = MongoClient("localhost:27017")
    db = client["ironhack"]
    c = db.get_collection("companies")
    return c

def mongo_search(c):
    condition_1 =  {"total_money_raised": {"$regex": "M$|B$"}} 
    condition_2 = {"tag_list":{"$regex": "design"}}  
    condition_3 = {"offices.country_code": {"$exists": True}}   


    query = {"$and": [condition_1,condition_2, condition_3]}
         

    projection = {"offices.city":1,"offices.country_code":1, "offices.state_code":1,"offices.latitude":1,"offices.longitude":1,"name":1, "tag_list":1, "total_money_raised":1, "_id":0}

    df=list(c.find(query, projection))
    world_offices_data = pd.DataFrame(df)
    x= world_offices_data.iloc[0]["offices"]
    
    
    
    # Extract data for the first office
    world_offices_data["lat"] = world_offices_data["offices"].apply(lambda x: x[0]['latitude'] if len(x) >= 1 else None)
    world_offices_data["lon"] = world_offices_data["offices"].apply(lambda x: x[0]['longitude'] if len(x) >= 1 else None)
    world_offices_data["state_code"] = world_offices_data["offices"].apply(lambda x: x[0]['state_code'] if len(x) >= 1 else None)
    world_offices_data["country_code"] = world_offices_data["offices"].apply(lambda x: x[0]['country_code'] if len(x) >= 1 else None)
    world_offices_data["city"] = world_offices_data["offices"].apply(lambda x: x[0]['city'] if len(x) >= 1 else None)

    
    # Split rows with two offices into two separate rows
    world_offices_data = world_offices_data.explode("offices")

    
    # Extract data for the second office (new rows)
    world_offices_data["lat"] = world_offices_data["offices"].apply(lambda x: x['latitude'] if len(x) >= 2 else None)
    world_offices_data["lon"] = world_offices_data["offices"].apply(lambda x: x['longitude'] if len(x) >= 2 else None)
    world_offices_data["state_code"] = world_offices_data["offices"].apply(lambda x: x['state_code'] if len(x) >= 2 else None)
    world_offices_data["country_code"] = world_offices_data["offices"].apply(lambda x: x['country_code'] if len(x) >= 2 else None)
    world_offices_data["city"] = world_offices_data["offices"].apply(lambda x: x['city'] if len(x) >= 2 else None)  
    return world_offices_data

    
    
    
def cleaning_mongo(world_offices_data):
    # droping data where there are na values and reset index
    world_offices_data.dropna(axis=0, inplace=True)
    world_offices_data=world_offices_data.drop("offices", axis=1)
    world_offices_data = world_offices_data.reset_index()

    # filtering by city SF and MV, changing column name, droping 2 useless columns.
    world_offices_data2=world_offices_data[(world_offices_data.city == 'San Francisco') | (world_offices_data.city == 'Mountain View')]
    
    # creating categories columns which we will fill later with the count of each one:
    world_offices_data2 = world_offices_data2.rename(columns={'name': 'company_name'})
    world_offices_data2.drop(["index", "tag_list"], inplace=True, axis=1)
    world_offices_data2['schools'] = pd.Series(dtype='int')
    world_offices_data2['airports'] = pd.Series(dtype='int')
    world_offices_data2['train stations'] = pd.Series(dtype='int')
    world_offices_data2['clubs'] = pd.Series(dtype='int')
    world_offices_data2['vegan places'] = pd.Series(dtype='int')
    world_offices_data2['basketball places'] = pd.Series(dtype='int')
    world_offices_data2['pet grooming'] = pd.Series(dtype='int')
    
    df_sorted = world_offices_data2.sort_values(by='city')
    return df_sorted


    
    
    
    
    
    
    
    
    
    
    
    
    
    
