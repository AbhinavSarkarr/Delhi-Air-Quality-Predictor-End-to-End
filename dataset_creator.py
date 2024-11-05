import pandas as pd
import aiohttp
import asyncio
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()

# Define the API endpoint and token
API_URL = "https://api.waqi.info/feed/"
API_TOKEN = os.getenv("API_TOKEN")
CSV_FILE_PATH = "air_quality_feature_store2.csv"

# List of station names for Delhi
CITIES = [
    "Delhi Institute of Tool Engineering, Wazirpur, Delhi, Delhi, India",
    "Satyawati College, Delhi, Delhi, India",
    "ITI Shahdra, Jhilmil Industrial Area, Delhi, Delhi, India",
    "Sonia Vihar Water Treatment Plant DJB, Delhi, Delhi, India",
    "Pusa, Delhi, Delhi, India",
    "R.K. Puram, Delhi, Delhi, India",
    "Major Dhyan Chand National Stadium, Delhi, Delhi, India",
    "Mandir Marg, Delhi, Delhi, India",
    "New Delhi US Embassy, India (( &?2M2@ .G0?@ &B$>5>8)",
    "Mother Dairy Plant, Parparganj, Delhi, Delhi, India",
    "Jawaharlal Nehru Stadium, Delhi, Delhi, India",
    "IHBAS, Delhi, Delhi, India",
    "Lodhi Road, Delhi, Delhi, India",
    "Burari Crossing, Delhi, Delhi, India",
    "CRRI Mathura Road, Delhi, Delhi, India",
    "Siri Fort, Delhi, Delhi, India",
    "North Campus, Delhi, Delhi, India",
    "Civil Lines, Delhi, Delhi, India",
    "ITO, Delhi, Delhi, India",
    "ITI Jahangirpuri, Delhi, Delhi, India",
    "Anand Vihar, Delhi, Delhi, India"
]

# Define a mapping of station names to actual city names
CITY_MAPPING = {
    "Delhi Institute of Tool Engineering, Wazirpur, Delhi, Delhi, India": "Wazirpur",
    "Satyawati College, Delhi, Delhi, India": "Delhi",
    "ITI Shahdra, Jhilmil Industrial Area, Delhi, Delhi, India": "Jhilmil",
    "Sonia Vihar Water Treatment Plant DJB, Delhi, Delhi, India": "Sonia Vihar",
    "PGDAV College, Sriniwaspuri, Delhi, Delhi, India": "Sriniwaspuri",
    "Pusa, Delhi, Delhi, India": "Pusa",
    "R.K. Puram, Delhi, Delhi, India": "R.K. Puram",
    "Major Dhyan Chand National Stadium, Delhi, Delhi, India": "Major Dhyan Chand National Stadium",
    "Mandir Marg, Delhi, Delhi, India": "Mandir Marg",
    "New Delhi US Embassy, India (( &?2M2@ .G0?@ &B$>5>8)": "New Delhi",
    "Mother Dairy Plant, Parparganj, Delhi, Delhi, India": "Parparganj",
    "Jawaharlal Nehru Stadium, Delhi, Delhi, India": "Jawaharlal Nehru Stadium",
    "IHBAS, Delhi, Delhi, India": "IHBAS",
    "Lodhi Road, Delhi, Delhi, India": "Lodhi Road",
    "Burari Crossing, Delhi, Delhi, India": "Burari",
    "CRRI Mathura Road, Delhi, Delhi, India": "Mathura Road",
    "Siri Fort, Delhi, Delhi, India": "Siri Fort",
    "North Campus, Delhi, Delhi, India": "North Campus",
    "Civil Lines, Delhi, Delhi, India": "Civil Lines",
    "ITO, Delhi, Delhi, India": "ITO",
    "ITI Jahangirpuri, Delhi, Delhi, India": "Jahangirpuri",
    "Anand Vihar, Delhi, Delhi, India": "Anand Vihar"
}

# Function to fetch data from the API for a given city
async def fetch_air_quality_data(session, city, timestamp):
    request_url = f"{API_URL}{city}/?token={API_TOKEN}&timestamp={int(timestamp.timestamp())}"
    try:
        async with session.get(request_url) as response:
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

            # Log the raw response text for debugging
            print(f"Response for {city} at {timestamp}: {await response.text()}")

            data = await response.json()
            
            # Check if the status is 'error' and handle it
            if data.get("status") == "error":
                print(f"API Error for {city} at {timestamp}: {data['data']}")
                return None

            if isinstance(data, dict) and 'data' in data and data['data'] is not None:
                iaqi = data['data'].get('iaqi', {})
                # Extract features
                features = {
                    "temperature": iaqi.get("t", {}).get("v", None),
                    "humidity": iaqi.get("h", {}).get("v", None),
                    "pressure": iaqi.get("p", {}).get("v", None),
                    "wind_speed": iaqi.get("w", {}).get("v", None),
                    "wind_direction": iaqi.get("wd", {}).get("v", None),
                    "pm25": iaqi.get("pm25", {}).get("v", None),
                    "pm10": iaqi.get("pm10", {}).get("v", None),
                    "no2": iaqi.get("no2", {}).get("v", None),
                    "so2": iaqi.get("so2", {}).get("v", None),
                    "o3": iaqi.get("o3", {}).get("v", None),
                    "co": iaqi.get("co", {}).get("v", None)
                }
                # Extract targ
                # et (AQI) and rename it to 'aqi'
                aqi = data['data'].get("aqi", None)

                return {
                    "location_id": city,  # Use the city name as the location ID
                    "city": CITY_MAPPING.get(city, city),  # Use the mapped area name
                    "event_timestamp": timestamp,  # Use the passed timestamp
                    **features,  # Unpack features into the return dictionary
                    "aqi": aqi  # Include aqi in the return dictionary
                }
            else:
                print(f"Unexpected data format for {city} at {timestamp}: {data}")
                return None
    except Exception as e:
        print(f"Error fetching data for {city}: {e}")
        return None

# Function to append data to CSV
def append_data_to_csv(data_dict, file_path):
    file_exists = os.path.isfile(file_path)
    df = pd.DataFrame([data_dict])
    
    try:
        if not file_exists:
            df.to_csv(file_path, index=False, mode='w')  # Create new file with header
        else:
            df.to_csv(file_path, index=False, mode='a', header=False)  # Append without header
    except Exception as e:
        print("Error writing to CSV:", e)

# Function to get the last timestamp from the CSV
def get_last_timestamp(file_path):
    if os.path.isfile(file_path):
        try:
            df = pd.read_csv(file_path)
            if not df.empty:
                last_timestamp = pd.to_datetime(df['event_timestamp']).max()
                return last_timestamp
        except Exception as e:
            print("Error reading CSV file:", e)
    return None

async def main():
    # Get the last recorded timestamp
    last_timestamp = get_last_timestamp(CSV_FILE_PATH)
    if last_timestamp:
        start_date = last_timestamp + timedelta(hours=1)  # Start from the next hour
    else:
        # Default to 9000 days ago if no data exists
        start_date = datetime.utcnow() - timedelta(days=9000)
    
    end_date = datetime.utcnow()

    # Generate timestamps for each hour in the date range
    current_date = start_date
    async with aiohttp.ClientSession() as session:
        while current_date <= end_date:
            tasks = []
            for city in CITIES:
                tasks.append(fetch_air_quality_data(session, city, current_date))

            # Await the results with a limit to control the number of concurrent requests
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    append_data_to_csv(result, CSV_FILE_PATH)
                    print(f"New data appended for {result['city']} at {result['event_timestamp']}")
            
            # Move to the next hour
            current_date += timedelta(hours=1)

# To run the async main function
if __name__ == "__main__":
    asyncio.run(main())