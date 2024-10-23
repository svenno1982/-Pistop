import requests
from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict

# Fetch the GTFS-RT feed
feed_url = 'YOUR_GTFS_RT_FEED_URL'  # Replace with your GTFS-RT feed URL
response = requests.get(feed_url)

# Parse the GTFS-RT feed
feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)

# Extract and display vehicle positions and trip updates
for entity in feed.entity:
    if entity.HasField('vehicle'):
        vehicle = entity.vehicle
        if vehicle.trip.route_id in ['26', '44']:  # Filter for routes 26 and 44
            print(f"Bus {vehicle.vehicle.id} on route {vehicle.trip.route_id}")
            print(f"Location: {vehicle.position.latitude}, {vehicle.position.longitude}")

    if entity.HasField('trip_update'):
        trip_update = entity.trip_update
        for stop_time_update in trip_update.stop_time_update:
            stop_id = stop_time_update.stop_id
            arrival_time = stop_time_update.arrival.time
            print(f"Bus arriving at stop {stop_id} at {arrival_time}")