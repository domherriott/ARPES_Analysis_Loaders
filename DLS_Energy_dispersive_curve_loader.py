


#----------------------BEGINNING OF IMPORTS--------------------------
import numpy as np
import h5py
import matplotlib.pyplot as plt
from scipy import constants
import scipy
from scipy.interpolate import interp1d
#--------------------------END OF IMPORTS-----------------------------

#Defining physical constants
pi = scipy.pi
Me = constants.value(u'electron mass')
hbar = constants.value(u'Planck constant over 2 pi')
e = constants.value(u'elementary charge')

#Set fermi energy (can be done by seeing where the energy dispersive curve reaches a minimum)
fermiE = 0

#Set filename (must be in same directory)
filename = "i05-1-14626.nxs"
f = h5py.File(filename, "r")
dsIntensity = f["/entry1/analyser/data"][0]
dsEnergyValues = f["/entry1/analyser/energies"]
dsAngles = f["/entry1/analyser/angles"]

#Fermi energy is repeated across array so that it can be subtracted from the energy values dataset
dsFermiEnergy = np.repeat(fermiE, len(dsEnergyValues))
dsEnergyValuesShifted = dsEnergyValues - dsFermiEnergy

#Mean energy is calculated so an estimate of the momentum can be calculated
meanE = np.mean(dsEnergyValues)
dsk = (2*Me*e*meanE)**(0.5) * 0.0173648 * dsAngles[:] * ( 3.925 * (10 ** -10) /pi) /hbar

#Intensity data is integrated across all angles/momentum
dsDOSfull = np.mean(dsIntensity, axis=0)
#Intensity data is normalised so maximum is 1
dsDOSfull = dsDOSfull / np.max(dsDOSfull)

#The data is selected to be plotted
xs = dsEnergyValuesShifted
ys = dsDOSfull

#Energy dispersive curve is plotted across full angular range
fig, (ax0) = plt.subplots(nrows=1,figsize=(8,5))
ax0.set_title("Energy Dispersive Curve integrated along the entirety of the Brillouin Zone cut")
plt.plot(xs, ys, color="xkcd:turquoise")
plt.plot((0,0),(0, 1.1), linestyle = 'dashed', color="black")
plt.ylabel("Normalised Intensity")
plt.xlabel("$E-E_{F}$ ($eV$)")

#Following lines can be included to improve aesthetics of plot
#plt.xlim((-0.8,0.2))
#plt.ylim((0,1.1))

#Following lines can be included to improve aesthetics of x ticks
#xticks = np.arange(-0.8,0.21,0.1)
#plt.xticks(xticks)
#plt.minorticks_on()

plt.tight_layout()
plt.show()

#Figure is created to be used for different momentum cuts
fig, (ax0) = plt.subplots(nrows=1,figsize=(8,5))

#Momentum range is selected by the lowest value, highest value and the step
kmin = 0
kmax = 2
kstep = 0.4
kRange = np.arange(kmin,kmax,kstep)

#The momentum range is iterated over, each time calculating the energy dispersive curve for that range
#These curves are then plotted on top of each other on a single figure
for i in kRange:
    kMid = np.around(i,1)
    kHalfRange = kstep/2
    kMin = np.around(kMid - kHalfRange, 1)
    kMax = np.around(kMid + kHalfRange, 1)
    kMinIndex = (np.abs(dsk - kMin)).argmin()
    kMaxIndex = (np.abs(dsk - kMax)).argmin()
    dsIntensitySlice = dsIntensity[kMinIndex:kMaxIndex,]
    dsDOSslice = np.mean(dsIntensitySlice, axis=0)
    xs = dsEnergyValuesShifted
    ys = dsDOSslice
    plt.plot(xs, ys, label=(str(kMin) + " to " + str(kMax)))

#Aesthetics are selected for plot of different momentum cuts
plt.title("Energy Dispersive Curves integrated along different regions of the Brillouin Zone cut")
plt.ylabel("Normalised Intensity")
plt.plot((0,0),(0, 1.1), linestyle = 'dashed', color="black")
plt.xlabel("$E-E_{F}$ ($eV$)")
plt.legend(title="Range of k ($\pi / a$):")

#Following lines can be included to improve aesthetics of plot
#plt.xlim((-0.8,0.2))
#plt.ylim((0,1.1))

#Following lines can be included to improve aesthetics of x ticks
#xticks = np.arange(-0.8,0.21,0.1)
#plt.xticks(xticks)
#plt.minorticks_on()

fig.tight_layout()
plt.tight_layout()
plt.show()

