import requests

# Get station info for CA
# GET https://www.ncdc.noaa.gov/cdo-web/api/v2/stations?locationid=FIPS:23&limit=5&sortfield=mindate
base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations'
dataset_id = 'GHCND'
#locationid = 'FIPS:06'
locationid = 'ZIP:95060'
location = '36.974,237.969' #122.031
radius = '25'  # Search radius in miles
# Set the request headers
headers = {'token': 'YOURTOKENHERE'}
# Send the web request
response = requests.get(base_url, headers=headers, params={
    'datasetid': dataset_id,
    #'location': location,
    'locationid': locationid,
    'radius': radius,  # Maximum number of records to retrieve per request
    'limit': 1000
})
# Check if the request was successful
if response.status_code == 200:
    # Retrieve the JSON data from the response
    json_data = response.json()
    # Extract the station names
    station_data = []
    for result in json_data['results']:
        station_data.append((result['name'], result['id']))
    # Display the data
    print(f'{"Name":^40}{"ID":^15}')
    for name, sid in station_data:
        print(f'{name:^40}{sid:^15}')
else:
    # Display the error message
    print(f'Error: {response.status_code} - {response.reason}')

for name, sid in station_data:
    if "SANTA" in name:
        print(f'{name:^40}{sid:^15}')

# Find Santa Cruz County code
# https://www.ncdc.noaa.gov/cdo-web/api/v2/&state=<state abbreviation>&limit=1
base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/locations'
locationcategoryid = 'COUNTY'
state_abbr = 'CA'
county_name = 'Santa Cruz'
# Set the request headers
headers = {'token': 'YOURTOKENHERE'}
# Send the web request
response = requests.get(base_url, headers=headers, params={
    'locationcategoryid': locationcategoryid,
    'name' : county_name,
    'locationid': locationid,
    'state': state_abbr,
    'limit': 10
})
# Check if the request was successful
if response.status_code == 200:
    # Retrieve the JSON data from the response
    json_data = response.json()
    # Extract the station names
    station_data = []
    for result in json_data['results']:
        station_data.append((result['name'], result['id']))
    # Display the data
    print(f'{"Name":^40}{"ID":^15}')
    for name, sid in station_data:
        print(f'{name:^40}{sid:^15}')
else:
    # Display the error message
    print(f'Error: {response.status_code} - {response.reason}')



# See if we can correlate with rainfall
# ChatGPT said Santa Cruz is CITY:US060013, which is actually Los Angeles
base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'
location_id = 'US1CAZ0055'
dataset_id = 'GHCND'
data_type_id = 'PRCP'
start_date = '2022-01-01'
end_date = '2022-12-31'
# Set the request headers
headers = {'token': 'YOURTOKENHERE'}
# Send the web request
response = requests.get(base_url, headers=headers, params={
    'datasetid': dataset_id,
    'datatypeid': data_type_id,
    'stationid': location_id,
    'startdate': start_date,
    'enddate': end_date,
    'limit': 1000,  # Maximum number of records to retrieve per request
})
# Check if the request was successful
if response.status_code == 200:
    # Retrieve the JSON data from the response
    json_data = response.json()
    # Extract the rainfall data from the JSON data
    rainfall_data = []
    for result in json_data['results']:
        rainfall_data.append((result['date'], result['value']))
    # Display the rainfall data
    # print('Date\tRainfall')
    # for date, rainfall in rainfall_data:
    #     print(f'{date}\t{rainfall}')
else:
    # Display the error message
    print(f'Error: {response.status_code} - {response.reason}')


# Set up API request parameters
#station_id = 'GHCND:US1CAZ0055'
station_ids = ['GHCND:US1CASZ0047',
               'GHCND:US1CASZ0048',
               'GHCND:US1CASZ0049',
               'GHCND:US1CASZ0058',
               'GHCND:USC00047916',
               'GHCND:USR0000CBNL',
               'GHCND:US1CASZ0029']
               
# Set up API headers and authentication
headers = {'token': 'YOURTOKENHERE'}

for station_id in station_ids:
    url = f'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations/{station_id}'
    
    # Send API request and parse JSON response
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Print station information
    print('Station name:', data['name'])
    print('Latitude:', data['latitude'])
    print('Longitude:', data['longitude'])
    print('Elevation (meters):', data['elevation'])
    print('MinDate:', data['mindate'])
    print('MaxDate:', data['maxdate'])



base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'
station_id = 'GHCND:US1CASZ0058'
#station_id = 'GHCND:US1CASZ0048' # only worked for a few days of the time
dataset_id = 'GHCND'
data_type_id = 'PRCP'
start_date = '2022-01-01'
end_date = '2022-12-31'
# Set the request headers
headers = {'token': 'YOURTOKENHERE'}
# Send the web request
response = requests.get(base_url, headers=headers, params={
    'datasetid': dataset_id,
    'datatypeid': data_type_id,
    'stationid': station_id,
    'startdate': start_date,
    'enddate': end_date,
    'limit': 1000  # Maximum number of records to retrieve per request
})
# Check if the request was successful
if response.status_code == 200:
    # Retrieve the JSON data from the response
    json_data = response.json()
    # Extract the rainfall data from the JSON data
    rainfall_data = []
    for result in json_data['results']:
        rainfall_data.append((result['date'].split('T')[0], result['value']))
    # Display the rainfall data
    # print('Date\tRainfall')
    # for date, rainfall in rainfall_data:
    #     print(f'{date}\t{rainfall}')
else:
    # Display the error message
    print(f'Error: {response.status_code} - {response.reason}')

rf_data = rainfall_data.copy()

import csv
of = 'santa_cruz_rain_2022.csv'
with open(of, 'w', newline='') as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)
    # Write the header row, if needed
    csv_writer.writerow(['Date', 'Rain 0.1mm'])
    # Write each tuple as a row in the CSV file
    for row in rainfall_data:
        csv_writer.writerow(row)