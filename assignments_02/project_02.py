import requests
import pandas as pd
import matplotlib.pyplot as plt

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

print(df.describe())
print('\n--------\n')
print(df.shape)
print('\n--------\n')
print(df.head())

'''
I picked The City of Gardena, California
'''

#task 2
print(df.describe())
print('\n--------\n')
print(df.isnull().sum())

'''
NOTE: 
Before fitting a model, it is worth asking which features actually relate to the target. A quick way to check is the correlation between each feature and temp_max.
'''
#correlation with temperature_2m_max
print(df.corr(numeric_only=True)["temperature_2m_max"].sort_values())

#scattered

plt.scatter(df['temperature_2m_min'], df['temperature_2m_max'] )
plt.xlabel('Min Temp')
plt.ylabel('Max Temp')
plt.title("Daily High vs Low")

#save the plot to a file
plt.savefig('./outputs/project_high_vs_low.png')

plt.show()

'''
What I see , are scattered point everywhere but they have a trend of when the min temp is high so as the max temp will be high too.
'''