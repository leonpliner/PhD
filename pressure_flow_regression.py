#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fluigent Pressure - Flow experiment data processing.  
The aim of this experiment was to determine the pressure-flow relationship.
This will be done by fitting a polynomial regression model to the obtained 
dataset.

Since there was an issue with the liquid refill which has contaminated the 
original dataset with non-representative flow measurements, a threshold will be
applied at the value P=224 mbar.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

threshold=11200

dataset = pd.read_csv('pressure_flow_23_Mar_2021.csv')

P= dataset.P[:threshold]
Q= dataset.Q[:threshold]

P=P[:,np.newaxis]
Q=Q[:,np.newaxis]

#%%
plt.figure()
plt.scatter(Q,P,s=0.1)
plt.xlabel('Measured flow Q, ul/min')
plt.ylabel('Measured pressure P, mbar')


#%%


from sklearn.model_selection import train_test_split
Q_train, Q_test, P_train, P_test = train_test_split(Q,P,test_size=0.2,random_state=0)



#%%
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2)
x_poly= poly.fit_transform(Q_train)


#%%
from sklearn.linear_model import LinearRegression
reg=LinearRegression()

reg.fit(x_poly,P_train)

y_pred=reg.predict(x_poly)

#%%
print ('The model equation: \nP = ',str(reg.intercept_[0]),' + ',str(reg.coef_[0,1])+'*Q + ',str(reg.coef_[0,2])+'*Q^2')


#%%
import operator
sort_axis = operator.itemgetter(0)
sorted_zip = sorted(zip(Q_train,y_pred), key=sort_axis)
Q_train, y_pred = zip(*sorted_zip)

#%%
plt.figure()
plt.scatter(Q, P, color = 'blue', s=0.1, label='Measured values')
plt.plot(Q_train, y_pred, color = 'red', linewidth=2, markersize=2, label='Linear polynomial model')
plt.xlabel('Flow Q, ul/min')
plt.ylabel('Pressure P, mbar')
plt.legend(loc='lower right')
plt.show()


