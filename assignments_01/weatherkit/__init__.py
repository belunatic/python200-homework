"""weatherkit: tools for working with daily weather observations."""

from weatherkit.schemas import WeatherResponse
from weatherkit.records import HourlyReading, to_readings
from weatherkit.summarize import DailyAggregator, DailySummary

__all__ = ['WeatherResponse', 'HourlyReading', 'to_reading', 'DailySummary', 'DailyAggregator']