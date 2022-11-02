"""
Cell density analysis 

In the cell density experiment 2D and 3D cell cultures were prepared by seeding
MIN6 cells onto a 2D well plate at 8 different cell concentrations and also
onto a 3D B********S(R) hydroscaffold plate at 6 different concentrations.

    2D (cells per well):
        1k 2k 5k 10k 20k 50k 100k 500k

    3D (cells per well):
        10k 50k 100k 200k 500k 1M

Fluorescent imaging was performed for 4 days starting from Day 4 with Hoechst 
stainig on the blue channel to determine the cell nuclei of the live cells,
and with draq7 on the red channel to determine the dead cells. 2D images were
collected using flourescemt microscopy, and 3D images - using confocal
fluorescence mycroscopy. For 3D imaging a z-stack of 15-20 images taken at
different focal planes along the z-axis spaced by approximately 20 um to
capture the cells that have proliferated into the hydroscaffold. The stack
images were then combined into a single 2D projection image.

Percentage cell desity is worked out as the ratio between the high-intensity 
blue channel pixels indicating the cells to the total area of the image.

Some of the code related to image processing was cpoied from Sreenivas Bhattiprolu, "Python for Microscopists":
https://github.com/bnsreenu/python_for_microscopists/blob/master/033-grain_size_analysis_using_wateshed_segmentation.py

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os.path
import cv2
from scipy import ndimage
from skimage import measure, color, io


def celldensity(datapath,pixel_to_um=1.7, show=True):

    img=cv2.imread(datapath)

#pixel_to_um=1.7

    #Take the blue channel
    dapi=img[:,:,0]

    #Threshold image to binary using OTSU. ALl thresholded pixels will be set to 255
    ret1, thresh=cv2.threshold(dapi, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    #Create a working kernel matrix
    kernel3 = np.ones((3,3),np.uint8)
    kernel2 = np.ones((2,2),np.uint8)

    #Define a backgroud around the cells that is definitely not cells by using the function 'dilate'
    sure_bg = cv2.dilate(thresh,kernel2,iterations=1)

    #Apply distance trasform method to the foreground. 
    dist_transform = cv2.distanceTransform(thresh,cv2.DIST_L2,3)

    #Threshold the distance transform
    ret2, sure_fg = cv2.threshold(dist_transform,0.01*dist_transform.max(),255,0)

    #The unknown region is the difference between sure background and sure foreground
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)

    #Perform connected components algorythm without the border
    ret3, markers = cv2.connectedComponents(sure_fg)
    markers = markers+10
    markers[unknown==255] = 0
    #plt.imshow(markers, cmap='jet')

    #Perform the watershed to find the boundaries and color them yellow, excluding the borders of the image
    markers = cv2.watershed(img,markers)
    for i in range(1,len(img)-1):
        for j in range(1,len(img)-1):
            if markers[i,j]==-1:
                img[i,j]=[0,255,255]
        
        #img[markers == -1] = [0,255,255]  

    #Produce an image with marked cells
    img1 = color.label2rgb(markers, bg_label=0)
    
    #Extracting the properties of detected cells
    regions = measure.regionprops(markers, intensity_image=dapi)

    #For cell density estimation, area is imortant
    Areas=[]
    for prop in regions:
        Areas.append(prop.area)
    #Remove the background area
    Areas.pop(0)

    Total_area=float(len(img)**2)
    Cells_area=float(sum(Areas))

    density_percent=100*Cells_area/Total_area
    
    #Show the original image and the colored cells that were found
    if show==True:
        cv2.destroyAllWindows()
        cv2.imshow('Overlay on original image', img)
        cv2.imshow('Colored Grains', img1)
        cv2.waitKey(1000)
    
    return density_percent

#print('\nCell density =',round(density,2),'%')


#%%
cv2.destroyAllWindows()
cv2.imshow('Overlay on original image', img)
cv2.imshow('Colored Grains', img1)
cv2.waitKey(0)

#%%

'''/Volumes/LaCie SSD/Leonid/Imaging/Stained/MIN6_density_2D_day4_1k.tif'''


Cond=['2D','3D','3D_wb']
Day=['day4','day5','day6','day7']
Cell_conc=['1k', '2k', '5k', '10k', '20k', '50k', '100k', '200k','500k', '1M']

Results={'Condition':[], 'Day':[], 'Cell concentration':[], 'Density':[]}

common='/Volumes/LaCie SSD/Leonid/Imaging/Stained/MIN6_density_'

for cond in Cond:
    for day in Day:
        for conc in Cell_conc:
            if (cond=='2D' and (conc=='200k' or conc=='1M')) or ((cond=='3D' or cond=='3D_wb') and (conc=='1k' or conc=='2k' or conc== '5k' or conc=='20k')) or (cond=='3D_wb' and day!='day7'):
                continue
            datapath=common+cond+'_'+day+'_'+conc+'.tif'
            density=celldensity(datapath,pixel_to_um=1.7, show=True)
            Results['Condition'].append(cond)
            Results['Day'].append(day)
            Results['Cell concentration'].append(conc)
            Results['Density'].append(density)
            #print (cond,day,conc,density,'%')
            
Results_df=pd.DataFrame(Results)
#%%
plt.figure()
plt.plot(np.arange(len(Day)),Results_df['Density'][(Results_df['Condition']=='2D')&(Results_df['Cell concentration']=='1k')]) 
plt.xticks(np.arange(len(Day)),labels=Day)

'''            
datapath=common+'_'+Experiment['Condition']+'_'+Experiment['Day']+'_'+Experiment['Cell concentration']+'.tif'
datapoint=Experiment['Condition']+'_'+Experiment['Day']+'_'+Experiment['Cell concentration']
'''
