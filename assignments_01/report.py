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
    print(f"{'Date':<12} {'temp_max':<10} {'temp_min':<10} {'precipitation_sum':<20} {'temp_range':<10}")

    for i in daily_summary_rows:
        print(f"{i.date:<12} {i.temp_max: <10.2f} {i.temp_min: <10.2f} {i.precipitation_sum: <20.2f} {i.temp_range(): < 10.2f}")

    #print out incomplete days list
    if(incomplete_data_row):
        print(f"These date with no enough observation {(',').join(incomplete_data_row)}")

if __name__ =="__main__":
    main()

'''
If someone omit the guard, it means that whenever the repory.py is imported it will immediately execute the report.py (fetching data, printing and so on); This si not good if you are to import report.py in test folder/ file, it may populate your test variables and cause wrong tests.
'''

'''
Your WeatherResponse rejects the whole file if a single temperature is null. Is that the right behavior for a weather pipeline? Describe one situation where you would want it, and one where you would rather tolerate the gap. What would you change in the schema to tolerate it?
- In the world of accuracy a null data may lead to inaccuracy, so it is important to have actual data and no missing data. A situation I think it will be okey to allow a single temperature null data is when the data is very close from one to another or consistency, it will make it easy to calculate or fill the gap. In the schema , I would just temperature_2m to be float | None.
DailyAggregator.min_hours defaults to 24. What goes wrong if a pipeline runs at noon and the day is only half over? How does incomplete_days() help?
- If the pipeline runs at noon then that date will be added to the incomplete_days return list. The function incomplete_days return a list of date that we can use as information to proper locate or learn the problem by giving us a dates to identify the errors or issue. 
You wrote weatherkit as a package rather than one file. Name one concrete thing that becomes easier in Week 10, when a pipeline needs to import this code.
- Cohesion, the degree to which the methods, properties, and responsibilities inside a class belong together and serve a single, well-defined purpose.

'''