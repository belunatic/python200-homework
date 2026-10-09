# --- Classes ---

#Q1

class Thermometer:
    def __init__(self, location, readings=None):
        '''
        location: the place the readings where taken
        readings: the daily temp readings
        '''
        self.location = location
        self.readings = readings if readings else []
        

    def add(self,reading):
        '''append a reading to the reading list'''
        self.readings.append(reading)

    def average(self):
        '''average daily reading'''
        
        if len(self.readings) > 0:
            return sum(self.readings)/ len(self.readings)

    def hottest(self):
        '''highest reading'''
        return max(self.readings)

    def __repr__(self):
        return f"Thermometer(location={self.location}, n_readings={len(self.readings)}, average={self.average()})"

london = Thermometer('London', [20,30,30,20,50])
print(london.average())
print(london.hottest())

#average method need to handle the empty case because if not Zero Division Error will be raise and cause the program to stop

#Q2

my_thermometer = Thermometer('Dubai', [30,70,90,89])
my_thermometer2 = Thermometer('Amazon', [10,70,90,45])
print(my_thermometer)
print([my_thermometer,my_thermometer2])

#If __repl__is not use the information that is display from printing object is the type and memory address, it does not give anything useful to use or understand better what object it is.

#Q3

class TemperatureAlert:
    def __init__(self, threshold=30.0):
        self.threshold = threshold

    def breaches(self,thermometer):
        '''return reading above the threshold'''
        return [reading for reading in thermometer.readings if reading > self.threshold]

t_alert_1 = TemperatureAlert(71.5)
t_alert_2 = TemperatureAlert(20.9)

my_alert_thermometer = Thermometer('California', [21.7,90,10,38,-1.1,100,71.7])

print(t_alert_1.breaches(my_alert_thermometer))
print(t_alert_2.breaches(my_alert_thermometer))

''' 
why is the threshold stored on TemperatureAlert rather than passed as an argument to breaches()? What advantage does that give you if you have twenty thermometers to check?
- The threshold is an attribute to TemperatureAlert class, it is initiated once and used everywhere within the class, allowing us to be able to compare multiple thermometer without redefining it or passing as an argument.
'''

#---- Dataclasses, Type Hints, and Docstrings

#Q1

from dataclasses import dataclass, FrozenInstanceError

@dataclass(frozen=True)
class Station:
    '''
    Station location

    station_id: the unique id
    name: the station name 
    latitude: location of the station in latitude
    longitude: location of the station in longitude
    elevation: station elevation from sea level
    '''

    station_id:int
    name:str
    latitude:float
    longitude:float
    elevation:float


station_a = Station(1,'Moon',112.3,11.9, 5000.34)
station_b = Station(1,'Moon',112.3,11.9, 5000.34)

print(station_a == station_b)
''' When using dataclass, it takes care of __init__, __eq__, and __repr__ automatically. Doing it it with original hand-written class it comparing two equal sation will result to False unless you have define __eq__ in your class'''


#Q2

try:
    station_a.latitude = 600
except FrozenInstanceError as e:
    print("Cannot modify:", e)

station_c = Station(1,'Saturn',1.3,1100.9, 0.34)

#make a set
my_set_stations = {station_a,station_b,station_c}

print(len(my_set_stations))

''' frozen=True make the class read-only; value that do not change,  A frozen dataclass also becomes hashable, so you can use it as a dictionary key or put it in a set'''

#Q3

from dataclasses import field

@dataclass
class StationBatch:
    region:str
    stations: list[Station] = field(default_factory=list)

    def add(self,station:Station) -> None:
        ''' add a station to the station batch'''
        self.stations.append(station)

    def highest(self)-> Station | None:
        ''' find the ihghest elevated station from the batch'''
        if len(self.stations)> 0:
            return max(self.stations, key=lambda e: e.elevation)


new_batch = StationBatch('Outer_World', [station_a,station_b,station_c])

print(new_batch.highest())


# '''
# Traceback (most recent call last):
#   File "C:\Abel Xul\Data Science Class\python200-homework\assignments_01\warmup_01.py", line 121, in <module>
#     @dataclass
#      ^^^^^^^^^
#   File "C:\Users\abelt\AppData\Local\Programs\Python\Python312\Lib\dataclasses.py", line 1275, in dataclass
#     return wrap(cls)
#            ^^^^^^^^^
#   File "C:\Users\abelt\AppData\Local\Programs\Python\Python312\Lib\dataclasses.py", line 1265, in wrap
#     return _process_class(cls, init, repr, eq, order, unsafe_hash,
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\abelt\AppData\Local\Programs\Python\Python312\Lib\dataclasses.py", line 994, in _process_class
#     cls_fields.append(_get_field(cls, name, type, kw_only))
#                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\abelt\AppData\Local\Programs\Python\Python312\Lib\dataclasses.py", line 852, in _get_field
#     raise ValueError(f'mutable default {type(f.default)} for field '
# ValueError: mutable default <class 'list'> for field stations is not allowed: use default_factory
# '''

''' Python refuse the stations:list[Station]=[] because; A default value is created once when the class is defined, so every instance would share the same list. Appending to one batch would append to all of them. Dataclasses detect this problem and refuse to define the class.'''

#---Pydantic

#Q1

from pydantic import BaseModel, Field, ValidationError,model_validator

class Reading(BaseModel):
    '''
    A reading from one of the station 

    station_id: the station the record is coming from
    timestamp: the exact time the reading was taken
    temperature_c: the temp at that moment that was taken
    humidity: the value of humidity

    '''

    station_id:str=Field(min_length=3)
    timestamp:str
    temperature_c:float = Field(ge= -90, le=60)
    humidity:float = Field(ge= 0, le=100)

    @model_validator(mode='after')
    def check_humid_temp(self):
        ''' Reject humid equal to 0.0' and temperature under -40'''
        if self.humidity == 0.0 and self.temperature_c < -40:
            raise ValueError(
                f'Humidity cannot be {self.humidity} and the temperature, {self.temperature_c} is below -40 '
            )
        return self



reading_1 = Reading(
    station_id = '1234',
    timestamp = '1791174083',
    temperature_c= 21,
    humidity= 99
    )

print(reading_1)

#Q2

try:
    Reading(
    station_id = '1234',
    temperature_c= 21,
    humidity= 99
    )
except ValidationError as e:
    print(e)

try:
    Reading(
    station_id = '1234',
    timestamp = '1791174083',
    temperature_c= 150.0,
    humidity= 99
    )
except ValidationError as e:
    print(e)

try:
    Reading(
    station_id = '1234',
    timestamp = '1791174083',
    temperature_c= 21,
    humidity= "very humid"
    )
except ValidationError as e:
    print(e)

reading_2 = Reading(
    station_id = '1234',
    timestamp = '1791174083',
    temperature_c= "21.5",
    humidity= 40
    )

print(reading_2,type(reading_2.temperature_c),type(reading_2.humidity))

'''
why does Pydantic accept "21.5" but reject "very humid"? State the rule in your own words.

- it does accept it because python is capable to interpret a value if it is has one meaning or outcome, therefore 21.5 has one outcome while "very humid" will have multiple outcome.

'''

# Q4

try:
    Reading(
        station_id = '34',
        temperature_c= "very hot",
        humidity= 40
    )
except ValidationError as e:
    print(f"{e.error_count()} problems found\n")
    for err in e.errors():
        print(f"  field={err['loc']}  msg={err['msg']}")

'''
how many errors were reported, and why is reporting all of them at once more useful than stopping at the first?
- 3 error reported
- It is useful because when working with a malformed API payload, you will receive a whole list at once allowing you to fix all of them at once or less interactions on fixing it.

'''

try:
    Reading(
        station_id= '12345',
        timestamp='123456787',
        temperature_c = -54,
        humidity =0.0
    )
except ValidationError as e:
    print(e)

''' 
explaining why this rule cannot be expressed with Field constraints alone.
- you can only set one constrain per attribute, so if additonal constrain are needed then model_validation is useful for that
'''

#----- pytest ----

import pytest

#Q1

def celsius_to_fahrenheit(celsius: float) -> float:
    ''' convert celsius temperature to fahrenheit'''
    return celsius * 9 / 5 + 32

def test_celsius_to_fahrenheit():
    '''testing the conversions'''
    assert celsius_to_fahrenheit(0) == 32
    assert celsius_to_fahrenheit(100) == 212
    assert celsius_to_fahrenheit(37) == pytest.approx(98.6)

'''pytest.approx is necessary a regular result of float is result to a fraction with aloot of decimal places which will lead to the test failing. Therefore pytest.approx compare float within the relative tolerance'''

#Q2

def mean(values: list[float]) -> float:
    ''' Check to for an empty string
    
    Raises:
            ValueError: if values list is empty
    '''
    if len(values) == 0:
        raise ValueError(
            f"cannot average an empty list"
        )
    else:
        return sum(values)/ len(values)

def test_mean_of_empty_raises():
    ''' check for empty list of values  '''
    with pytest.raises(ValueError, match='empty'):
        mean([])

''' 
what would pytest.raises(ValueError) alone fail to catch that match= catches?
- because the "match" variable is used as a search string in assert the exception's error message  matches a specific regular expression
'''

#Q3

@pytest.mark.parametrize(
    "values, expected, reason",
    [ 
        ([1,2,3], 2 , "positive number"),
        ([-1,-2,-3], -2 , "negative number"),
        ([4], 4 , "single element"),
        ([1,2,3,10], 4 , "positive number")
     ]
)
def test_mean_values(values,expected, reason):
    assert mean(values) == expected , reason

'''
why is one parametrized test with four cases better than four nearly identical test functions?
- Organization and legibility and also if one test fail it does not stop it will assert all tests
'''

#Q4

# """
# platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0 -- C:\Abel Xul\Data Science Class\python200-homework\.venv\Scripts\python.exe
# cachedir: .pytest_cache
# rootdir: C:\Abel Xul\Data Science Class\python200-homework\assignments_01
# collected 6 items                                                                                                                                                                                                                     

# warmup_01.py::test_celsius_to_fahrenheit FAILED                                                                                                                                                                                 [ 16%]
# warmup_01.py::test_mean_of_empty_raises PASSED                                                                                                                                                                                  [ 33%]
# warmup_01.py::test_mean_values[values0-2-positive number] PASSED                                                                                                                                                                [ 50%]
# warmup_01.py::test_mean_values[values1--2-negative number] PASSED                                                                                                                                                               [ 66%]
# warmup_01.py::test_mean_values[values2-4-single element] PASSED                                                                                                                                                                 [ 83%]
# warmup_01.py::test_mean_values[values3-4-positive number] PASSED                                                                                                                                                                [100%]

# ============================================================================================================== FAILURES ==============================================================================================================
# _____________________________________________________________________________________________________ test_celsius_to_fahrenheit _____________________________________________________________________________________________________

#     def test_celsius_to_fahrenheit():
#         '''testing the conversions'''
#         assert celsius_to_fahrenheit(0) == 32
# >       assert celsius_to_fahrenheit(100) == 212
# E       assert 257.0 == 212
# E        +  where 257.0 = celsius_to_fahrenheit(100)

# warmup_01.py:299: AssertionError
# ====================================================================================================== short test summary info =======================================================================================================
# FAILED warmup_01.py::test_celsius_to_fahrenheit - assert 257.0 == 212
# """

'''
 what specific values did pytest show you in the failure report, and why is that more useful than a bare "assertion failed"?
 - it showed me that "assert celsius_to_fahrenheit(100) == 212" has failed, this is great because it shows exactly what failed and where to go correct it.
'''