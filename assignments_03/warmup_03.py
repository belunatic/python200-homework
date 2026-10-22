import numpy as np
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

df = pd.read_csv("weather_classification.csv")
numeric = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max"]
X = df[numeric]
y = df["good_for_running"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- Preprocessing ---

# Q1
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(X_scaled.mean(axis=0))  # Should be close to 0

'''
Add a comment explaining, in one sentence, why you fit the scaler on X_train only.
- We fit the scaler on X_train only to prevent data leakage and ensure that the model is evaluated on unseen data during testing.
'''

# Q2
encoder = OneHotEncoder(sparse_output=False)

season = df[["season"]]
encoded = encoder.fit_transform(season)

print('\n')
print(encoded.shape)
print(encoder.get_feature_names_out())
# print(encoded)

'''
how many columns did the single season column become, and why is that number what it is?
- The single season column became 4 columns because there are 4 unique categories (seasons) in the data, and one-hot encoding creates a separate binary column for each category.
'''

# Q3

features = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max", "season"]

X = df[features]
X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

preprocess = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric),
        ("cat", OneHotEncoder(handle_unknown='ignore'), ["season"]),
    ]
)

model = Pipeline(
    steps=[
        ("preprocess", preprocess),
        ("classifier", LogisticRegression(max_iter=1000))
    ]
)

model.fit(X_train_2, y_train_2) #fit the scaler, the encoder AND the classifier
y_pred_2 = model.predict(X_test_2)

print('\n')
print("Accuracy: ", accuracy_score(y_test_2, y_pred_2))

'''
what does the pipeline do automatically that you would otherwise have to do by hand?
- The pipeline automatically applies the preprocessing steps (scaling and encoding) to the training data before fitting the classifier, and it also applies the same preprocessing to the test data before making predictions, ensuring consistency and reducing the risk of errors.'''

## ---KNN ---

# Q1

knn_scaled = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(n_neighbors=5)),
])

knn_scaled.fit(X_train, y_train)
y_pred = knn_scaled.predict(X_test)

print('\n')
print("Scaled accuracy:  ", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=["skip", "good"]))

# Q2
print('\n')

for k in [1, 3, 5, 7, 9, 11, 15, 19, 25]:
    knn = Pipeline([
        ("scaler", StandardScaler()),
        ("knn", KNeighborsClassifier(n_neighbors=k)),
    ])
    scores = cross_val_score(knn, X_train, y_train, cv=5)
    print(f"k={k:2d}:  mean={scores.mean():.3f}  std={scores.std():.3f}")

'''
Add a comment naming the k you would choose and why
- I would pick k=11 because it has a highest cross-validation mean and a low standard deviation, making it  strong and stable choice for the model's performance.
'''

#Q3
print('\n')
#Unscaled KNN
knn_unscaled = KNeighborsClassifier(n_neighbors=5)
knn_unscaled.fit(X_train, y_train)
print("Unscaled accuracy:", accuracy_score(y_test, knn_unscaled.predict(X_test)))

#scaled KNN
knn_scaled = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(n_neighbors=5)),
])
knn_scaled.fit(X_train, y_train)
print("Scaled accuracy:  ", accuracy_score(y_test, knn_scaled.predict(X_test)))

'''
did scaling help, and why would scaling matter for a distance-based model?
- Yes, scaling did help, the  improvement comes almost entirely from letting precipitation and the other smaller-range features count fairly in the distance; since KNN is a distance-based model, scaling is not optional.
'''

#Logistic Regression
#Q1
model = Pipeline([
    ("scaler", StandardScaler()),
    ("logreg", LogisticRegression(max_iter=1000)),
])
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

report = classification_report(y_test, y_pred, target_names=["skip", "good"], output_dict=True) #output to a dictionary so we can access the metrics easily

print('\n')
print('Accuracy Score:',accuracy_score(y_test, y_pred))
print("Metrics for GOOD:")
print(report['good']) #print the metrics for the "good" class

#Q2
print('\n')

logreg = model.named_steps["logreg"]
for name, coef in zip(features, logreg.coef_[0]):
    print(f"{name:20s}: {coef:+.2f}")

'''
which features push most strongly toward "skip," and does that match your intuition about running weather?
-Precipitation and wind speed have large negative coefficients, which means more rain and more wind both push a day strongly toward "skip." SInce the data was  tested on the 120 days the temperatures have small coeffiecients because the temperature range were not extreme. In short the coffecients match my intuition about running weather.
- Positive coefficients increase the chance of “good”; negative coefficients increase the chance of “skip.”
'''

# Q3
print('\n')
probabilities = model.predict_proba(X_test)[:, 1]   # probability of "good"
print(probabilities[:5].round(2))

'''
what does a probability near 0.5 tell you about the model's confidence for that day?
- The model is not sure whether to skip or run on that day.
'''

# --- Evaluation
print('\n')
# from logistic regression model

cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
print(cm)

#display the confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["skip", "good"])
disp.plot(colorbar=False)
plt.title("Rapid Test Confusion Matrix")
plt.savefig('outputs/logreg_confusion_matrix.png')
plt.show()

'''
            Predicted
           0      1
Actual 0  TN     FP
Actual 1  FN     TP
'''

'''
how many false positives and how many false negatives did the model make, and which kind of error would matter more for a running app?
- FP = 9 and FN = 7, A False Negative will matter more for a running app because the user will lose confidence in the app if it skips good days for running.
- A False Positive (predicting “good” on a bad day) is annoying, but a False Negative feels like a lost opportunity, which users dislike more.
'''

# --Joblib ---
#Q1

#saving the model
joblib.dump(model, "models/warmup_model.pkl")
print("\nModel saved.")

#load and test the saved model
loaded = joblib.load("models/warmup_model.pkl")
assert (loaded.predict(X_test) == model.predict(X_test)).all()
print("Predictions match.")

'''
what would go wrong if you had saved only the LogisticRegression step without the scaler, then called .predict() on raw data?
- If you save only the LogisticRegression step without the scaler, then call .predict() on raw data, the model will produce incorrect predictions. LogisticRegression was trained on scaled features, so its learned coefficients assume normalized inputs. Feeding raw values causes the model’s internal math to break: coefficients no longer match the feature magnitudes, the sigmoid saturates, and the model ends up predicting the wrong class with high confidence. This is why you must save the entire pipeline, not just the classifier.
'''