# --- Classes ---

#Q1

class Thermometer:
    def __init__(self, location, readings=[]):
        '''
        location: the place the readings where taken
        readings: the daily temp readings
        '''
        self.location = location
        self.readings = readings

    def add(self,reading):
        '''append a reading to the reading list'''
        self.reading.append(reading)

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
        self.station.append(station)

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