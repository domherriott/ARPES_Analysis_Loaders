# ARPES-Analysis-Loaders
Python scripts for loading and analysing ARPES data.

## ARPES_Spatial_Map_Loader.py
### This script is designed to be used for extracting and analysing spatial map data from the Diamond Light Source IO5. It can be used to create spatial maps, energy dispersive curves from these maps, energy dispersive curves by conducting and insulating regions, and energy dispersive curves from specific spatial points.

The script consists of two functions; extractData() and ASMLoader(). The required arguments for these functions will be explained below.

#### extractData()
##### path
This should be the path for the folder that contains your nexus file.
##### filename
This should be the name of the file you wish to analyse. (N.B. This only works for nexus files, so should hend .nxs)
##### experimentName
This is the name of the experiment you want to analyse. The default for IO5 experiments is 'A_21_salsaentry_1_1'. For other formats the experiment name should be found using an HDF5 Reader.

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
