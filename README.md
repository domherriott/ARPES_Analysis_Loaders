# ARPES_Analysis_Loaders
Python scripts for loading and analysing ARPES data.

---

## SOLEIL_ARPES_Spatial_Map_Loader.py
### This script is designed to be used for extracting and analysing spatial map data from SOLEIL ARPES experiments. It can be used to create spatial maps, energy dispersive curves from these maps, energy dispersive curves by conducting and insulating regions, and energy dispersive curves from specific spatial points.

The script consists of two functions; extractData() and ASMLoader(). The required arguments for these functions will be explained below.

#### extractData()
##### path
This should be the path for the folder that contains your nexus file.
##### filename
This should be the name of the file you wish to analyse. (N.B. This only works for nexus files, so should end .nxs)
##### experimentName
This is the name of the experiment you want to analyse. The default for SOLEIL experiments is 'A_21_salsaentry_1_1'. For other formats the experiment name should be found using an HDF5 Reader.

#### ASMLoader()
##### energyInputLowerBound
This is the lower energy bound that you want to consider for your spatial map (in eV).
##### energyInputUpperBound
This is the upper energy bound that you want to consider for your spatial map (in eV).
##### numberOfColourBins
This determines the number of colour bins you wish to use for the spatial map (default = 20).
##### markCross
This determines whether a cross is featured on the spatial map to mark which specific point is being considered for the final energy dispersive curve. If 'markCross = True', the cross will be shown. If 'markCross = False', it will not.
##### xPosSpectra
This determines the value along the x axis in real space you wish to consider for the final energy dispersive curve.
##### yPosSpectra
This determines the value along the y axis in real space you wish to consider for the final energy dispersive curve.

---
## DLS_ARPES_Spatial_Map_Loader.py
### This script is designed to be used for extracting and analysing spatial map data from Diamond Light Source IO5 ARPES experiments. It can be used to create spatial maps.

The script does not consist of functions but does have variables within the code that can be altered by the user. These are;

#### numberOfColourBins
This determines the number of colour bins you wish to use for the spatial map (default = 20).
#### filename
This should be the name of the file you wish to analyse. The script file and the file to be analysed MUST be in the same directory. (N.B. This only works for nexus files, so should end .nxs)

---
## Energy_dispersive_curve_loader.py
### This script is designed to be used for extracting and analysing energy dispersive curve data from Diamond Light Source IO5 ARPES experiments. It can be used to create energy dispersive curve plots for the full range of momenta measured, and also split by momentum to show how it varies with k.

The script does not consist of functions but does have variables within the code that can be altered by the user. These are;

#### fermiE
This must be defined by the user by running the script with 'fermiE = 0', and by then determining at which value the fermi energy has been reached as where the curves plateau.  
##### filename
This should be the name of the file you wish to analyse. The script file and the file to be analysed MUST be in the same directory. (N.B. This only works for nexus files, so should end .nxs)
##### kmin
This is to be set as, when iterating across momenta, the starting value to be considered. (Default = 0)
##### kmax
This is to be set as, when iterating across momenta, the final value to be considered. (Default = 2)
##### kstep
This is to be set as, when iterating across momenta, the steps to be taken between kmin and kmax. (Default = 0.4)

In addition to these variables there is also code between lines 54-61 and 97-104 which can be uncommented to improve the aesthetics of the figures produced.
