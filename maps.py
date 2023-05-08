import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
import pandas as pd


def initial_map(world_offices_data):
    
    usa_lat = 37.7576171
    usa_lon = -122.5776844
    usa_map = Map(location=[usa_lat, usa_lon], zoom_start=3)
    markers = []
    for index, row in world_offices_data.iterrows():
        all_together = {"location": [row["lat"], row["lon"]]}
        icon = Icon (
                    icon = "building",
                    prefix = "fa",
                    color = "ce40c2",
                    icon_color = "white")        

        # 2. With the icon: I pass that to the Marker
        new_marker = Marker(**all_together, icon=icon)

        # 3. Add a Marker per row
        markers.append(new_marker)

    # Add all the markers to the map
    for marker in markers:
        marker.add_to(usa_map)

    return usa_map

def final_map(dfs):

    usa_lat = 37.7653307
    usa_lon = -122.419473616
    usa_map = Map(location = [usa_lat, usa_lon], zoom_start = 13)
    for df in dfs:
        for index, row in df.iterrows():

            all_together = {"location": [row["lat"], row["lon"]]}

            if row["category"] == "Child Care Service" or row["category"] == "Preschool":
                icon = Icon (
                    icon = "graduation-cap",
                    prefix = "fa",
                    color = "blue",
                    icon_color = "white")

            elif row["category"] == "Metro Station":
                icon = Icon (
                    icon = "train-tram",
                    prefix = "fa",
                    color = "beige",
                    icon_color = "black")

            elif row["category"] == "Night Club":
                icon = Icon (
                    icon = "champagne-glasses",
                    prefix = "fa",
                    color = "lightblue",
                    icon_color = "black") 

            elif row["category"] == "vegan":
                icon = Icon (
                    icon = "leaf",
                    prefix = "fa",
                    color = "yellow",
                    icon_color = "black")


            elif row["category"] == "Basketball Court":
                icon = Icon (
                    icon = "basketball",
                    prefix = "fa",
                    color = "green",
                    icon_color = "white")

            elif row["category"] == "Pet Grooming Service":
                icon = Icon (
                    icon = "dog",
                    prefix = "fa",
                    color = "orange",
                    icon_color = "white")



        # 2. With the icon: I pass that to the Marker

            new_marker = Marker(**all_together, icon = icon)

        # 3. Add a Marker per row

            new_marker.add_to(usa_map)

    return usa_map
