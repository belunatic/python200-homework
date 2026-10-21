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

#Task 2: Engineer the Label
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


# Task 3: Build and Evaluate a KNN Classifier
numerics_feature = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max"]
X = df[numerics_feature]
y = df["good_for_running"]

#train and test split
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=42, stratify=y)

# Choosing the k for KNN using cross-validation
for k in [1,3,5,7,10,11,15,20,24, 30]:
    knn = Pipeline([
        ("scaler", StandardScaler()),
        ("knn", KNeighborsClassifier(n_neighbors=k)),
    ])
    scores = cross_val_score(knn, X_train, y_train, cv=5)
    print(f"k={k:2d}:  mean={scores.mean():.3f}  std={scores.std():.3f}")

'''
Why choose k = 3?
- I chose k =3 because the cross-val mean is second highest (the the other one is a k =1, with high std, meaning not stable) and the cross-val std is lowest, making it strong and stable to use on the model.
'''

#KNN Pipeline

best_k =3
knn_model = Pipeline([
        ("scaler", StandardScaler()),
        ("knn", KNeighborsClassifier(n_neighbors=k)),
    ])

knn_model.fit(X_train,y_train)
y_pred = knn_model.predict(X_test)

#test accuracy
print("\nFinal test accuracy:", accuracy_score(y_test, y_pred))

#Classification report
print('\n Classification Report')
print(classification_report(y_test, y_pred, target_names=["skip", "good"]))

# Task 4: Build and Evaluate a Logistic Regression Classifier

logreg_model = Pipeline([
    ("scaler", StandardScaler()),
    ("logreg", LogisticRegression(max_iter=1000)),
])

logreg_model.fit(X_train, y_train)

y_pred = logreg_model.predict(X_test)

#test accuracy
print("\nFinal test accuracy:", accuracy_score(y_test, y_pred))

#Classification report
print('\n Classification Report')
print(classification_report(y_test, y_pred, target_names=["skip", "good"]))

#Coefficient of each feature
print('\n')
logreg = logreg_model.named_steps["logreg"]
for name, coef in zip(numerics_feature, logreg.coef_[0]):
    print(f"{name:20s}: {coef:+.2f}")

'''
which conditions most strongly push a day toward "skip"?
Precipitation seem like the most define factor when it come to skipping a run for the day with highest negative value. To also point out Max temperature and Wind speed are negative with second factor in determined if a day is good for a run. 
'''