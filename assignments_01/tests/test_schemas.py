from pathlib import Path
import json
from weatherkit import WeatherResponse
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
json_path = BASE_DIR / "weather_raw.json"

with open(json_path, 'r') as file:
    api_response = json.load(file)

'''
The reason using a Path is to insure that it will work no matter where it is located, if you use a relative path, a change in the folder name or relocation of the file will fail the retrival of json element'
'''

#api_response with validation error on latitude
invalid_response = {
  "latitude": 200, #validation error
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
      "2026-04-08T00:00"
    ],
    "temperature_2m": [
      16.8
    ],
    "precipitation": [
      0.0
    ]
  }
}

#one less entry api_response
one_less_response = {
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
      "2026-04-08T00:00",
      "2026-04-08T02:00"
    ],
    "temperature_2m": [
      16.8,
      15.1,
      13.4
    ],
    "precipitation": [
      0.0,
      0.0, # one less element
    ]
  }
}

#none temp api
#one less entry api_response
none_temp_element = {
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
      None,
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



#test the schemas validation
def test_the_schemas_json_validation():
    assert WeatherResponse.model_validate(api_response)

#invalid latitude validation
def test_latitude_error():
    with pytest.raises(ValueError):
        assert WeatherResponse.model_validate(invalid_response)

#invalid entries elements
def test_one_less_element():
    with pytest.raises(ValueError, match="same"):
        assert WeatherResponse.model_validate(one_less_response)

#null inside temperature_c
def test_none_in_temperature():
    with pytest.raises(ValueError,):
        assert WeatherResponse.model_validate(none_temp_element)