"""
ELISA data processing 

Data processing of the ELISA samples from GSIS experiment.

First the appropriate model for the relationship between the optical density
readings and the concentration of 'standard' solutions provided in the kit, 
is established via quadratic and cubic regression. The better of the two is 
determined visually (although cubic is recommended by the manufacturer).

During the experiment the dilution of KRB high glucose (16.7 mM) sample had
been tested on the wells E4 (dilution 1/20), E5 (1/30) and E6 (1/10).
Consequently, the dilution of 1/30 was carried forward for all the samples.

The content was also diluted on the wells G5 (1/40), G6 (1/20), G7 (1/10) and 
G8 (1/1).

The samples were occupying the following wells:
    - KRB low glucose (2.8 mM) period A1->A12 , B1->B3
    - KRB high glucose period C1->C12, D1->D12, E1->E6
    - KRB low glucose period F1->F12 , G1->G3
    - KRB low glucose control H1->H3
    - KRB high glucose control H4->H6
    - water control B4->B12
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Regression model for absorbance vs insulin concentration
data={'Known_concentration':[0,0.197,0.504,1.54,3.12,6.72],'Standard_optical_density':[0.1853862,0.1905384,0.211486,0.3549538,0.6754186,1.193362]}
df=pd.DataFrame(data)

Con=df.Known_concentration[:,np.newaxis]
St=df.Standard_optical_density[:,np.newaxis]

from sklearn.preprocessing import PolynomialFeatures
poly2 = PolynomialFeatures(degree=2)
x_poly2= poly2.fit_transform(St)

poly3 = PolynomialFeatures(degree=3)
x_poly3= poly3.fit_transform(St)

from sklearn.linear_model import LinearRegression
reg2=LinearRegression()
reg3=LinearRegression()

reg2.fit(x_poly2,Con)
reg3.fit(x_poly3,Con)

y_pred2=reg2.predict(x_poly2)
y_pred3=reg3.predict(x_poly3)

print ('Square model equation: \nCon = ',str(reg2.intercept_[0]),' + ',str(reg2.coef_[0,1])+'*St + ',str(reg2.coef_[0,2])+'*St^2')
print ('\nCubic model equation: \nCon = ',str(reg3.intercept_[0]),' + ',str(reg3.coef_[0,1])+'*St + ',str(reg3.coef_[0,2])+'*St^2 + ',str(reg3.coef_[0,3])+'*St^3')

x=np.linspace(0.0,3.0,num=3000)
y2=reg2.intercept_[0]+reg2.coef_[0,1]*x+reg2.coef_[0,2]*x**2
y3=reg3.intercept_[0]+reg3.coef_[0,1]*x+reg3.coef_[0,2]*x**2+reg3.coef_[0,3]*x**3

plt.figure()
plt.scatter(Con, St, color = 'blue', label='Measured values')
plt.plot(y2,x, color = 'red', linewidth=2, markersize=2, label='Linear quadratic model')
plt.plot(y3,x, color = 'black', linewidth=2, markersize=2, label='Linear cubic model')
plt.xlabel('Concentration of insulin, ug/L')
plt.ylabel('Optical density')
plt.legend(loc='lower right')
plt.xlim(0,10)
plt.ylim(0,2)
plt.show()


#%% ELISA data import
'''
	1	2	3	4	5	6	7	8	9	10	11	12
A	2,018699	2,042031	2,035878	2,022398	2,004807	2,041945	2,046226	2,032803	2,026511	2,047624	2,016986	2,156846
B	1,973769	1,963749	1,949643	0,1681632	0,1745819	0,1744578	0,1771074	0,2683942	0,1691025	0,3267033	0,1690594	0,1631733
C	1,759748	1,839638	1,394302	1,968488	1,946724	0,1629154	1,505982	1,232338	1,014314	1,127996	1,006019	0,832605
D	1,177076	1,070834	0,6916102	0,8286411	0,7650177	1,846838	0,5378968	0,477591	0,4715931	0,5908011	0,5405015	0,4124603
E	0,9476956	0,6458877	0,421353	0,2599212	0,1937246	0,4246712	0,1717444	0,1695049	0,1692084	0,1743506	0,1668288	0,1648865
F	0,7631415	1,28566	1,432892	1,591312	1,521064	2,102351	2,057864	2,055404	2,021239	2,009549	2,042783	2,011983
G	2,023147	2,037394	2,026183	0,1692863	2,078684	2,145769	2,082916	2,094893	0,1618705	0,1608979	0,1661031	0,1784518
H	0,1901354	0,1808179	0,1742383	0,1702762	0,1767989	0,1642345	0,1555457	0,1631407	0,1638745	0,2289974	0,4112067	0,162017
'''

import os.path
datapath=os.path.abspath(str(input('Enter the file name: ')))
dataframe = pd.read_csv(datapath, skiprows=[0,1,2,3,4,5,6,7,8,18,19,20,21,22,23,24,25,26,26], delimiter=';', usecols=[2,3,4,5,6,7,8,9,10,11,12,13])

#%% ELISA data arrays 

absorbance_datapoint_lg1='0'
absorbance_datapoint_hg1='0'
absorbance_datapoint_lg2='0'
absorbance_datapoint_lgc='0'
absorbance_datapoint_hgc='0'
absorbance_datapoint_wc='0'
absorbance_datapoint_c='0'
coefc=0

#low glucose priod 1
lg1=[]

#high glucose period
hg1=[]

#low glucose period 2
lg2=[]

#low glucose control
lgc=[]

#high glucise control
hgc=[]

#water control
wc=[]

#content
c=[]

#%% ELISA dataset fromation from the designated 96-well plate locaitons

def ab_to_con(value,coef):
    
    if isinstance(value, str)==True:
        
        value=float(value.replace(',','.'))
        
    con_value=coef*(reg3.intercept_[0]+reg3.coef_[0,1]*value+reg3.coef_[0,2]*value**2+reg3.coef_[0,3]*value**3)
    
    if con_value<0:
        
        con_value=0
    
    return con_value

for i in range (30):
    
    if i<=11:
        
        absorbance_datapoint_lg1=dataframe.iloc[0,i]
        
        absorbance_datapoint_hg1=dataframe.iloc[2,i]
        
        absorbance_datapoint_lg2=dataframe.iloc[5,i]
        
        if i<=2:
            
            absorbance_datapoint_lgc=dataframe.iloc[7,i]
            
            lgc.append(ab_to_con(absorbance_datapoint_lgc,30))
            
        elif i>2 and i<=5:
            
            absorbance_datapoint_hgc=dataframe.iloc[7,i]
            
            hgc.append(ab_to_con(absorbance_datapoint_hgc,30))
            
        lg1.append(ab_to_con(absorbance_datapoint_lg1,30))
        
        hg1.append(ab_to_con(absorbance_datapoint_hg1,30))
        
        lg2.append(ab_to_con(absorbance_datapoint_lg2,30))
        
    elif i>11 and i<=14:
        
        absorbance_datapoint_lg1=dataframe.iloc[1,i-12]
        
        absorbance_datapoint_hg1=dataframe.iloc[3,i-12]
        
        absorbance_datapoint_lg2=dataframe.iloc[6,i-12]
        
        lg1.append(ab_to_con(absorbance_datapoint_lg1,30))
        
        hg1.append(ab_to_con(absorbance_datapoint_hg1,30))
        
        lg2.append(ab_to_con(absorbance_datapoint_lg2,30))
        
    elif i>14 and i<=23:
        
        absorbance_datapoint_hg1=dataframe.iloc[3,i-12]
        
        absorbance_datapoint_wc=dataframe.iloc[1,i-12]
        
        if i==16:
            
            absorbance_datapoint_c=dataframe.iloc[6,i-12]
            
            c.append(ab_to_con(absorbance_datapoint_c,40))
            
        elif i==17:
            
            absorbance_datapoint_c=dataframe.iloc[6,i-12]
            
            c.append(ab_to_con(absorbance_datapoint_c,20))
        
        elif i==18:
            
            absorbance_datapoint_c=dataframe.iloc[6,i-12]

            c.append(ab_to_con(absorbance_datapoint_c,10))
            
        elif i==19:
            
            absorbance_datapoint_c=dataframe.iloc[6,i-12]
            
            c.append(ab_to_con(absorbance_datapoint_c,1))
        
        hg1.append(ab_to_con(absorbance_datapoint_hg1,30))
        
        wc.append(ab_to_con(absorbance_datapoint_wc,1))
        
    elif i>23 and i<=29:
        
        absorbance_datapoint_hg1=dataframe.iloc[4,i-24]
        
        hg1.append(ab_to_con(absorbance_datapoint_hg1,30))

#%% Control averages and standard deviations
water_control=np.mean(wc)
low_glucose_control=np.mean(lgc)
high_glucose_control=np.mean(hgc)
content=np.mean(c)

water_control_error=np.std(wc)
low_glucose_control_error=np.std(lgc)
high_glucose_control_error=np.std(hgc)
content_error=np.std(c)

#%% Plot of control bands on the regression curve
fig=plt.figure()
fig.set_size_inches(w=13,h=7)
plt.plot(y3,x, color = 'black', linewidth=2, markersize=2, label='Linear cubic model')
plt.fill_betweenx(x, content-content_error, content+content_error, color = 'green',alpha=0.5, label='Measured content concentration')
plt.fill_betweenx(x, low_glucose_control-low_glucose_control_error, low_glucose_control+low_glucose_control_error, color = 'yellow',alpha=0.5, label='Low glucose control')
plt.fill_betweenx(x, high_glucose_control-high_glucose_control_error, high_glucose_control+high_glucose_control_error, color = 'red',alpha=0.5, label='High glucose control')
plt.fill_betweenx(x, water_control-water_control_error, water_control+water_control_error, color = 'grey',alpha=0.5, label='Water control')
plt.xlabel('Concentration of insulin, ug/L')
plt.ylabel('Optical density')
plt.legend(loc='lower right')
plt.xlim(0.2,300)
#plt.ylim(0,2)
plt.show()

#%% Log plot of control bands on the regression curve
fig0=plt.figure()
fig0.set_size_inches(w=13,h=7)
plt.semilogx(y3,x, color = 'black', linewidth=2, markersize=2, label='Linear cubic model')
plt.fill_betweenx(x, content-content_error, content+content_error, color = 'green',alpha=0.5, label='Measured content concentration')
plt.fill_betweenx(x, low_glucose_control-low_glucose_control_error, low_glucose_control+low_glucose_control_error, color = 'yellow',alpha=0.5, label='Low glucose control')
plt.fill_betweenx(x, high_glucose_control-high_glucose_control_error, high_glucose_control+high_glucose_control_error, color = 'red',alpha=0.5, label='High glucose control')
plt.fill_betweenx(x, water_control-water_control_error, water_control+water_control_error, color = 'grey',alpha=0.5, label='Water control')
plt.xlabel('Concentration of insulin, ug/L')
plt.ylabel('Optical density')
plt.legend(loc='lower right')
plt.xlim(0.2,300)
#plt.ylim(0,2)
plt.show()

#%% Collective GSIS dataset for all periods

hg1[27]=2*hg1[27]/3
hg1[29]=hg1[29]/3

insulin_concentration=lg1+hg1+lg2

timepoint = np.arange(0,2*len(insulin_concentration),2)

#%% GSIS plot - measured concentration

fig1=plt.figure()
fig1.set_size_inches(w=13,h=10)
plt.plot(timepoint,insulin_concentration)
plt.xlabel('Time, min')
plt.ylabel('Insulin Concentraion, ug/L')
plt.title('Measured insulin concentration')

plt.show()

#%% GSIS plot - measured concentratin with control bands

fig2=plt.figure()
fig2.set_size_inches(w=13,h=10)
plt.plot(timepoint,insulin_concentration)
plt.fill_between(timepoint, content-content_error, content+content_error, color = 'green',alpha=0.5, label='Measured content concentration')
plt.fill_between(timepoint, low_glucose_control-low_glucose_control_error, low_glucose_control+low_glucose_control_error, color = 'yellow',alpha=0.5, label='Low glucose control')
plt.fill_between(timepoint, high_glucose_control-high_glucose_control_error, high_glucose_control+high_glucose_control_error, color = 'red',alpha=0.5, label='High glucose control')
plt.fill_between(timepoint, water_control-water_control_error, water_control+water_control_error, color = 'grey',alpha=0.5, label='Water control')
plt.xlabel('Time, min')

plt.title('Measured insulin concentration')
plt.show()

#%% GSIS plot - normalised concentration

number_of_islets=50

insulin_concentration=np.array(insulin_concentration)
normalised_insulin_concentration=100*insulin_concentration/(number_of_islets*content)

fig2=plt.figure()
fig2.set_size_inches(w=13,h=10)
plt.plot(timepoint,normalised_insulin_concentration)
plt.xlabel('Time, min')
plt.ylabel('Normalised Insulin Concentraion, %')

plt.title('Measured normalised insulin concentration')
plt.show()

#%% GSIS plot - normalised concentration with estimated period bands
import matplotlib as mpl

time_for_1_volume=41.25
lg1_start=0
hg1_start=30
lg2_start=60+hg1_start

c1='yellow'
c1=np.array(mpl.colors.to_rgb(c1))
c2='red'
c2=np.array(mpl.colors.to_rgb(c2))

mixing_time=90
n=mixing_time


fig3, ax =plt.subplots()
fig3.set_size_inches(w=13,h=10)

ax.axvspan(lg1_start, hg1_start, color='yellow',label='Low glucose')

for x in range(hg1_start,lg2_start):
    mix=1/(1+np.exp(-0.12*(x-hg1_start-n/2)))
    ax.axvline(x, color=mpl.colors.to_hex((1-mix)*c1 + mix*c2),linewidth=7)
    
finalmix=mix

for x in range(lg2_start,120):
    mix=finalmix/(1+np.exp(0.12*(x-lg2_start-n/2)))
    ax.axvline(x, color=mpl.colors.to_hex((1-mix)*c1 + mix*c2),linewidth=7)

plt.axvline(x=30, color="black", linestyle="--")
plt.axvline(x=30+60, color="black", linestyle="--")

plt.axvspan(118,119, color="red", label='High glucose')

plt.plot(timepoint,normalised_insulin_concentration, color='blue',label='Secreted Insulin')
plt.xlabel('Time, min')
plt.ylabel('Normalised Insulin Concentraion, %')

plt.title('Measured normalised insulin concentration')
plt.legend(loc='best')
plt.show()

#%%


