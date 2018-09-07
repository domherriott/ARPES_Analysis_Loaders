# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 17:05:55 2018

@author: herri
"""

#----------------------BEGINNING OF IMPORTS--------------------------
import numpy as np
import math
import h5py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import os
#--------------------------END OF IMPORTS-----------------------------

def extractData(path, filename, experimentName):
    os.chdir(path)
    hdf5FileName = filename
    f = h5py.File(hdf5FileName, "r")
    
    global dsAct1, dsAct2, dsEnergyValues, dsIntensity
    dsAct1 = f["/"+str(experimentName)+"/scan_data/trajectory_1_1"]
    #dsAct1 stores the variation of the first actuator in real space
    dsAct2 = f[""+str(experimentName)+"/scan_data/trajectory_2_1"]
    #dsAct2 stores the variation of the second actuator in real space
    dsEnergyValues = f["/"+str(experimentName)+"/scan_data/data_02"]
    #Three dimensional data set of XxYxE, therefore showing the energy cut at each pixel in X and Y.
    #The energy cuts are the same at each pixel.
    dsIntensity = f["/"+str(experimentName)+"/scan_data/data_01"]
    #Three dimensional data set of XxYxI, therefore showing the measured intensities at each energy cut (see above) at each pixel.
    #These values are the sum across all angles.
    #It can therefore be summed up in differing amounts to get different VB maps.

    
def ASMLoader(energyInputLowerBound, energyInputUpperBound, numberOfColourBins, markCross, xPosSepctra, yPosSpectra):
    #Debugging
    if (energyInputLowerBound > energyInputUpperBound):
        print("ERROR! energyInputLowerBound must be lower than energyInputUpperBound")
        return
    elif (energyInputLowerBound == energyInputUpperBound):
        print("WARNING! energyInputLower is equal to energyInputUpperBound. Intensity mean will only consider one energy cut.")
    
    #Creates list of all the energy cuts
    energyList = np.ndarray.tolist(dsEnergyValues[0][0])
    #Prints the smallest and largest energies from the energy cuts.
    print("\nSmallest selectable energy = " + str(min(energyList)))
    print("Largest selectable energy = " + str(max(energyList)))
    energyLowerBound = min(energyList, key=lambda x:abs(x-energyInputLowerBound))
    #Prints which energy cuts were selected for the ARPES Spatial Map image.
    print("Selected energy lower bound = " + str(energyLowerBound))
    energyUpperBound = min(energyList, key=lambda x:abs(x-energyInputUpperBound))
    print("Selected energy upper bound = " + str(energyUpperBound))
    print("\n" + "---------------------------------------------------------------------" + "\n")
    
    #Finds the indexes of the set Lower and Upper energy bounds to be later used to slice the
    #intensity dataset.
    indexUpper = energyList.index(energyUpperBound)
    indexLower = energyList.index(energyLowerBound)
    
    #Takes a slice of the intensity datset in the selected energy region
    dsIntensitySlice = dsIntensity[:,:,indexLower:indexUpper]
    
    #Calculates the intensity mean from the selected energy range
    selectedMean = np.mean(dsIntensitySlice, axis = 2)
    
    #Using selectedMean, the top and bottom percentiles are selected. These are used to find the most and
    #least conducting regions
    lowerBarrier = np.percentile(selectedMean, 1)
    upperBarrier = np.percentile(selectedMean, 99)
    
    #Masks of the ARPES Spatial Map are created using the lowerBarrier and upperBarrier
    topPercentilesMask = np.ma.masked_less(selectedMean, upperBarrier).mask
    bottomPercentilesMask = np.ma.masked_greater(selectedMean, lowerBarrier).mask
    
    #The masks are expanded into a third dimension, so they can later be used on the original dataset
    topPercentiles3d = np.expand_dims(topPercentilesMask, axis=2)
    topPercentiles3d = np.repeat(topPercentiles3d, 1064, axis=2)
    bottomPercentiles3d = np.expand_dims(bottomPercentilesMask, axis=2)
    bottomPercentiles3d = np.repeat(bottomPercentiles3d, 1064, axis=2)
    
    #Masks are applied to the original dataset
    topPercentilesData = np.ma.array(dsIntensity, mask=topPercentiles3d)
    y3 = np.mean(topPercentilesData, axis=(0,1))
    bottomPercentilesData = np.ma.array(dsIntensity,mask=bottomPercentiles3d)
    y4 = np.mean(bottomPercentilesData, axis=(0,1))
    x3 = energyList
    
    #Conducting and insulating EDCs are plotted
    fig3, (ax3) = plt.subplots(nrows=1,figsize=(8,3))
    ax3.set_title("Energy Dispersive Cut for conducting and insulating regions")    
    plt.plot(x3,y3, label = 'Conducting')
    plt.plot(x3,y4, label = 'Insulating')
    plt.ylabel("Intensity")
    plt.xlabel("Kinetic Energy")
    ax3.set_xlim([min(x3),max(x3)])
    ax3.set_ylim([min(y3),max(y3)+200])
    plt.xticks(np.arange(round(min(x3),1), round(max(x3),1), 0.5))
    fig3.tight_layout()
    
    #Determines the x and y axes, and their incremements
    dx = dsAct1[1] - dsAct1[0]
    dy = dsAct2[1] - dsAct2[0]
    xMin = 0
    xMax = dsAct1[80] - dsAct1[0]
    yMin = 0
    yMax = dsAct2[80] - dsAct2[0]
    
    # generate 2 2d grids for the x & y bounds
    xs = np.mgrid[slice(xMin, xMax + dx, dx)]
    ys = np.mgrid[slice(yMin, yMax + dy, dy)]

    #Mean intensity is generated across all space
    arrMeanSpectra = np.mean(dsIntensity, axis=(0,1))
    
    #Plots average spectra from all positions
    x0 = energyList
    y0 = arrMeanSpectra
    fig0, (ax0) = plt.subplots(nrows=1,figsize=(8,3))
    ax0.set_title("Mean Energy Dispersive Cut")    
    plt.plot(x0,y0)
    plt.ylabel("Intensity")
    plt.xlabel("Kinetic Energy")
    ax0.set_xlim([min(x0),max(x0)])
    ax0.set_ylim([min(y0),max(y0)+200])
    plt.xticks(np.arange(round(min(x0),1), round(max(x0),1), 0.5))
    ax0.add_patch(
    patches.Rectangle(
        (energyLowerBound, 0),
        (energyUpperBound - energyLowerBound),
        (max(y0)+200),  
        edgecolor="black" , facecolor="#f2f2f2"))
    fig0.tight_layout()
    
    #Determines the real space positions (x and y) closest to the inputted Spectra position
    print("Smallest selectable spectra x position = " + str(min(xs)))
    print("Largest selectable spectra x position = " + str(max(xs)))
    print("Smallest selectable spectra y position = " + str(min(ys)))
    print("Largest selectable spectra y position = " + str(max(ys)))
    xPosSpectra = min(xs, key=lambda x:abs(x-xPosSpectraInput))
    xIndex = list(xs).index(xPosSpectra)
    print("Selected spectra x position = " + str(xPosSepctra))
    yPosSpectra = min(ys, key=lambda x:abs(x-yPosSpectraInput))
    yIndex = list(ys).index(yPosSpectra)
    print("Selected spectra y position = " + str(yPosSpectra))
    print("\n" + "---------------------------------------------------------------------" + "\n")
    
    #Take the mean intensity across the sliced Intensity dataset, dsIntensity
    arrIntensityMean = np.empty([80,80])
    arrIntensityMean = np.mean(dsIntensitySlice, axis=2)
    
    zs = arrIntensityMean
    # x and y are bounds, so z should be the value *inside* those bounds.
    # Therefore, remove the last value from the z array.
    zs = zs[:-1, :-1]
    #zs =  np.fliplr(zs)
    
    #Determins the range for the ARPES spatial map
    levels = MaxNLocator(nbins=numberOfColourBins).tick_values(zs.min(), zs.max())

    #Plots the ARPES spatial map
    cmap = plt.get_cmap("inferno")
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    fig1, (ax1) = plt.subplots(nrows=1,figsize=(8,6))
    im = ax1.pcolormesh(xs, ys, zs, cmap=cmap, norm=norm)
    fig1.colorbar(im, ax=ax1)
    ax1.set_title("Valence Band Spatial Map ["+str(numberOfColourBins)+" colour bins]")
    plt.ylabel("y")
    plt.xlabel("x")
    if (markCross == True):
        plt.plot(xPosSpectra, yPosSpectra, color="white", marker="x", markersize="16", markeredgewidth="3.0")
    fig1.tight_layout()
    plt.show()

    #Extracts the intensity values at the inputted position
    dsSpectra = dsIntensity[yIndex,xIndex,:]
    
    #Plots spectra for the position marked at X on the VB Spatial Map
    x2 = energyList
    y2 = dsSpectra
    fig2, (ax2) = plt.subplots(nrows=1,figsize=(8,3))
    ax2.set_title("Energy Dispersive Cut at x=" + str(xPosSepctra) + ", y=" + str(yPosSpectra))
    plt.plot(x2,y2)
    plt.ylabel("Intensity")
    plt.xlabel("Kinetic Energy")
    ax2.set_xlim([min(x2),max(x2)])
    ax2.set_ylim([min(y2),max(y2)+200])
    plt.xticks(np.arange(round(min(x2),1), round(max(x2),1), 0.5))
    ax2.add_patch(
    patches.Rectangle(
        (energyLowerBound, 0),
        (energyUpperBound - energyLowerBound),
        (max(y2)+200),  
        edgecolor="black" , facecolor="#f2f2f2"))
    fig2.tight_layout()




#Inputs for extractData()
path = r""
filename = r".nxs"
experimentName = "A_21_salsaentry_1_1"

#Inputs for ASMLoader()
energyInputLowerBound = 95.4
energyInputUpperBound = 96
numberOfColourBins = 20
markCross = False
xPosSpectraInput = 11
yPosSpectraInput = 4

extractData(path, filename, experimentName)
ASMLoader(energyInputLowerBound, energyInputUpperBound, numberOfColourBins, markCross, xPosSpectraInput, yPosSpectraInput)
