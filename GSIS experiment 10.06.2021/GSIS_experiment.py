'''
Experiment to determine the dependance of insulin secretion on the glucose 
concentration in media/buffer.

The protocol includes passing different solutions through the microfluidic
device with seeded islets in the following order:
    
    1) KRB Low glucose 30 min
    2) KRB High glucose 60 min
    3) KRB Low glucose 30 min
    
The flowrate is 10 ul/min. The collection of samples is done every 2 mins onto
the 96 well plate to then be taken for ELISA.

The pressure for this experiment is ___ mbar and is determined from 
p-q experiment preseeding this and in accordance with the total volume of the 
system.
'''

import winsound as ws
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import date

from Fluigent.SDK import fgt_init, fgt_close
from Fluigent.SDK import fgt_set_pressure, fgt_get_pressure, fgt_get_sensorValue


#%% The experiment

P_in= 42

Step_duration = [30*60, 60*60, 30*60]
Message = ['\nChange the tube for KRB High Glucose and press Enter to continue...\n',
           '\nChange the tube for KRB Low Glucose and press Enter to continue...\n',
           '\nPress Enter to finish\n',]

#initialise the session with Fluigent

fgt_init()

for i in range(len(Step_duration)):

    #set the pressure to the desired value for the desired flow    

    fgt_set_pressure(0, P_in)
    
    #no sample collection during the first and last step
    
    if i ==-1 or i == 4:
        
        time.sleep(Step_duration[i])
        
    #The sample is collected during the Steps 2)-4)
        
    else:
        
        time_end= time.time()+Step_duration[i]

        while time.time() < time_end:
            
            print('\nCollect now')
            
            ws.Beep(600,986)
            
            time.sleep(59)
            
            print('\nStop collecting\n')
            
            time.sleep(60)

    fgt_set_pressure(0, 0)

    #change the tube with the solution
    input(Message[i])

#At the end of the experiment, set the presure to zero and finish the session

fgt_set_pressure(0, 0)
fgt_close()
