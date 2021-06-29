#%%
'''
PID control of setting the flowrate to a certain value via adjusting pressure.
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import date

from LineUP_Middleware import *
from LineUP_lowLevel import PRESSURE_UNIT   # Explicit import of available enumerations
from LineUP_lowLevel import FLOW_UNIT
from LineUP_lowLevel import PRESSURE_MODE
from LineUP_lowLevel import FLOW_UNIT_CALIBRATION_TABLE
from LineUP_lowLevel import TTL_PORT
from LineUP_lowLevel import TTL_MODE
from LineUP_lowLevel import POWER_STATE
from LineUP_lowLevel import FLOW_UNIT_TYPE

from Fluigent.SDK import fgt_init, fgt_close
from Fluigent.SDK import fgt_set_pressure, fgt_get_pressure, fgt_get_sensorValue


#%% The experiment

#initialise the session with Fluigent

fgt_init()

LineUP = LineUPClassicalSessionFactory().Create(0)

#set the ranges and experimental parameters

Q_d = 10

t_step=20

t_sampling=0.1

pressure_measured=[]

flow_measured=[]

timepoint=[]

volume_utilised=0

time_passed=0

Kp=1

Ki=1

Kd=1

Error_Q = []

E=0
Input_Q=[]

Q_in = 0
    
#take the measuremets over the course of 10 seconds at the sampling frequency
    
while time_passed<= t_step:
    
    #Perform measurements
        
    pressure_measured.append(fgt_get_pressure(0))

    flow_measured.append(fgt_get_sensorValue(0))
    
    Error_Q.append(Q_d-fgt_get_sensorValue(0))
    
    Input_Q.append(Q_in)
        
    timepoint.append(time_passed)
        
    time_passed += t_sampling
    
    #Adjust the input according to PID
    
    E=Error_Q[len(Error_Q)-1]
    
    Q_in = Kp*E + Ki*t_sampling*np.sum(Error_Q) + Kd*(flow_measured[len(flow_measured)-1] - flow_measured[len(flow_measured)-2])/t_sampling
    
    #add the used volume as measured flow * measurement time
    
    volume_utilised += t_sampling*flow_measured[len(flow_measured)-1]
    
    time.sleep(t_sampling)
    
    #Set the flow to the imput value
    
    LineUP.SetFlowrate(0, Q_in)

#At the end of the experiment, set the presure to zero and finish the session

fgt_set_pressure(0, 0)
fgt_close()



'''
#save the data

dict = {'t':timepoint,'P':pressure_measured, 'Q':flow_measured, 'Q_in':Q_in}

df=pd.DataFrame(dict)

today=date.today()

date_of_experiment = today.strftime('%d_%b_%Y')

filename='flow_time'+ date_of_experiment +'.csv'

df.to_csv(filename)
'''

#%% Data visualisation

#plot a scatterplot 

#threshold=int(number_of_repeats_per_measurement*20)
#cutoff=int(number_of_repeats_per_measurement*1)

plt.figure()

plt.subplot(3,1,1)
plt.plot(timepoint,flow_measured,color='C0')
plt.xlabel('Time t, s')
plt.ylabel('Measured flow Q, ul/min')

plt.subplot(3,1,2)
plt.plot(timepoint,Input_Q,color='C1')
plt.xlabel('Time t, s')
plt.ylabel('Input flow Q, ul/min')

plt.subplot(3,1,3)
plt.plot(timepoint,pressure_measured,color='C2')
plt.xlabel('Time t, s')
plt.ylabel('Measured pressure P, mbar')
