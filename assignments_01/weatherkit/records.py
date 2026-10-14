from dataclasses import dataclass   
from weatherkit import WeatherResponse

@dataclass
class HourlyReading:
    ''' hourly reading for a fix location
    
    Attribute:
        timestamp: observation date and time as an ISO string
        temperature_c: Daily temperature in degree Celsius
        precipitation_mm: Total precipitation in millimeters.
    '''

    timestamp:str
    temperature_c: float
    precipitation_mm: float


def to_readings(response: WeatherResponse) -> list[HourlyReading]:
        '''
        Reading the WeatherResponse and returning the hourly value as a list

        Args:
            response: Daily weather observation 

        Returns:
            One HourlyReading per hour, in the order returned by the API.
        '''
        hourly = response.hourly
        return [
            HourlyReading(
            timestamp=hourly.time[i],
            temperature_c=hourly.temperature_2m[i],
            precipitation_mm=hourly.precipitation[i],
        )
        for i in range(len(hourly.time))
        ]

''' why is HourlyReading a dataclass rather than a Pydantic model, when WeatherResponse is a Pydantic model? Be specific. A good answer identifies where the boundary is.

    - HourlyReading is a dataclass because the data stored does not require the validation, parsing, and serialization features provided by Pydantic models. WeatherResponse, on the other hand, represents the raw API response and benefits from Pydantic's validation to ensure the data conforms to the expected schema.
-
'''

