import pandas as pd
import requests
from datetime import datetime
import time
import os

# Define the API endpoint and token
API_URL = "https://api.waqi.info/feed/here/?token=f72812a3dce2b2328992b2b06e42f4bc8e9f30da"
CSV_FILE_PATH = "air_quality_feature_store.csv"

# Function to fetch data from the API
def fetch_air_quality_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        data = response.json()
        if 'data' in data and data['data'] is not None:
            iaqi = data['data'].get('iaqi', {})
            return {
                "location_id": "delhi_mandir_marg",
                "event_timestamp": datetime.utcnow(),
                "temperature": iaqi.get('t', {}).get('v', None),
                "humidity": iaqi.get('h', {}).get('v', None),
                "pressure": iaqi.get('p', {}).get('v', None),
                "wind_speed": iaqi.get('w', {}).get('v', None),
                "wind_direction": iaqi.get('wd', {}).get('v', None),
                "pm25": iaqi.get('pm25', {}).get('v', None),
                "pm10": iaqi.get('pm10', {}).get('v', None),
                "no2": iaqi.get('no2', {}).get('v', None),
                "so2": iaqi.get('so2', {}).get('v', None),
                "o3": iaqi.get('o3', {}).get('v', None),
                "co": iaqi.get('co', {}).get('v', None)
            }
        else:
            print("No data found in API response.")
            return None
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None

# Function to append data to CSV
def append_data_to_csv(data_dict, file_path):
    # Check if the file exists to write the header only if needed
    file_exists = os.path.isfile(file_path)
    df = pd.DataFrame([data_dict])
    
    try:
        if not file_exists:
            df.to_csv(file_path, index=False, mode='w')  # Create new file with header
        else:
            df.to_csv(file_path, index=False, mode='a', header=False)  # Append without header
    except Exception as e:
        print("Error writing to CSV:", e)

# Main loop to fetch data every hour and update CSV
while True:
    new_data = fetch_air_quality_data()
    if new_data:
        append_data_to_csv(new_data, CSV_FILE_PATH)
        print("New data appended at:", new_data["event_timestamp"])
    
    # Wait for 1 hour (3600 seconds)
    time.sleep(3600)
