import joblib
import json
import pandas as pd
import numpy as np

# Task 7: Load and Predict
clf = joblib.load("models/weather_classifier.pkl")

# #confirm the model behaves as expected
# assert np.array_equal(model.predict(X_test), clf.predict(X_test))
# print("Loaded model matches the original.")

with open("models/weather_classifier_metadata.json") as f:
    metadata = json.load(f)
    print(metadata)
    print('City:', metadata['city'])
    print('Features:', metadata['features'])
    print('Test accuracy:', metadata['test_accuracy'])

# Build new days using the exact feature names and order from the metadata
# You create a DataFrame with 4 columns and Then you select columns using the metadata['features'] list to ensure the order is correct or else panda will throw an error.
new_days = pd.DataFrame(
    [
        {"temperature_2m_max": 18, "temperature_2m_min": 10, "precipitation_sum": 0.0, "wind_speed_10m_max": 12},
        {"temperature_2m_max": 22, "temperature_2m_min": 13, "precipitation_sum": 9.0, "wind_speed_10m_max": 14},
        {"temperature_2m_max": 25, "temperature_2m_min": 15, "precipitation_sum": 0.0, "wind_speed_10m_max": 33},
        {"temperature_2m_max": 26, "temperature_2m_min": 1, "precipitation_sum": 2.9, "wind_speed_10m_max": 29},
    ]
)[metadata["features"]]

preds = clf.predict(new_days)
probs = clf.predict_proba(new_days)[:, 1]

for i, (pred, prob) in enumerate(zip(preds, probs)):
    label = "good for running" if pred == 1 else "skip"
    print(f"Day {i + 1}: {label}  (confidence: {prob:.2f})")

#Task 8: Reflect

'''
Pick your borderline day. What probability did the model give it? Would you call the model confident or uncertain, and how would you handle a day where it predicts 0.52?
- my border day was {"temperature_2m_max": 26, "temperature_2m_min": 1, "precipitation_sum": 2.9, "wind_speed_10m_max": 29} and i got a probability of 0.01; the model was confidence on "SKIP"
- A probability of 0.52 means "a near toss-up, leaning slightly toward class 1," 
- 
'''

'''
predict.py has no training code. What would break if someone ran predict.py before train_classifier.py had ever been run? How could you make the error message more helpful?
- If someone runs predict.py before train_classifier.py, the script will fail because the trained model file and metadata file do not exist yet. The prediction code depends on loading these files, so it cannot run without them. To make the error more helpful, you can catch the FileNotFoundError and display a clear message such as: “Model not found. Please run train_classifier.py first to train and save the model.”
'''

'''
In Week 10 this model will run inside a cloud pipeline that classifies each day's weather automatically. Name one thing about your current predict.py that would need to change to support that.
- One thing will need to change is how we get the days weather instead of hard coding it.
'''