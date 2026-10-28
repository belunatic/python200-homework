"""Classify a few sample days using the saved weather model."""

from weather_model import WeatherClassifier

SAMPLE_DAYS = [
    {"temperature_2m_max": 18, "temperature_2m_min": 10, "precipitation_sum": 0.0, "wind_speed_10m_max": 12},
    {"temperature_2m_max": 22, "temperature_2m_min": 13, "precipitation_sum": 9.0, "wind_speed_10m_max": 14},
    {"temperature_2m_max": 25, "temperature_2m_min": 15, "precipitation_sum": 0.0, "wind_speed_10m_max": 33},
    {"temperature_2m_max": 19, "temperature_2m_min": 10, "precipitation_sum": 1.0, "wind_speed_10m_max": 29},
    {"temperature_2m_max": 23, "temperature_2m_min": 9, "precipitation_sum": 0.0, "wind_speed_10m_max": 20},
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

'''
Your predict() selects the four features in a fixed order rather than using whatever order the caller passed. Describe a concrete bug this prevents.
- Because a model produces silently wrong predictions if the features are passed in a different order than it was trained on.
- the model expects features in a specific order. Selecting them explicitly means the caller can pass keys in any order and still get correct results, and a missing feature is caught rather than silently misaligned.
'''

'''
The graded tests train their own tiny model in a fixture instead of loading models/weather_classifier.pkl. Why is that a better design for a test suite than depending on the real file?
- First, test should be independent and predictable.
- if we are to used the real MODEL file for test, we might run into some issues: model "pkl" file missing or wrong path, somebody having to run training first.
- Lastly, but not least, this approach trains a small model, Save it to a TEMPORARY FOLDER 'tmp_path' and return the path to the test. ["Does my loading/prediction code work?"]
'''

'''
In Week 10 a pipeline will import WeatherClassifier and call predict() on batches of weather records from a database. Name one thing about your component that makes it ready for that, and one thing you might add before it runs in production.
- My component is ready for it because it is using classes, so by creating an instance of WeatherClassifier we can predict as many days as possible without changing anything.
- One thing I may added to my component is checking the database connection and adding the database connection.
'''