#!/usr/bin/env python3
import requests
from datetime import datetime, timedelta
import time

# Your API key
API_KEY = '70Y87Slx2OFOyrlikj0v6yoxZ7cgGYvZ'  # Replace with your actual API key

# Stop key for Park Lane
stop_key = 's-gcvy4z9ws3-parklane'
next_departure_seconds = 1200  # Time frame in seconds
limit = 8  # Limit the number of records

# Construct the URL
url = f'https://transit.land/api/v2/rest/stops/s-gcvy4z9ws3-parklane/departures?next=12000&limit=4'
print(f"Requesting URL: {url}")  # Debugging output

# Infinite loop to refresh data every 30 seconds
while True:
    try:
        response = requests.get(url, headers={'apikey': API_KEY})
        ## print(f"Response Status Code: {response.status_code}")  # Debugging output

        # Check the response
        if response.status_code == 200:
            departures = response.json()  # Parse the JSON response
            now = datetime.now()  # Get the current time

            # Dictionary to store upcoming departures by route
            upcoming_buses = {'26': [], '44': [], 'N26': []}

            # Extract specific information for buses 26, 44, and N26
            for stop in departures['stops']:
                for departure in stop['departures']:
                    scheduled_time = departure['departure']['scheduled']
                    route_name = departure['trip']['route']['route_short_name']
                    trip_headsign = departure['trip']['trip_headsign']

                    # Check if the route is 26, 44, or N26 and collect up to the next two departures
                    if route_name in upcoming_buses and len(upcoming_buses[route_name]) < 2:
                        # Combine current date with scheduled time
                        try:
                            scheduled_dt = datetime.combine(now.date(), datetime.strptime(scheduled_time, "%H:%M:%S").time())
                            
                            # If the bus is scheduled for the next day, add one day
                            if scheduled_dt < now:
                                scheduled_dt += timedelta(days=1)
                            
                            time_diff = scheduled_dt - now  # Calculate the time difference
                            minutes_until = int(time_diff.total_seconds() // 60)  # Convert to minutes

                            # Append bus info to the list
                            upcoming_buses[route_name].append((trip_headsign, minutes_until))
                        except ValueError as e:
                            print(f"Error processing time: {e}")

            # Display the formatted output for each route
            for route, departures in upcoming_buses.items():
                if departures:
                    if len(departures) == 1:
                        headsign, minutes = departures[0]
                        print(f"Next bus: {route} to {headsign} in {minutes} minutes")
                    else:
                        headsign_1, minutes_1 = departures[0]
                        headsign_2, minutes_2 = departures[1]
                        print(f"Next bus: {route} to {headsign_1} in {minutes_1} minutes & {minutes_2} minutes")
                    
    except Exception as e:
        print(f"An error occurred: {e}")  # Print any exceptions that occur

    # Wait for 30 seconds before refreshing
    time.sleep(30)
