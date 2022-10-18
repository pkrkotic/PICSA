#################################################

# PICSA Version 0.1
# By Patrick Krkotic

#################################################

############## Python Libraries
import os
import sys
from functions import *
import colorama
from colorama import Fore, Style
import shutil
import time


############## include the path where CST is installed on your local device
sys.path.append(r"C:/Program Files (x86)/CST Studio Suite 2020/AMD64/python_cst_libraries")


############## CST Libraries
# import the cst library
import cst
# test if cst file path is correct
print(cst.__file__)



total_start = time.time()
Results_Longitudinal = []
Results_Transverse = []
Results_Eigenmode = []
angles = [11, 43.2]

for DRFangle in angles:
    print('Currently running:' + str(DRFangle) + 'Degrees')
    simulation_counter = 0
    
    ########
    #Longitudinal Study
    ########
    try:
        # path to cst file and name of the file
        path = 'C:/Users/Simulations/CST/Impedance_DRF/DRF_150_Longitudinal.cst'
        
        # pathsplitter is necessary to separate the cst file from the path
        pathsplitter(path)
        
        # arbitraty 
        start = time.time()
        simulation_counter = simulation_counter + 1
        print('Current Simulation Number: ' + str(simulation_counter))
        
        # the function wakefield_cst opens the cst file and starts the simulation with 
        # the parameters given by the user. The parameters have to be pre defined 
        # in the original CST file 
        solver = wakefield_cst(path, xDip=0, yDip=0, xInt=0, yInt=0, angle=DRFangle, cpw=120, wakelength=50000)
        
        # the function get_wakefield_results exports the results from CST into python
        [XImpedance_Longi, YImpedance_Longi, ZImpedance_Longi] = get_wakefield_results(path)
        
        # the function plot_wakefield_results visualises the exported results
        plot_wakefield_results(XImpedance_Longi, YImpedance_Longi, ZImpedance_Longi)
        
        # the function longitudinalresults calculates the Z/n value of the longitudinal impedance
        longitudinalresults = longitudinal_impedance(ZImpedance_Longi, 2.5, 11245)
        
        #arbitrary
        Results_Longitudinal.append(longitudinalresults)
        end = time.time()
        print('Calculation time for Simulation Number: ' + str(simulation_counter))
        print((end - start) / 60)
    
    except:
        print('Something went wrong for simulation' + str(simulation_counter))
        pass

    
    
    #######
    ##Transverse Study
    #######
    # similar as the longitudinal with the only difference in calling the transverse_impedance function
    try:
       path = 'C:/Users/Simulations/CST/Impedance_DRF/DRF_150_Trans2.cst'
       pathsplitter(path)
       start = time.time()
       simulation_counter = simulation_counter + 1
       print('Current Simulation Number: ' + str(simulation_counter))
       solver = wakefield_cst(path, xDip=0, yDip=10, xInt=0, yInt=-10, angle=DRFangle, cpw=120, wakelength=50000)
       [XImpedance_Trans2, YImpedance_Trans2, ZImpedance_Trans2] = get_wakefield_results(path)
       plot_wakefield_results(XImpedance_Trans2, YImpedance_Trans2, ZImpedance_Trans2)
       transverse_results_Trans2 = transverse_impedance(YImpedance_Trans2, 2.5, 10, YImpedance_Longi, 1, 1)
       Results_Transverse.append(transverse_results_Trans2)
       end = time.time()
       print('Calculation time for Simulation Number: ' + str(simulation_counter))
       print((end - start) / 60)
       print(Results_Trans2)
    except:
       print('Something went wrong for simulation' + str(simulation_counter))
       pass

    
    
   
    #######
    ##Eigenmode Study
    #######
    try:
        path = 'C:/Users/pakrkoti/cernbox/Documents/DRF/Simulations/CST/DRF_63/test.cst'
        pathsplitter(path)
        start = time.time()
        simulation_counter = simulation_counter + 1
        print('Current Simulation Number: ' + str(simulation_counter))
        
        # the function eigenmode_cst opens the cst file and starts the simulation with 
        # the parameters given by the user. The parameters have to be pre defined 
        # in the original CST file 
        solver = eigenmode_cst(path, modes = 10, angles=DRFangle)
        
        # the function get_wakefield_results exports the user defined 'post processing' results 
        # from CST into python and plots them automatically
        eigenmode_results = get_eigenmode_results(path, 'TotalQ_Eigenmode_All', 'Frequency (Multiple Modes)', 'Shunt Impedance (Perturbation) (Multiple Modes)')
        
        # Returns the longitudinal impedance based on the equivalent LRC resonator circuit formula
        resonant_impedance(eigenmode_results[1], eigenmode_results[3], eigenmode_results[5], 10, 10^10, 1001)
        
        #arbitrary
        Results_Eigenmode.append(post)  
        end = time.time()
        print('Calculation time for Simulation Number: ' + str(simulation_counter))
        print((end - start) / 60)

     except:
        print('Something went wrong for simulation' + str(simulation_counter))
        pass

end = time.time()

print('Total calculation time')
print(str((end-start)/3600) + ' hours')
