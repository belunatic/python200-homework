from weatherkit import WeatherResponse, HourlyReading, to_readings, DailyAggregator, DailySummary
from pathlib import Path
import json

#load and validate
#Open and load the raw JSON file into a Python data structure

BASE_DIR = Path(__file__).resolve().parent
json_path = BASE_DIR / "weather_raw.json"

with open(json_path, 'r') as file:
    api_response = json.load(file)

# validate the loaded json against the WeatherResponse schema
parsed = WeatherResponse.model_validate(api_response)

print(parsed.latitude, parsed.timezone)
print(len(parsed.hourly.time), type(parsed))

#test the Daily Aggregation summary
hourly_list = to_readings(parsed)

ds = DailyAggregator()
print(ds.summarize(hourly_list))
print(ds.incomplete_days(hourly_list))