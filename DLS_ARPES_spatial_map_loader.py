


#----------------------BEGINNING OF IMPORTS--------------------------
import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
#--------------------------END OF IMPORTS-----------------------------

#Determines the number of colour bins to be used
numberOfColourBins = 20

#Selects file to be extracted. Must be in the same directory.
filename = ".nxs"
f = h5py.File(filename, "r")

#Extracts the intensity dataset, the energy values, the angular values and the x and y positions
dsIntensity = f["/entry1/analyser/data"]
dsEnergyValues = f["/entry1/analyser/energies"]
dsAngles = f["/entry1/analyser/angles"]
dsX = f["/entry1/analyser/smx"][0,:]
dsY = f["/entry1/analyser/smy"][:,0]

#Normalising dsX and dsY to have origin of map at (0,0)
dsX = dsX - dsX[0]
dsY = dsY - dsY[0]

#Creates an empty array, the same size of the ARPES spatial map
dsIntensityMapping = np.zeros((len(dsY),len(dsX)))

#Due to the size of the array it cannot be fully extracted as a numpy array. Therefore it must be opened
#iteratively instead
print('Started data extraction')
for i in range(0, len(dsX)):
    for j in range(0, len(dsY)):
        dsIntensityMapping[j,i] = np.mean(dsIntensity[j,i,:,:])
print('Completed data extraction')

#Finds the increment amount in x and in y
dx = dsX[1] - dsX[0]
dy = dsY[1] - dsY[0]

#Determines the minimum and maximum x and y values
xMin = 0
xMax = dsX[len(dsX)-1] - dsX[0]
yMin = 0
yMax = dsY[len(dsY)-1] - dsY[0]
 
# generate 2 2d grids for the x & y bounds
xs = np.mgrid[slice(xMin, xMax + dx, dx)]
ys = np.mgrid[slice(yMin, yMax + dy, dy)]

#Normalises the data
dsIntensityMapping = dsIntensityMapping / np.max(dsIntensityMapping)
zs = dsIntensityMapping

# x and y are bounds, so z should be the value *inside* those bounds.
# Therefore, remove the last value from the z array.
zs = zs[:, :]
zs = np.rot90(zs)
zs = np.rot90(zs)
zs =  np.fliplr(zs)

#Plots the ARPES spatial map
cmap = plt.get_cmap("inferno")
levels = MaxNLocator(nbins=numberOfColourBins).tick_values(0,1)
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
width = 8
height = (width/len(xs))*len(ys) * 0.8
plt.figure(figsize=(width,height))
plt.pcolormesh(xs, ys, zs, cmap=cmap, norm=norm)
plt.colorbar(ticks=(0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0), label="Normalised Intensity")
plt.title("ARPES Spatial Map")
plt.ylabel("$y$ $(\mu m)$")
plt.xlabel("$x$ $(\mu m)$")
plt.minorticks_on
plt.tight_layout()
plt.show()

#Closes nexus file 
f.close()
