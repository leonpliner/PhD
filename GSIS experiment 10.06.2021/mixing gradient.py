"""
Mixing time estimation

This is a complementary experiment to the GSIS experiment on 10.06.2021

Mixing of two colored solutions with concentration ratio Low:High=1:6 was 
sampled onto the 96 well plate. During this, the system previously, had been 
filled with Low solution, was perfused with High solution at flow rate Q=50 ul/
min for 24 minutes.

The plate has following layout:
    - Mixing gradient 1A->1H + 2A->2H + 3A->3H
    - Low control 4A->4H 
    - High control 5A->5H
    
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os.path
datapath=os.path.abspath(str(input('Enter the file name: ')))
dataframe = pd.read_csv(datapath, delimiter=';', usecols=[1,2,3,4,5])

#%%
for i in range(dataframe.shape[0]):
    for j in range(dataframe.shape[1]):
        dataframe.iloc[i,j]=float(dataframe.iloc[i,j].replace(',','.'))

#%%
mixing_grad=np.array([])
Low_control=np.array([])
High_control=np.array([])

mixing_grad=np.append(mixing_grad,[dataframe.loc[:,['1']].values, dataframe.loc[:,['2']].values,dataframe.loc[:,['3']].values])
Low_control=np.append(Low_control,dataframe.loc[:,['4']].values)
High_control=np.append(High_control,dataframe.loc[:,['5']].values)

#%%
Low_control_mean=np.mean(Low_control)
High_control_mean=np.mean(High_control)

Low_control_error=np.std(Low_control)
High_control_error=np.std(High_control)

#%%
k=0
mixing_time=0
while mixing_grad[k]<High_control_mean-High_control_error:
    mixing_time=k+1
    k+=1

print('\nThe time taken for the solutions to mix is ',mixing_time,'minutes \n')

#%%
timepoint_np = np.arange(0,len(mixing_grad),1)
timepoint=timepoint_np.tolist()
#%%
fig=plt.figure()
fig.set_size_inches(w=13,h=10)
plt.plot(timepoint,mixing_grad,'o-b',label='Measured values')
plt.axhline(y=High_control_mean, color="red", linestyle="--", label='High solution absorbance')
plt.axhline(y=Low_control_mean, color="orange", linestyle="--", label='Low solution absorbance')
plt.axvline(x=mixing_time, color="grey", linestyle="--")
plt.axhspan(Low_control_mean-Low_control_error,Low_control_mean+Low_control_error,alpha=0.5,color="yellow")
plt.axhspan(High_control_mean-High_control_error,High_control_mean+High_control_error,alpha=0.5,color="red")
plt.xlabel('Time, minutes')
plt.ylabel('Absorbance at 580 nm')
plt.legend(loc='lower right')
plt.title('Time taken for the solution to mix from Low to High concentration')
plt.xticks(timepoint)
plt.show()


#%%
y=(High_control_mean-Low_control_mean)/(1+np.exp(-0.65*(timepoint_np-10.5)))+Low_control_mean


fig1=plt.figure()
fig1.set_size_inches(w=13,h=10)
plt.plot(timepoint,y,color='blue',linestyle='--',label='Logistic sigmoid approximation')
plt.plot(timepoint,mixing_grad,'o-b',label='Measured values')
plt.axhline(y=High_control_mean, color="red", linestyle="--", label='High solution absorbance')
plt.axhline(y=Low_control_mean, color="orange", linestyle="--", label='Low solution absorbance')
plt.axvline(x=mixing_time, color="grey", linestyle="--")
plt.axhspan(Low_control_mean-Low_control_error,Low_control_mean+Low_control_error,alpha=0.5,color="yellow")
plt.axhspan(High_control_mean-High_control_error,High_control_mean+High_control_error,alpha=0.5,color="red")
plt.xlabel('Time, minutes')
plt.ylabel('Absorbance at 580 nm')
plt.legend(loc='best')
plt.title('Time taken for the solution to mix from Low to High concentration')
plt.xticks(timepoint)
plt.show()

#%%

fig1=plt.figure()
fig1.set_size_inches(w=13,h=10)
plt.plot(timepoint,y,color='blue',linestyle='--',label='Logistic sigmoid approximation')
plt.scatter(timepoint,mixing_grad,c=y,cmap='autumn_r',label='Measured values')
plt.axhline(y=High_control_mean, color="red", linestyle="--", label='High solution absorbance')
plt.axhline(y=Low_control_mean, color="orange", linestyle="--", label='Low solution absorbance')
plt.axvline(x=mixing_time, color="grey", linestyle="--")
plt.axhspan(Low_control_mean-Low_control_error,Low_control_mean+Low_control_error,alpha=0.5,color="yellow")
plt.axhspan(High_control_mean-High_control_error,High_control_mean+High_control_error,alpha=0.5,color="red")
plt.xlabel('Time, minutes')
plt.ylabel('Absorbance at 580 nm')
plt.legend(loc='best')
plt.title('Time taken for the solution to mix from Low to High concentration')
plt.xticks(timepoint)
plt.show()
