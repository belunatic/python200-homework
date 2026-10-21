import requests
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, ConfusionMatrixDisplay, classification_report,
)
import joblib

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 33.88,
    "longitude": -118.30,
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "wind_speed_10m_max",
    ],
    "timezone": "America/New_York",
}
response = requests.get(url, params=params)
response.raise_for_status()
df = pd.DataFrame(response.json()["daily"])
df["date"] = pd.to_datetime(df["time"])
df = df.drop("time", axis=1)

print(df.shape)
print('\n')
print(df.head())

'''
I picked City of Gardena, California, 90247, USA
'''

#engineering the 'good_for_running' column
def good_for_running_func(row):
    ''' A function to determin if the value for good_for_running column

    parameter:
        row: a row of the dataframe
    '''
    if (row["temperature_2m_max"] >= 7) and (row["temperature_2m_max"] <= 26) and (row["precipitation_sum"] < 3) and (row["wind_speed_10m_max"] < 30) and (row["temperature_2m_min"] >= 0):
        return 1
    else:
        return 0

df["good_for_running"] = df.apply(good_for_running_func, axis=1)
print('\n')
print(df["good_for_running"].value_counts())

'''
what fraction of days are good, and does that seem reasonable for your city's climate?
- The fraction is 0.6, which seems reasonable with the climate of Gardena.
'''
