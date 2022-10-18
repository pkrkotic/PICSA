#################################################

# CST Wakefield Impedance Solver Tool Version 0.1
# By Patrick Krkotic

#################################################

############## Libraries
import os
import sys
from functions import *
import colorama
from colorama import Fore, Style
import shutil
import time
#Include the path for your computer where CST is installed
sys.path.append(r"C:/Program Files (x86)/CST Studio Suite 2020/AMD64/python_cst_libraries")

# import the cst library
import cst

# test if cst file path is correct
print(cst.__file__)

start = time.time()

meshes = [1,2]

angles = [11]

# 62238, 2644200, 12076550, 29141520, 52098224

path = 'C:/Users/pakrkoti/cernbox/Documents/DRF/Simulations/CST/Impedance_DRF63/DRF_63_Longitudinal.cst'

pathsplitter(path)

Results = []

for DRFangle in angles:
    for mesh in meshes:

        #try:
        print('Currently running:' +str(DRFangle) + ' Degrees and ' +str(mesh)+ 'CpW')
        sstart = time.time()

        solver = wakefield_cst(path, xDip = 0, yDip = 0, xInt = 0, yInt=0, angle = DRFangle, cpw = mesh)

        [XImpedance, YImpedance, ZImpedance] = get_wakefield_results(path)

        plot_wakefield_results(XImpedance, YImpedance, ZImpedance)

        longitudinalresults = longitudinal_impedance(ZImpedance, 2.5, 11245)

        Results.append(longitudinalresults)

        eend = time.time()

        print('Calculation time')
        print((eend - sstart) / 60)

        print(Results)

        #except:
        #    print('Oups')
         #   continue



print(Results)


end = time.time()

print('Total calculation time')
print(str((end-start)/3600) + ' hours')