from dataclasses import dataclass
from pathlib import Path
import joblib
import pandas as pd


@dataclass
class Prediction:
    """The model's verdict for a single day.

    Attributes:
        label: Either "good" or "skip".
        probability: The probability, from 0 to 1, that the day is good for running( how confident the model is)
    """
    label: str
    probability: float


#the features we need 
FEATURES = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max"]

class WeatherClassifier:
    """Loads a saved weather pipeline once and predicts on many days."""

    def __init__(self, model_path: str | Path):
        model_path = Path(model_path)
        #check if train model file exist
        if not model_path.exists():
            raise FileNotFoundError(
                f"No model file at {model_path}. Train and save a model first."
            )
        self.model = joblib.load(model_path)
        self.features = FEATURES

    def predict(self, days: list[dict], threshold :float = None) -> list[Prediction]:
        """Predict whether each day is good for running.

        Args:
            days: A list of dictionaries, each with the keys temperature_2m_max, temperature_2m_min,
                precipitation_sum, and wind_speed_10m_max.

        Returns:
            One Prediction per input day, in the same order.
        """
        #if days == [] return []
        if not days:
            return []

        df = pd.DataFrame(days)
        #check to see if any features are missing as dataframe column
        missing = [f for f in self.features if f not in df.columns]
        if missing:
            raise ValueError(f"missing required features: {missing}")

        #Select the four features in a fixed order, run the model, and return a list of Prediction objects, one per day, in the same order.
        X = df[self.features]
        labels = self.model.predict(X)
        probabilities = self.model.predict_proba(X)[:, 1]

        predictions = []

        for label, prob in zip(labels, probabilities):
            if threshold is None:
                result = "good" if int(label) == 1 else "skip"
            else:
                result = (
                    "good"
                    if int(label) == 1 and prob >= threshold
                    else "skip"
                )

            predictions.append(Prediction(result, float(prob)))

        return predictions