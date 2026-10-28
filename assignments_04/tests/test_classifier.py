# tests/test_classifier.py
import pytest
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import json

from weather_model import WeatherClassifier, Prediction, FEATURES

'''
@oytest.fixture -> is a reusable setup function that pytest automatically  injects into your test
'''

'''
Why tests need a save model to load?
- First, test should be independent and predictable.
- if we are to used the real MODEL file for test, we might run into some issues: model "pkl" file missing or wrong path, somebody having to run training first.
- Lastly, but not least, this approach trains a small model, Save it to a TEMPORARY FOLDER 'tmp_path' and return the path to the test. ["Does my loading/prediction code work?"]
'''

''' 
Why use tmp_path?
- No leftover files from previous runs
- Tests don't interfere with each other
- Safe to run on any machine
- Easy cleanup automatically
'''

@pytest.fixture
def model_path(tmp_path):
    """Train a tiny model on obvious days and save it to a temp file."""
    good = [{"temperature_2m_max": 18, "temperature_2m_min": 9, "precipitation_sum": 0.0, "wind_speed_10m_max": 10}] * 15
    bad = [{"temperature_2m_max": 2, "temperature_2m_min": -6, "precipitation_sum": 12.0, "wind_speed_10m_max": 40}] * 15
    X = pd.DataFrame(good + bad)[FEATURES]
    y = [1] * 15 + [0] * 15

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("logreg", LogisticRegression(max_iter=1000)),
    ])
    pipe.fit(X, y)

    path = tmp_path / "weather_classifier.pkl"
    joblib.dump(pipe, path)
    return path

'''
Using the temporary saved model, create an instance of WeatherClassifier, and use it to run the tests'
'''
@pytest.fixture
def clf(model_path):
    """A WeatherClassifier loaded from the saved tiny model."""
    return WeatherClassifier(model_path)

def test_good_day_predicted_good(clf):
    result = clf.predict([
        {"temperature_2m_max": 18, "temperature_2m_min": 9, "precipitation_sum": 0.0, "wind_speed_10m_max": 10}
    ])
    assert result[0].label == "good"

'''
The above call [def test_good_day_predicted_good(clf)]?
- when pytest see the "clf" this are the steps it takes:
- - This test need something called "clf"
- - Pytest then search for a fixture named 'clf'
- - Finds it and executes it.
'''


def test_bad_day_predicted_skip(clf):
    result = clf.predict([
        {"temperature_2m_max": 3, "temperature_2m_min": -5, "precipitation_sum": 10.0, "wind_speed_10m_max": 38}
    ])
    assert result[0].label == "skip"

@pytest.mark.parametrize("data, expected, reason", 
        [
            ({"temperature_2m_max": 18, "temperature_2m_min": 9, "precipitation_sum": 0.0, "wind_speed_10m_max": 10}, "good", "it is a good weather to run"),
            ({"temperature_2m_max": 3, "temperature_2m_min": -5, "precipitation_sum": 10.0, "wind_speed_10m_max": 38}, "skip", "it is not a good weather to run"),
            ({"temperature_2m_max": 13, "temperature_2m_min": -1, "precipitation_sum": 50.0, "wind_speed_10m_max": 38}, "skip", "it is not a good weather to run"),
            ]
)
def test_random_running_day_weather(clf,data, expected, reason):
    result = clf.predict([data])
    assert result[0].label == expected , reason

@pytest.mark.parametrize("data,threshold, expected", 
        [
            ({"temperature_2m_max": 23, "temperature_2m_min": 9, "precipitation_sum": 0.0, "wind_speed_10m_max": 20},0.6, "good" ),
            ({"temperature_2m_max": 23, "temperature_2m_min": 9, "precipitation_sum": 0.0, "wind_speed_10m_max": 20},0.5, "good" ),
            ({"temperature_2m_max": 23, "temperature_2m_min": 9, "precipitation_sum": 0.0, "wind_speed_10m_max": 20},0.97, "skip" ),
            ]
)
def test_random_running_day_weather(clf,data,threshold, expected):
    result = clf.predict([data], threshold)
    assert result[0].label == expected 


def test_probability_is_between_zero_and_one(clf):
    result = clf.predict([
        {"temperature_2m_max": 15, "temperature_2m_min": 8, "precipitation_sum": 1.0, "wind_speed_10m_max": 12}
    ])
    assert 0.0 <= result[0].probability <= 1.0


def test_one_prediction_per_day_in_order(clf):
    days = [
        {"temperature_2m_max": 18, "temperature_2m_min": 9, "precipitation_sum": 0.0, "wind_speed_10m_max": 10},
        {"temperature_2m_max": 2, "temperature_2m_min": -6, "precipitation_sum": 12.0, "wind_speed_10m_max": 40},
        {"temperature_2m_max": 20, "temperature_2m_min": 0, "precipitation_sum": 24.0, "wind_speed_10m_max": 0},
    ]
    results = clf.predict(days)
    assert len(results) == 3
    assert all(isinstance(r, Prediction) for r in results)


def test_empty_list_returns_empty(clf):
    assert clf.predict([]) == []

def test_missing_feature_raises(clf):
    with pytest.raises(ValueError, match="missing required features"):
        clf.predict([{"temperature_2m_max": 18, "temperature_2m_min": 9}])   # no precipitation_sum or wind_speed_10m_max

def test_missing_model_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError, match="No model file"):
        WeatherClassifier(tmp_path / "does_not_exist.pkl")