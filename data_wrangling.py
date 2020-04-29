import requests
import csv
import json
import geopy


# get the google api key
with open("env/config.json", 'r') as f:
    temp = json.loads(f.read())
API_KEY = temp['GOOGLE']['API_KEY']


def read_data(filename):
    header = []
    data = []
    i = 0
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if i == 0:
                header = row
            else:
                data.append(row)
            i += 1
    return header, data


construction_filename = 'data/Street_Closures_due_to_construction_activities_by_Intersection.csv'

construction_header, construction_data = read_data(construction_filename)
print(construction_header,'\n')

traffic_filename = 'data/Traffic_Volume_Counts__2014-2018_.csv'
traffic_header,traffic_data = read_data(traffic_filename)
print(traffic_header,'\n')

dict = {}
for key in construction_data:
    construction_location = key[1]+'+'+key[2]+',+nyc'  # combine two street to locate the construction location
    dict[construction_location] = dict.get(construction_location, 0) + 1
construction_location = list(dict.keys())

dict = {}
for key in traffic_data:
    traffic_location = key[2]+'+'+key[3]+',+nyc'  # combine two street to locate the construction location
    dict[traffic_location] = dict.get(traffic_location, 0) + 1
traffic_location = list(dict.keys())

# url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+ traffic_location[0]+'&key='+API_KEY
# r = requests.get(url)
# response_dict=r.json()
response_dict = {'results': [{'address_components': [{'long_name': '3rd Avenue & East 154th Street', 'short_name': '3rd Ave & E 154th St', 'types': ['intersection']}, {'long_name': 'Woodstock', 'short_name': 'Woodstock', 'types': ['neighborhood', 'political']}, {'long_name': 'The Bronx', 'short_name': 'The Bronx', 'types': ['political', 'sublocality', 'sublocality_level_1']}, {'long_name': 'Bronx County', 'short_name': 'Bronx County', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'New York', 'short_name': 'NY', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United States', 'short_name': 'US', 'types': ['country', 'political']}, {'long_name': '10455', 'short_name': '10455', 'types': ['postal_code']}], 'formatted_address': '3rd Ave & E 154th St, The Bronx, NY 10455, USA', 'geometry': {'location': {'lat': 40.818951, 'lng': -73.9140388}, 'location_type': 'GEOMETRIC_CENTER', 'viewport': {'northeast': {'lat': 40.82029998029149, 'lng': -73.9126898197085}, 'southwest': {'lat': 40.8176020197085, 'lng': -73.91538778029151}}}, 'place_id': 'Ei4zcmQgQXZlICYgRSAxNTR0aCBTdCwgVGhlIEJyb254LCBOWSAxMDQ1NSwgVVNBImYiZAoUChIJl12VjMn1wokR2g_fyWtTbJASFAoSCZddlYzJ9cKJEdoP38lrU2yQGhQKEgml9NL9R_TCiRHXPohktnFNuhoUChIJm7Udfcn1wokRzAf0hmBZqloiCg1GelQYFdyc8dM', 'types': ['intersection']}], 'status': 'OK'}
print(response_dict['results'][0]['formatted_address'])
print(response_dict['results'][0]['geometry']['location'])

