# --- scikit-learn API ---

#Q1
import numpy as np
from sklearn.linear_model import LinearRegression

temp_min = np.array([1, 4, 8, 12, 16, 20]).reshape(-1, 1)
temp_max = np.array([8, 10, 15, 18, 23, 27])

model = LinearRegression()  # Create
model.fit(temp_min, temp_max) # learn the relationship between min temp and max temp

#Predict highs for 6 and 18 temp
pred_6 = model.predict([[6]])
pred_18 = model.predict([[18]])

print(' 6 degree predict: ', pred_6)
print(' 18 degree predict: ', pred_18)

print('Slope: ', model.coef_[0])
print('Intercept: ', model.intercept_)

#Q2
print('\t')
x = np.array([10, 20, 30, 40, 50])
print(x)
x = np.array([10, 20, 30, 40, 50]).reshape(-1,1) 
print(x)
#scikit-learn only take 2d arrays, if you try to use a 1D array you will get an error; the @d shape represent (num_samples, num_features).

# --- Linear Regression ---

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

rng = np.random.default_rng(42)
num_days  = 120
temp_min  = rng.uniform(-5, 22, num_days)
is_rainy  = rng.integers(0, 2, num_days).astype(float)
temp_max  = 1.0 * temp_min + 6 - 4 * is_rainy + rng.normal(0, 2, num_days)

#Q1
#create a scattered plot
plt.scatter(temp_min, temp_max, c=is_rainy, cmap='coolwarm')
plt.xlabel('Min Temp')
plt.ylabel('Max Temp')
plt.title("Daily High vs Low")

#save the plot to a file
plt.savefig('./outputs/high_vs_low.png')

plt.show()

'''
Add a comment describing what you see. Are there two visible groups? What does that suggest about the is_rainy variable?
- I see a continuous value that grow as the min temp increase and how the plot is scattered; Yes there are two visible groups, the rain and no-rain. the plot suggests that it rain equal amount as it hasn't rained.

'''

#Q2
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
#reshape the temp_min
X = temp_min.reshape(-1,1)

#train and test the model
X_train, X_test, y_train, y_test = train_test_split(X,temp_max, test_size=0.2, random_state=42)

print('\t X_train: ', X_train)
print('\t X_test: ', X_test)
print('\t y_train: ', y_train)
print('\t y_test: ', y_test)

#Q3
model = LinearRegression()
model.fit(X_train,y_train)

print('\tSlope: ', model.coef_[0])
print('\tIntercept: ', model.intercept_)

y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test,y_pred))
r2 = model.score(X_test, y_test)

print('\t rmse: ', rmse)
print('\t r2: ', r2)

'''
Add a comment interpreting the slope in plain English. What does it mean for the daily high?
- The slope tells you how much the predicted value changes when the input changes by 1 unit 
- for daily high, it means max temperature increases by 0.94 for 1 degree increase in min temperature
'''

#Q4
X_full = np.column_stack([temp_min, is_rainy])

model_full = LinearRegression()
model_full.fit(X_full, temp_max)

print("temp_min coefficient:", model_full.coef_[0])
print("is_rainy coefficient:", model_full.coef_[1])

X_multi_train, X_multi_test, y_multi_train, y_multi_test = train_test_split(X_full, temp_max, test_size= 0.2, random_state=42)

model_multi_train = LinearRegression()
model_multi_train.fit(X_multi_train, y_multi_train)
y_multi_pred = model_multi_train.predict(X_multi_test)

r2_multi = model_multi_train.score(X_multi_test,y_multi_test)
print('r2_multi: ', r2_multi)

'''
Add a comment interpreting the is_rainy coefficient. What does it represent in practical terms?
- is_rainy coefficient shows that when it rains the max temperature is 3 degree lower, so it rain contribute to the max temperature.
- In practical term if min temperature is held at a given temperature, the rain is still show to be effective in lowering the max temperature
'''

#Q5
plt.scatter(y_multi_pred, y_multi_test,)

# Diagonal reference line
min_val = min(y_multi_test.min(), y_multi_pred.min())
max_val = max(y_multi_test.max(), y_multi_pred.max())
plt.plot([min_val, max_val], [min_val, max_val], 'k--', linewidth=2)

plt.title("Predicted vs Actual")
plt.xlabel('Prediction')
plt.ylabel('Actual')

#save the plot to a file
plt.savefig('./outputs/predicted_vs_actual_warmup.png')

plt.show()

'''
what does it mean when a point falls above the diagonal? What about below?
- when the point is above the line it means that the model prediction was lower than the real value
- when the point is below the line it means that the model prediction was higher than the real value
'''