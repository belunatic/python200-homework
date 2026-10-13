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