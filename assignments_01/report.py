from weatherkit import WeatherResponse, HourlyReading, to_readings, DailyAggregator, DailySummary
from pathlib import Path
import json

#load and validate
#Open and load the raw JSON file into a Python data structure

def main():
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
    daily_summary_rows = ds.summarize(hourly_list)
    incomplete_data_row = ds.incomplete_days(hourly_list)

    #print daily summary

    # Print header row (with 12-character spaces for alignment)
    print(f"{'Date':<12} {'temp_max':<10} {'temp_min':<10} {'temp_range':<10}")

    for i in daily_summary_rows:
        print(f"{i.date:<12} {i.temp_max: <10.2f} {i.temp_min: <10.2f} {i.temp_range(): < 10.2f}")

    #print out incomplete days list
    if(incomplete_data_row):
        print(f"These date with no enough observation {(',').join(incomplete_data_row)}")

if __name__ =="__main__":
    main()

'''
If someone omit the guard, it means that whenever the repory.py is imported it will immediately execute the report.py (fetching data, printing and so on); This si not good if you are to import report.py in test folder/ file, it may populate your test variables and cause wrong tests.
'''