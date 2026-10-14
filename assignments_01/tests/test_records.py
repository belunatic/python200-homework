from weatherkit import HourlyReading, WeatherResponse, to_readings

#api_sample to use for testing
sample_weatherResponse = {
  "latitude": 35.216976,
  "longitude": -80.83189,
  "generationtime_ms": 0.11944770812988281,
  "utc_offset_seconds": 0,
  "timezone": "GMT",
  "timezone_abbreviation": "GMT",
  "elevation": 254.0,
  "hourly_units": {
    "time": "iso8601",
    "temperature_2m": "°C",
    "precipitation": "mm"
  },
  "hourly": {
    "time": [
      "2026-04-08T00:00",
      "2026-04-08T01:00",
      "2026-04-08T02:00"
    ],
    "temperature_2m": [
      16.8,
      15.1,
      13.4
    ],
    "precipitation": [
      0.0,
      0.0,
      0.0, # one less element
    ]
  }
}

def test_first_last_element():
    api_results = WeatherResponse.model_validate(sample_weatherResponse)
    hourly_results = to_readings(api_results)
    '''
    print(hourly_results) ==
        readings = [
    HourlyReading(timestamp='2026-04-08T00:00', temperature_c=16.8, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T01:00', temperature_c=15.1, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T02:00', temperature_c=13.4, precipitation_mm=0.0)
    ]
    '''
    assert hourly_results[0].timestamp == api_results.hourly.time[0] and hourly_results[-1].timestamp == api_results.hourly.time[-1]

def test_reading_i_matches_index_i():
    api_results = WeatherResponse.model_validate(sample_weatherResponse)
    hourly_results = to_readings(api_results)
    for i in range (len(hourly_results)):
        assert hourly_results[i].timestamp == api_results.hourly.time[i] and hourly_results[i].temperature_c == api_results.hourly.temperature_2m[i] and hourly_results[i].precipitation_mm == api_results.hourly.precipitation[i]

#test if two hourly objects match
def test_the_hourly_object_match():
    api_results = WeatherResponse.model_validate(sample_weatherResponse)
    hourly_results = to_readings(api_results)
    hourly_results_2 = to_readings(api_results)
    assert hourly_results == hourly_results_2