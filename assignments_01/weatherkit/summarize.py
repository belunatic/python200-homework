from dataclasses import dataclass
from weatherkit import WeatherResponse
from weatherkit import HourlyReading
from datetime import datetime

@dataclass
class DailySummary:
    '''
    Daily summary of weather observations.

    Attributes:
        date: Observation date as an ISO string.
        temp_max: Maximum temperature in degree Celsius.
        temp_min: Minimum temperature in degree Celsius.
        precipitation_sum: Total precipitation in millimeters.
        hours_observed: Number of hours observed.
    '''
    date: str
    temp_max: float
    temp_min: float
    precipitation_sum: float
    hours_observed: int

    def temp_range(self) -> float:
        return self.temp_max - self.temp_min


class DailyAggregator :
    ''' groups hourly readings into daily summaries'''
    def __init__(self, min_hours:int = 24):
        self.min_hours = min_hours

    def summarize(self,readings: list[HourlyReading]) -> list[DailySummary]:
        ''' Group readings by calendar date and return the summaries sorted by date
        
            Args:
                readings: List of hourly weather readings to be summarized.

            Returns:
                List of daily weather summaries sorted by date.
        '''
        #DailySummary list
        dailySummary =[]
       
        #daily aggregation dictionary
        daily={}

        #get readings and group them by dates
        for reading in readings:
            date= reading.timestamp[:10]
            daily.setdefault(date,[]).append(reading)

        print('this is daily:')
        print(daily)

        #loop thought the dates
        for date, observations in daily.items():
            #get temp_max and temp_min
            temps = [ reading.temperature_c for reading in observations]
            temp_max = max(temps)
            temp_min = min(temps)

            #precipitation sum
            precipitation_sum = sum(reading.precipitation_mm for reading in observations)

            #Create a DailySummary, only if observation is >= 24
            if len(observations)>=self.min_hours :
                dailySummary.append(
            DailySummary(
                date=date,
                temp_max=temp_max,
                temp_min=temp_min,
                precipitation_sum=precipitation_sum,
                hours_observed=len(observations)
            )
        )

        return dailySummary

