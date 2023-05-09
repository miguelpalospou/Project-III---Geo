from getpass import getpass
from dotenv import load_dotenv
import os
import requests
import pandas as pd
# foursquare categories to search


preschool_c = "12056"
airport_c = "19040"
train_station_c = "19046"
nightlife_spot_c = "10032"
vegetarian_vegan_c = "13377"
basketball_stadium_c = "18008"
pet_grooming_c = "11062"





def query_from_foursquare (query, lat, lon, radius, categories):
    
    load_dotenv()
    token = os.getenv("token")
    url = f"https://api.foursquare.com/v3/places/search?query={query}&ll={lat}%2C{lon}&radius={radius}&categories={categories}"

    headers = {
        "accept": "application/json",
        "Authorization": token
    }

    response = requests.get(url, headers=headers).json()
    return response





def factor_from_foursquare(one_element):
    
    ## Here I am taking the info that I need from the response.

    

    
    
    name = one_element["name"]
    distance = one_element["distance"]
    address = one_element["location"]["formatted_address"]
    lat = one_element["geocodes"]["main"]["latitude"]
    lon = one_element["geocodes"]["main"]["longitude"]
    category = one_element["categories"][0]["name"]
    
    dict_ = {"name": name, "distance": distance, "lat": lat, "lon": lon, "category":category}
    
    return dict_

    #### Here I'm creating a list of dataframes, I set the categories I want to loop through
    ####  I then loop through the categories and again through our main dataframe with the list
    #### of the potential offices (df_sorted)
    
def categories(df_sorted):
    
    dfs = []

    categories = ["12056", "19040", "19046", "10032", "13377", "18008", "11134"]

    for category in categories:
        category_df = pd.DataFrame(columns=["name", "distance", "lat", "lon", "category"])
        for index, row in df_sorted.iterrows():
            lat = row['lat']
            lon = row['lon']
            name = row['company_name']
            city = row['city']

            response = query_from_foursquare("", lat, lon, 1000, category)

            new_list = []
            for i in response["results"]:
                factor_dict = factor_from_foursquare(i)
                factor_dict['company_name'] = name
                factor_dict['city'] = city
                new_list.append(factor_dict)

            # append results to category dataframe


            category_df = category_df.append(new_list, ignore_index=True)

        dfs.append(category_df)
    

    dfs[4]['category'] = 'vegan'
    dfs[1] = dfs[1].assign(company_name="", city="")
    return dfs
    
def count_category(df_sorted,dfs):
    
# Here the idea is to count the number of locations for each category and for each office and add it to our main
# dataframe, which is df_sorted. As you can see I do "df_sorted.columns[7:]" to start iterating on the 7th column,
# because that's where I will be starting adding the count.

# Iterate through columns of df_sorted
    for i, col in enumerate(df_sorted.columns[7:]):

        # Count the number of rows in dfs[i] for each company name in df_sorted
        counts = []
        for index, row in df_sorted.iterrows():
            company_name = row["company_name"]
            count = dfs[i][dfs[i]["company_name"] == company_name].shape[0]
            counts.append(count)

        # Update the corresponding column in df_sorted with the counts
        df_sorted.iloc[:, i+7] = counts
        df_sorted = df_sorted.assign(weight_metric="")
        df_sorted["weight_metric"] = df_sorted.apply(lambda row: row["schools"]*0.2 + row["airports"]*0.2 + row["train stations"]*0.2 + row["clubs"]*0.1 + row["vegan places"]*0.1 + row["basketball places"]*0.1 + row["pet grooming"]*0.1, axis=1)
    return df_sorted


    
    






