"""Classify a few sample days using the saved weather model."""

from weather_model import WeatherClassifier

SAMPLE_DAYS = [
    {"temperature_2m_max": 18, "temperature_2m_min": 10, "precipitation_sum": 0.0, "wind_speed_10m_max": 12},
    {"temperature_2m_max": 22, "temperature_2m_min": 13, "precipitation_sum": 9.0, "wind_speed_10m_max": 14},
    {"temperature_2m_max": 25, "temperature_2m_min": 15, "precipitation_sum": 0.0, "wind_speed_10m_max": 33},
    {"temperature_2m_max": 19, "temperature_2m_min": 10, "precipitation_sum": 1.0, "wind_speed_10m_max": 29},
]


def main() -> None:
    """Load the component and print a prediction for each sample day."""
    classifier = WeatherClassifier("models/weather_classifier.pkl")
    for day, result in zip(SAMPLE_DAYS, classifier.predict(SAMPLE_DAYS)):
        print(f"{day['temperature_2m_max']:.0f}C, {day['precipitation_sum']:.0f}mm rain, "
              f"{day['wind_speed_10m_max']:.0f} km/h wind -> {result.label} ({result.probability:.2f})")


if __name__ == "__main__":
    main()

'''
Why this script exist?
- This script exists to demonstrate abd test a real user would load the save model and make predictions.
- the safe guard [ __init__ =="__main__] is to prevent the file execution when import and only execute when called directly
'''