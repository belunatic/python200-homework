import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

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

# print(df.describe())
# print('\n--------\n')
# print(df.shape)
# print('\n--------\n')
# print(df.head())

# '''
# I picked The City of Gardena, California
# '''

# #task 2
# print(df.describe())
# print('\n--------\n')
# print(df.isnull().sum())

# '''
# NOTE: 
# Before fitting a model, it is worth asking which features actually relate to the target. A quick way to check is the correlation between each feature and temp_max.
# '''
# #correlation with temperature_2m_max
# print(df.corr(numeric_only=True)["temperature_2m_max"].sort_values())

# #scattered

# plt.scatter(df['temperature_2m_min'], df['temperature_2m_max'] )
# plt.xlabel('Min Temp')
# plt.ylabel('Max Temp')
# plt.title("Daily High vs Low")

# #save the plot to a file
# plt.savefig('./outputs/project_high_vs_low.png')

# plt.show()

# '''
# What I see , are scattered point everywhere but they have a trend of when the min temp is high so as the max temp will be high too.
# '''

#Task 3
def is_summer_month(row):
    '''
    determine if the month is in summer

    df: the current data frame

    return:
        the value 1 or 0 to determine is_summer
    '''
    get_month = row['date'].month
    if get_month > 5 and get_month < 9:
        return 1
    else:
        return 0

#create the is_summer column
df['is_summer'] = df.apply(is_summer_month, axis=1)

print('\n--------\n')
print(f"Summer days: {(df["is_summer"] == 1).sum()}")
print(f"Non-Summer days: {(df["is_summer"] == 0).sum()}")

'''
do you expect is_summer to help predict the daily high, and why?
- Yes I do expect is_summer to help with the prediction because summer plays an important role in high temperature, it usually hotter in summer then other season, so I am expecting hight temperatures
'''

#Task 4

#2D min temp
X_min_temp = df[['temperature_2m_min']]

model = LinearRegression()
model.fit(X_min_temp, df['temperature_2m_max'])
y_pred = model.predict(X_min_temp)

print('Slope: ', model.coef_[0])
print('Intercept: ', model.intercept_)

#train and test the model
X_train, X_test, y_train, y_test = train_test_split(X_min_temp, df['temperature_2m_max'], test_size=0.2, random_state=42)

model_train = LinearRegression()
model_train.fit(X_train, y_train)
y_pred_test = model_train.predict(X_test)

#rmse
rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))

#R2
r2 = model_train.score(X_test, y_test)

print('\n--------\n')
print('Slope: ', model_train.coef_[0])
print('\n--------\n')
print('Intercept: ', model_train.intercept_)
print('\n--------\n')
print('RMSE: ', rmse)
print('\n--------\n')
print('R2: ', r2)

'''
RMSE is 4.18, which means that the model_train prediction are off by 4.18 degrees on average.
'''

#Task 5
feature_cols = ["temperature_2m_min", "precipitation_sum",
                "wind_speed_10m_max", "is_summer"]
X = df[feature_cols].values
y = df["temperature_2m_max"].values

#train and test the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#model
model_multi = LinearRegression()
model_multi.fit(X_train, y_train)

#r2
train_score = model_multi.score(X_train, y_train)
test_score = model_multi.score(X_test, y_test)
print('\n--------\n')
print('Train R2: ', train_score)
print('\n--------\n')
print('Test R2: ', test_score)

#rmse on the test set
y_pred_test = model_multi.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
print('\n--------\n')
print('Test RMSE: ', rmse)

'''
By adding more feature the RMSE is now 3.82, which means that the model_multi prediction are off by 3.82 degrees on average.
'''

for name, coef in zip(feature_cols, model_multi.coef_):
    print(f"{name:22s}: {coef:+.3f}") 

'''
Which features raise the predicted high, and which lower it? Are any signs surprising? Then compare train R² to test R². Are they close, or is there a gap, and what does that tell you?

- is_summer and min temperature raise the prediction high, while precipitation and wind speed lower it. Nothing surprising here.

- the train r2 score is 0.54 and test r2 is 0.46, they are close. On train data the variation is moderate and the model learned some real pattern. Test data is a bit lower, telling us that the model perform slightly wrose on new data/unseen data.
'''