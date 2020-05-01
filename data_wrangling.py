import requests
import csv
import json
from geopy.distance import geodesic
import numpy as np

# 167 dead end

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


def get_gps_data():
    construction_filename = 'data/Street_Closures_due_to_construction_activities_by_Intersection.csv'
    construction_header, construction_data = read_data(construction_filename)
    traffic_filename = 'data/Traffic_Volume_Counts__2014-2018_.csv'
    traffic_header, traffic_data = read_data(traffic_filename)

    construction = []
    construction_locations = {}
    for key in construction_data:
        construction_location = key[1]+'+'+key[2]+',+nyc'  # combine two street to locate the construction location
        construction_locations[construction_location] = construction_locations.get(construction_location, 0) + 1
        construction.append([construction_location, key[4], key[5], key[6]])
    construction_locations = list(construction_locations.keys())

    traffic = []
    traffic_locations = {}
    for key in traffic_data:
        FROM = (key[2]+'+'+key[3]+',+nyc').lower()  # combine two street to locate the construction location
        traffic_locations[FROM] = traffic_locations.get(FROM, 0) + 1
        TO = (key[2]+'+'+key[4]+',+nyc').lower()
        traffic_locations[TO] = traffic_locations.get(FROM, 0) + 1
        traffic.append([FROM,TO,key[6:30]])
    traffic_locations = list(traffic_locations.keys())

    TRAFFIC_LOCATIONS = {}
    for item in traffic_locations:
        try:
            url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + item + '&key=' +API_KEY
            r = requests.get(url)
            response_dict=r.json()
            if response_dict['status'] == 'OK':
                TRAFFIC_LOCATIONS[item] = [response_dict['results'][0]['formatted_address'], response_dict['results'][0]['geometry']['location']['lat'],
                         response_dict['results'][0]['geometry']['location']['lng']]
        except IndexError:
            pass
        continue
    print('traffic location finished')
    np.save("data/TRAFFIC_LOCATIONS.npy", TRAFFIC_LOCATIONS)

    CONSTRUCTION_LOCATIONS = {}
    for item in construction_locations:
        try:
            url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + item + '&key=' + API_KEY
            r = requests.get(url)
            response_dict=r.json()
            if response_dict['status'] == 'OK':
                CONSTRUCTION_LOCATIONS[item] = [response_dict['results'][0]['formatted_address'], response_dict['results'][0]['geometry']['location']['lat'],
                         response_dict['results'][0]['geometry']['location']['lng']]
        except IndexError:
            pass
        continue
    print('construction locations finished')

    construction_header = ['[formatted_address, lat, lng]', 'WORK_START_DATE', 'WORK_END_DATE', 'PURPOSE']
    traffic_header = ['From[formatted_address, lat, lng]', 'To[formatted_address, lat, lng]', 'Direction', 'Date', '12:00-1:00 AM',
                      '1:00-2:00AM', '2:00-3:00AM', '3:00-4:00AM','4:00-5:00AM', '5:00-6:00AM', '6:00-7:00AM', '7:00-8:00AM',
                      '8:00-9:00AM', '9:00-10:00AM', '10:00-11:00AM','11:00-12:00PM', '12:00-1:00PM', '1:00-2:00PM', '2:00-3:00PM',
                      '3:00-4:00PM', '4:00-5:00PM', '5:00-6:00PM','6:00-7:00PM', '7:00-8:00PM', '8:00-9:00PM', '9:00-10:00PM',
                      '10:00-11:00PM', '11:00-12:00AM']

    np.save("CONSTRUCTION_LOCATIONS.npy", CONSTRUCTION_LOCATIONS)


def filter(distance_threshold):
    construction_filename = 'data/Street_Closures_due_to_construction_activities_by_Intersection.csv'
    construction_header, construction_data = read_data(construction_filename)
    traffic_filename = 'data/Traffic_Volume_Counts__2014-2018_.csv'
    traffic_header, traffic_data = read_data(traffic_filename)
    constructions = np.load('data/CONSTRUCTION_LOCATIONS.npy', allow_pickle=True).item()
    traffic = np.load('data/TRAFFIC_LOCATIONS.npy', allow_pickle=True).item()



    construction_locations = {}
    for key in construction_data:
        construction_location = key[1] + '+' + key[
            2] + ',+nyc'  # combine two street to locate the construction location
        construction_locations[construction_location] = construction_locations.get(construction_location, 0) + 1
    construction_locations = list(construction_locations.keys())

    traffic_locations = {}
    for key in traffic_data:
        traffic_location = key[2] + '+' + key[3] + ',+nyc'
        # combine two street to locate the construction location
        traffic_locations[traffic_location] = key[2] + '+' + key[4] + ',+nyc'
    traffic_keys = list(traffic_locations.keys())
    # print(traffic_locations)
    # print(traffic)
    top = {}
    for item in construction_locations:
        tmp = []
        try:
            gps1 = constructions[item][1:3]
            for key in traffic_keys:
                FROM = traffic[key.lower()][1:3]
                TO = traffic[traffic_locations[key].lower()][1:3]
                MID = [(FROM[0]+TO[0])/2, (FROM[1]+TO[1])/2]
                dist = geodesic(gps1, MID).km
                if dist < distance_threshold:
                    tmp.append([key,dist])
            break
        except KeyError:
            pass
        if len(tmp) != 0:
            top[item] = tmp
        continue
    np.save('data/FILTER_RESULT.npy', top)

# get gps data from google map api
# get_gps_data()
distance_threshold = 1
filter(0.5)
data = np.load('data/FILTER_RESULT.npy', allow_pickle=True).item()
threshold = 5
i = 0
for key, value in data.items():
    if len(value) > 5:
        i += 1
        print(key,":",value)
print('number of constructions:', i)


