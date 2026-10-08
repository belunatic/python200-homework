from weatherkit import DailySummary, DailyAggregator, HourlyReading
import pytest

@pytest.fixture
def two_day_observation() -> list[HourlyReading]:
    return [
    # --- Day 1: 2026-04-08 ---
    HourlyReading(timestamp='2026-04-08T00:00', temperature_c=16.8, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T01:00', temperature_c=15.1, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T02:00', temperature_c=13.4, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T03:00', temperature_c=12.1, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T04:00', temperature_c=12.0, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T05:00', temperature_c=11.3, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T06:00', temperature_c=10.2, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T07:00', temperature_c=9.5, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T08:00', temperature_c=9.3, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T09:00', temperature_c=9.0, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T10:00', temperature_c=7.9, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T11:00', temperature_c=7.8, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T12:00', temperature_c=8.1, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T13:00', temperature_c=8.8, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T14:00', temperature_c=10.1, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T15:00', temperature_c=11.5, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T16:00', temperature_c=12.9, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T17:00', temperature_c=14.1, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T18:00', temperature_c=14.8, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T19:00', temperature_c=15.7, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T20:00', temperature_c=16.1, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T21:00', temperature_c=16.4, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T22:00', temperature_c=16.3, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-08T23:00', temperature_c=15.9, precipitation_mm=0.0),

    # --- Day 2: 2026-04-09 ---
    HourlyReading(timestamp='2026-04-09T00:00', temperature_c=13.6, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T01:00', temperature_c=11.7, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T02:00', temperature_c=10.5, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T03:00', temperature_c=9.4, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T04:00', temperature_c=8.7, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T05:00', temperature_c=8.2, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T06:00', temperature_c=7.6, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T07:00', temperature_c=6.6, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T08:00', temperature_c=5.8, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T09:00', temperature_c=5.0, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T10:00', temperature_c=4.2, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T11:00', temperature_c=3.7, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T12:00', temperature_c=4.8, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T13:00', temperature_c=6.5, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T14:00', temperature_c=9.0, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T15:00', temperature_c=11.3, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T16:00', temperature_c=13.5, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T17:00', temperature_c=15.4, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T18:00', temperature_c=17.1, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T19:00', temperature_c=18.4, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T20:00', temperature_c=19.1, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T21:00', temperature_c=19.3, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T22:00', temperature_c=18.9, precipitation_mm=0.0),
    HourlyReading(timestamp='2026-04-09T23:00', temperature_c=18.3, precipitation_mm=0.0)
    ]

#grouping of dates
def test_group_dates(two_day_observation):
    daily_agg = DailyAggregator()
    results = daily_agg.summarize(two_day_observation)
    assert len(results) == 2

def test_temp_high_temp_low(two_day_observation):
    daily_agg = DailyAggregator()
    results = daily_agg.summarize(two_day_observation)
    assert results[0].temp_max == 16.8 and results[0].temp_min == 7.8 and results[1].temp_max == 19.3 and results[1].temp_min == 3.7

def test_precipitation_sum(two_day_observation):
    daily_agg = DailyAggregator()
    results = daily_agg.summarize(two_day_observation)
    assert results[0].precipitation_sum == 0 == 0 and results[1].precipitation_sum == 0

def test_incomplete_days(two_day_observation):
    daily_agg = DailyAggregator()
    results = daily_agg.incomplete_days(two_day_observation)
    assert results == []

def test_min_hours_lowered(two_day_observation):
    daily_agg = DailyAggregator(2)
    results = daily_agg.incomplete_days(two_day_observation)
    assert len(results) == 0

#test different aggregation min hours for summarization
@pytest.mark.parametrize( 
    'daily_agg, expected, reason',
    [ 
        (2, True, 'low aggregation'),
        (100, False, 'high aggregation'),
        (0, True, 'zero'),
        (-1, True, 'negative'),
     ]
)
def test_different_daily_aggregation(daily_agg, expected, reason,two_day_observation):
    daily_summary = DailyAggregator(daily_agg)
    results = daily_summary.summarize(two_day_observation)
    assert (len(results) > 0) == expected,reason