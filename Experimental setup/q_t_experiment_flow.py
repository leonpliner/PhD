#%%
'''
Experiment to determine the flow-time relationship in the microfluidic
system, containing pressure generator Fluigent Flow EZ, a microfluidic set-up
and Flow Unit sensor.

The desired flow rate this experiment is 10 ul/min and the step responce time
is 10 sec. A set pressure is applied and the measurements of pressure and flow
are taken.
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

t_step=10

t_sampling=0.1

pressure_measured=[]

flow_measured=[]

timepoint=[]

volume_utilised=0

time_passed=0

#Set the flow to the desired
    
LineUP.SetFlowrate(0, Q_d)
    
#take the measuremets over the course of 10 seconds at the sampling frequency
    
while time_passed<= t_step:
        
    pressure_measured.append(fgt_get_pressure(0))

    flow_measured.append(fgt_get_sensorValue(0))
        
    timepoint.append(time_passed)
        
    time_passed += t_sampling
        
    time.sleep(t_sampling)
    
    #add the used volume as measured flow * measurement time
    
    volume_utilised += t_sampling*flow_measured[len(flow_measured)-1]

#At the end of the experiment, set the presure to zero and finish the session

fgt_set_pressure(0, 0)
fgt_close()



'''
#save the data

dict = {'t':timepoint,'P':pressure_measured, 'Q':flow_measured}

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
plt.plot(timepoint,flow_measured)
plt.xlabel('Time t, s')
plt.ylabel('Measured flow Q, mbar')
