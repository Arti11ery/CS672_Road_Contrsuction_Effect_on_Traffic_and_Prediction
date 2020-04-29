import requests
import csv
import json
import geopy

API_KEY = 'AIzaSyDaIsQTEAUdSGGk1Ia7OuwsUJhEZy6ZhFg'
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

url = 'https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key='+API_KEY
r = requests.get(url)
response_dict=r.json()
print(response_dict)

