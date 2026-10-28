# Q1

import json
from pathlib import Path
from dataclasses import dataclass
import pytest

class ModeInfo:
    def __init__(self, path:Path | str):
        # Open the JSON file in read mode
        with open(path, 'r') as file:
            # Parse the file content into a Python object
            self.data = json.load(file)

    def feature_count(self) -> int:
        print(len(self.data["features"]))

json_info = ModeInfo('features.json')
json_info.feature_count()
print('\n')

'''
why is loading the file in __init__ better than loading it inside feature_count() if the method is called many times?
- because using __init__ to load the json means that the file will be loaded once when the object is created. In short "Load Once, Use Many Times". This process many be slower in the building stages but it only does this once, compare to the reading the json feature_count method, will make the program slower
'''

# Q2
@dataclass
class DayForecast:
    '''
        Display the day high and if it is going to rain
    '''
    date:str
    high_c: float
    will_rain:bool

    def summary(self) -> str:
        '''
            print out the daily weather
        '''
        rain_bool = "rain expected" if self.will_rain else "no rain"
        return f"{self.date}: high {self.high_c}C, {rain_bool}"

day1 = DayForecast('2023-06-15' , 24.1, True)
day2 = DayForecast('2023-07-15' , 29.1, False)

print(day1.summary())
print(day2.summary())

'''
name one thing the @dataclass decorator wrote for you that you did not have to write by hand.
- dataclass wrote for me the __init__ method; and other but this is the main one.
'''

# Q3

def parse_temperature(text: str) -> float:
    try:
        return float(text)
    except ValueError:
        raise ValueError(
            f"The temperature value of {text} is not a number"
        )

def test_parse_temperature_valid():
    assert parse_temperature("24.1") == pytest.approx(24.1)

def test_parse_temperature_bad_input_raises():
     with pytest.raises(ValueError, match="is not a number"):
         parse_temperature('hot')

'''
what would pytest.raises(ValueError) without match fail to catch?
- The match attribute is used as a regex to match the exact message of the raised exception; in other word it attach the test to the function or method call.
'''