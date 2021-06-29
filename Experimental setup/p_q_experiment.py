#%%
'''
Experiment to determine the pressure-flow relationship in the microfluidic
system, containing pressure generator Fluigent Flow EZ, a microfluidic set-up
and Flow Unit sensor.

The pressure range for this experiment is [0,300] mbar and the step is 1 mbar.
The time step is 10 sec. A set pressure is applied and then given 5 seconds
for pressure to settle. Then measurements of pressure and flow are taken for
5 seconds.
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import date

from Fluigent.SDK import fgt_init, fgt_close
from Fluigent.SDK import fgt_set_pressure, fgt_get_pressure, fgt_get_sensorValue




#%% The experiment

#initialise the session with Fluigent

fgt_init()

#set the ranges and experimental parameters

P_min=0

P_max=300

P_step=1

t_halfstep=5

t_sampling=0.1




number_of_measurements=(P_max-P_min)/P_step + 1

number_of_repeats_per_measurement=(t_halfstep/t_sampling)

number_of_datapoints=number_of_repeats_per_measurement*number_of_measurements




pressure_measured=[]

flow_measured=[]

volume_utilised=0


#each measurement is an iteration of the while loop

P_in=P_min

while P_in<=P_max:
    
    #first check there is enough liquid
    
    if volume_utilised >= 10000:
        
        #pause the experiment and set pressure to 0 untill the required volume is restored
        
        fgt_set_pressure(0, 0)
        
        input('\nLow liquid volume. Pour more liquid and press Enter to continue...')
        
        volume_utilised=0
        
    else:
        
        pass

    #Set the pressure to a new value
    
    fgt_set_pressure(0,P_in)
    
    #allow the pressure to settle
    
    time.sleep(t_halfstep)
    
    #take the measuremets over the course of 5 seconds at the sampling frequency
    
    for t in range (int(number_of_repeats_per_measurement)):
        
        pressure_measured.append(fgt_get_pressure(0))
        
        flow_measured.append(fgt_get_sensorValue(0))
        
        time.sleep(t_sampling)
    
    #add the used volume as mean flow * time passed
    
    volume_utilised += 2*t_halfstep*np.mean(flow_measured[int(number_of_repeats_per_measurement*(P_in-1)):int(number_of_repeats_per_measurement*P_in)])
    
    #define the next input pressure 
    
    P_in += P_step




#At the end of the experiment, set the presure to zero and finish the session

fgt_set_pressure(0, 0)
fgt_close()




#save the data

dict = {'P':pressure_measured, 'Q':flow_measured}

df=pd.DataFrame(dict)

today=date.today()

date_of_experiment = today.strftime('%d_%b_%Y')

filename='pressure_flow_'+ date_of_experiment +'.csv'

df.to_csv(filename)

#%% Data visualisation

#plot a scatterplot 

threshold=int(number_of_repeats_per_measurement*224)
cutoff=int(number_of_repeats_per_measurement*1)

plt.figure()
plt.scatter(flow_measured[:threshold],pressure_measured[:threshold],s=0.1)
plt.xlabel('Measured flow Q, ul/min')
plt.ylabel('Measured pressure P, mbar')

x=[]
y=[]
for n in range (600):
    x.append(n)
    y.append(0.33*n)

plt.plot(x,y,'r')


