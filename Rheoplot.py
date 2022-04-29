'''
B********S(R) Rheology experiment

A classic rheology experiment was performed using the rheometer 'Anton Paar'.
The aim was to evaluate the mechanical properties of B********S(R)
hydroscaffold and to determine its storage modulus, G', indicating the elastic 
behaviour of the viscoelastic material. For this the scaffold was subjected to
shear stress with an oscillation measurement in a logarythmic amplitude sweep.

G" - the loss modulus representing the viscous phase of the biomaterial is also
recorded. Linear viscoelastic range (LVE) is the region where the change in
the shear stress does not result in the change of the storage neither in the
loss modulus. For gel-like (gel = colloid [liquid + solid] ) behaviour, G'>G"
in the LVE range.

The plot of G' and G" vs the shear strain are produced in this script.

'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os.path


#Function rheoplot() takes the path to the txt file noted from Anton Paar
#software and produces the plot of Storage and loss modulus vs strain
def rheoplot(datapath, r_t_s, colour):
    data = pd.read_csv(datapath, header=None, sep='\t', skiprows=r_t_s, usecols=range(1,6))
    data=data.stack().str.replace(',','.').unstack()
    data = data.astype(float)
    data.columns =['Strain', 'Stress', 'Storage', 'Loss', 'Loss factor']
    plt.loglog(data['Strain'],data['Storage'], '-s', color=colour)
    plt.loglog(data['Strain'],data['Loss'], '--^', color=colour)
    plt.xlabel('Shear strain $\gamma$, %')
    plt.ylabel('Storage modulus G\', Pa \nLoss modulus G\", Pa')
    Gp_max=np.amax(data['Storage'])
    Gpp_max=np.amax(data['Loss'])
    G=(Gp_max**2+Gpp_max**2)**(1/2)
    return Gp_max,Gpp_max, G
    
#%%
folder=str(input('Enter the folder name: '))
sampleset = str(input('Enter the file name: '))
r_t_s=int(input('Rows to skip: '))
n_of_samples=int(input('How many samples: '))
plot_title = str(input('Enter the plot name: '))

#A plot consisting of several datasets (1 for each sample) is genereated
Handles=[]

Gp=[]
Gpp=[]
Gt=[]

plt.figure(figsize=(8,5))
plt.title(plot_title)

for i in range(n_of_samples):
    filename=sampleset+'_'+str(i+1)+'.txt'
    datapath=os.path.abspath(folder+'/'+filename)
    colour='C'+str(i)
    Gp_max, Gpp_max, G= rheoplot(datapath,r_t_s,colour)
    Handles.append('Sample '+str(i+1)+' G\'')
    Handles.append('Sample '+str(i+1)+' G\"')
    print('\nLVR G\'=', Gp_max, 'Pa \nLVR G\"=', Gpp_max, 'Pa \nLVR G=',round(G,2),'Pa\n')
    Gp.append(Gp_max)
    Gpp.append(Gpp_max)
    Gt.append(G)
    
plt.legend(Handles,loc='best')


#Obtain the mechanical properties
mean_G=np.mean(Gt)
error_G=np.std(Gt)
print('Average shear elastic modulus =',round(mean_G,2),'±',round(error_G,2),'Pa\n')

E=3*mean_G
print('Young\'s modulus =',round(E,2),'Pa','±',round(3*error_G,2),'Pa\n')

roperties = {'G\'':Gp, 'G\"':Gpp, 'G':Gt, 'Average G':[mean_G,error_G],'E':[3*mean_G,3*error_G]}
