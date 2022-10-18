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
import threading

def countdown():
    global my_timer
    my_timer = 10

    for x in range(10):
        my_timer = my_timer - 1
        time.sleep(1)

    print("Out of time")

# test if cst file path is correct
print(cst.__file__)

start = time.time()

mesh = 1

angles = [11,42.3]

# 62238, 2644200, 12076550, 29141520, 52098224

path = 'C:/Users/pakrkoti/cernbox/Documents/DRF/Simulations/CST/Impedance_DRF63/DRF_63_Transversal.cst'

pathsplitter(path)

Results = []

countdown()

for DRFangle in angles:

    print('Currently running:' +str(DRFangle) + ' Degrees and ' +str(mesh)+ 'CpW')
    sstart = time.time()
    solver = wakefield_cst(path, xDip=5, yDip=0, xInt=-5, yInt=0, angle=DRFangle, cpw=mesh)
    [XImpedance, YImpedance, ZImpedance] = get_wakefield_results(path)
    print(XImpedance)
    plot_wakefield_results(XImpedance, YImpedance, ZImpedance)
    transverse_results = transverse_impedance(XImpedance, 2.5, 5, XImpedance, 1, 1)
    Results.append(transverse_results)
    eend = time.time()
    print('Calculation time')
    print((eend - sstart) / 60)

    # sstart = time.time()
    # solver = wakefield_cst(path, xDip=0, yDip=5, xInt=0, yInt=-5, angle=DRFangle, cpw=mesh)
    # [XImpedance, YImpedance, ZImpedance] = get_wakefield_results(path)
    # plot_wakefield_results(XImpedance, YImpedance, ZImpedance)
    # transverse_results = transverse_impedance(YImpedance, 2.5, 5, XImpedance, 1, 1)
    # Results.append(transverse_results)
    # eend = time.time()
    # print('Calculation time')
    # print((eend - sstart) / 60)
    #
    # sstart = time.time()
    # solver = wakefield_cst(path, xDip=0, yDip=-5, xInt=0, yInt=-5, angle=DRFangle, cpw=mesh)
    # [XImpedance, YImpedance, ZImpedance] = get_wakefield_results(path)
    # plot_wakefield_results(XImpedance, YImpedance, ZImpedance)
    # transverse_results = transverse_impedance(YImpedance, 2.5, 5, XImpedance, 1, 1)
    # Results.append(transverse_results)
    # eend = time.time()
    # print('Calculation time')
    # print((eend - sstart) / 60)
    #
    # sstart = time.time()
    # solver = wakefield_cst(path, xDip=0, yDip=0, xInt=5, yInt=0, angle=DRFangle, cpw=mesh)
    # [XImpedance, YImpedance, ZImpedance] = get_wakefield_results(path)
    # plot_wakefield_results(XImpedance, YImpedance, ZImpedance)
    # transverse_results = transverse_impedance(XImpedance, 2.5, 5, XImpedance, 1, 1)
    # Results.append(transverse_results)
    # eend = time.time()
    # print('Calculation time')
    # print((eend - sstart) / 60)
    #
    # sstart = time.time()
    # solver = wakefield_cst(path, xDip=0, yDip=0, xInt=0, yInt=5, angle=DRFangle, cpw=mesh)
    # [XImpedance, YImpedance, ZImpedance] = get_wakefield_results(path)
    # plot_wakefield_results(XImpedance, YImpedance, ZImpedance)
    # transverse_results = transverse_impedance(YImpedance, 2.5, 5, XImpedance, 1, 1)
    # Results.append(transverse_results)
    # eend = time.time()
    # print('Calculation time')
    # print((eend - sstart) / 60)
    #
    # sstart = time.time()
    # solver = wakefield_cst(path, xDip=0, yDip=0, xInt=0, yInt=-5, angle=DRFangle, cpw=mesh)
    # [XImpedance, YImpedance, ZImpedance] = get_wakefield_results(path)
    # plot_wakefield_results(XImpedance, YImpedance, ZImpedance)
    # transverse_results = transverse_impedance(YImpedance, 2.5, 5, XImpedance, 1, 1)
    # Results.append(transverse_results)
    # eend = time.time()
    # print('Calculation time')
    # print((eend - sstart) / 60)
    #
    # print(Results)





print(Results)


end = time.time()

print('Total calculation time')
print(str((end-start)/3600) + ' hours')