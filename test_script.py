#!/usr/bin/env python3
import requests

# Your API key
API_KEY = '70Y87Slx2OFOyrlikj0v6yoxZ7cgGYvZ'  # Replace with your actual API key

# Stop key for Park Lane
stop_key = 's-gcvy4z9ws3-parklane'
next_departure_seconds = 1200  # Time frame in seconds
limit = 8  # Limit the number of records

# Construct the URL
url = f'https://transit.land/api/v2/rest/stops/s-gcvy4z9ws3-parklane/departures?next=12000&limit=4'
print(f"Requesting URL: {url}")  # Debugging output

# Send the request
try:
    response = requests.get(url, headers={'apikey': API_KEY})
    print(f"Response Status Code: {response.status_code}")  # Debugging output

    # Check the response
    if response.status_code == 200:
        departures = response.json()  # Parse the JSON response
        
        # Extract and print specific information for buses 26 and 44
        for stop in departures['stops']:
            for departure in stop['departures']:
                scheduled_time = departure['departure']['scheduled']
                route_name = departure['trip']['route']['route_short_name']
                trip_headsign = departure['trip']['trip_headsign']
                
                # Check if the route is 26 or 44
                if route_name in ['26', '44', 'N26']:
                    print(f"Next bus: {route_name} to {trip_headsign} at {scheduled_time}")
    else:
        print(f"Error: {response.status_code} - {response.text}")  # Output error message
except Exception as e:
    print(f"An error occurred: {e}")  # Print any exceptions that occur

input("Press Enter to exit...")  # Wait for user input before closing