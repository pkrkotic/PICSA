#################################################

# PICSA Version 0.1
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

total_start = time.time()

angles = [11, 43.2]

# 62238, 2644200, 12076550, 29141520, 52098224

for DRFangle in angles:
    print('Currently running:' + str(DRFangle) + 'Degrees')
    simulation_counter = 0
    ########
    #Longitudinal 63
    ########
    try:
        path = 'C:/Users/pakrkoti/cernbox/Documents/DRF/Simulations/CST/Impedance_DRF/DRF_150_Longitudinal.cst'
        pathsplitter(path)
        Results_Longi = []
        start = time.time()
        simulation_counter = simulation_counter + 1
        print('Current Simulation Number: ' + str(simulation_counter))
        solver = wakefield_cst(path, xDip=0, yDip=0, xInt=0, yInt=0, angle=DRFangle, cpw=120, wakelength=50000)
        [XImpedance_Longi, YImpedance_Longi, ZImpedance_Longi] = get_wakefield_results(path)
        # plot_wakefield_results(XImpedance_Longi, YImpedance_Longi, ZImpedance_Longi)
        longitudinalresults = longitudinal_impedance(ZImpedance_Longi, 2.5, 11245)
        Results_Longi.append(longitudinalresults)
        end = time.time()
        print('Calculation time for Simulation Number: ' + str(simulation_counter))
        print((end - start) / 60)
    except:
        print('Something went wrong for simulation' + str(simulation_counter))
        pass


    time.sleep(120)

    #######
    #Transverse 63
    #######
    # try:
    #    path = 'C:/Users/pakrkoti/cernbox/Documents/DRF/Simulations/CST/Impedance_DRF/DRF_150_Trans1.cst'
    #    pathsplitter(path)
    #    Results_Trans1 = []
    #
    #    start = time.time()
    #    simulation_counter = simulation_counter + 1
    #    print('Current Simulation Number: ' + str(simulation_counter))
    #    solver = wakefield_cst(path, xDip=5, yDip=0, xInt=-5, yInt=0, angle=DRFangle, cpw=175)
    #    [XImpedance_Trans1, YImpedance_Trans1, ZImpedance_Trans1] = get_wakefield_results(path)
    #   #      plot_wakefield_results(XImpedance_Trans1, YImpedance_Trans1, ZImpedance_Trans1)
    #    transverse_results_Trans1 = transverse_impedance(XImpedance_Trans1, 2.5, 5, XImpedance_Longi, 1, 1)
    #    Results_Trans1.append(transverse_results_Trans1)
    #    end = time.time()
    #    print('Calculation time for Simulation Number: ' + str(simulation_counter))
    #    print((end - start) / 60)
    # except:
    #    print('Something went wrong for simulation' + str(simulation_counter))
    #    pass
    #
    # time.sleep(120)

    try:
       path = 'C:/Users/pakrkoti/cernbox/Documents/DRF/Simulations/CST/Impedance_DRF/DRF_150_Trans2.cst'
       pathsplitter(path)
       Results_Trans2 = []

       start = time.time()
       simulation_counter = simulation_counter + 1
       print('Current Simulation Number: ' + str(simulation_counter))
       solver = wakefield_cst(path, xDip=0, yDip=10, xInt=0, yInt=-10, angle=DRFangle, cpw=120, wakelength=50000)
       [XImpedance_Trans2, YImpedance_Trans2, ZImpedance_Trans2] = get_wakefield_results(path)
       # plot_wakefield_results(XImpedance_Trans2, YImpedance_Trans2, ZImpedance_Trans2)
       transverse_results_Trans2 = transverse_impedance(YImpedance_Trans2, 2.5, 10, YImpedance_Longi, 1, 1)
       Results_Trans2.append(transverse_results_Trans2)
       end = time.time()
       print('Calculation time for Simulation Number: ' + str(simulation_counter))
       print((end - start) / 60)
       print(Results_Trans2)


    except:
       print('Something went wrong for simulation' + str(simulation_counter))
       pass

    time.sleep(120)

    # try:
    #    path = 'C:/Users/pakrkoti/cernbox/Documents/DRF/Simulations/CST/Impedance_DRF/DRF_150_Trans3.cst'
    #    pathsplitter(path)
    #    Results_Trans3 = []
    #
    #    start = time.time()
    #    simulation_counter = simulation_counter + 1
    #    print('Current Simulation Number: ' + str(simulation_counter))
    #    solver = wakefield_cst(path, xDip=0, yDip=-5, xInt=0, yInt=5, angle=DRFangle, cpw=175)
    #    [XImpedance_Trans3, YImpedance_Trans3, ZImpedance_Trans3] = get_wakefield_results(path)
    #    # plot_wakefield_results(XImpedance_Trans3, YImpedance_Trans3, ZImpedance_Trans3)
    #    transverse_results_Trans3 = transverse_impedance(YImpedance_Trans3, 2.5, -5, XImpedance_Longi, 1, 1)
    #    Results_Trans3.append(transverse_results_Trans3)
    #    end = time.time()
    #    print('Calculation time for Simulation Number: ' + str(simulation_counter))
    #    print((end - start) / 60)
    #    print(Results_Trans3)
    #
    # except:
    #    print('Something went wrong for simulation' + str(simulation_counter))
    #    pass
    #
    # time.sleep(120)

    # try:
    #    path = 'C:/Users/pakrkoti/cernbox/Documents/DRF/Simulations/CST/Impedance_DRF/DRF_150_Trans4.cst'
    #    pathsplitter(path)
    #    Results_Trans4 = []
    #
    #    start = time.time()
    #    simulation_counter = simulation_counter + 1
    #    print('Current Simulation Number: ' + str(simulation_counter))
    #    solver = wakefield_cst(path, xDip=0, yDip=0, xInt=5, yInt=0, angle=DRFangle, cpw=175)
    #    [XImpedance_Trans4, YImpedance_Trans4, ZImpedance_Trans4] = get_wakefield_results(path)
    #    # plot_wakefield_results(XImpedance_Trans4, YImpedance_Trans4, ZImpedance_Trans4)
    #    transverse_results_Trans4 = transverse_impedance(XImpedance_Trans4, 2.5, 5, XImpedance_Longi, 1, 1)
    #    Results_Trans4.append(transverse_results_Trans4)
    #    end = time.time()
    #    print('Calculation time for Simulation Number: ' + str(simulation_counter))
    #    print((end - start) / 60)
    #    print(Results_Trans4)
    #
    # except:
    #    print('Something went wrong for simulation' + str(simulation_counter))
    #    pass
    #
    # time.sleep(120)

    try:
        path = 'C:/Users/pakrkoti/cernbox/Documents/DRF/Simulations/CST/Impedance_DRF/DRF_150_Trans5.cst'
        pathsplitter(path)
        Results_Trans5 = []

        start = time.time()
        simulation_counter = simulation_counter + 1
        print('Current Simulation Number: ' + str(simulation_counter))
        solver = wakefield_cst(path, xDip=0, yDip=0, xInt=0, yInt=10, angle=DRFangle, cpw=120, wakelength=50000)
        [XImpedance_Trans5, YImpedance_Trans5, ZImpedance_Trans5] = get_wakefield_results(path)
        # plot_wakefield_results(XImpedance_Trans5, YImpedance_Trans5, ZImpedance_Trans5)
        transverse_results_Trans5 = transverse_impedance(YImpedance_Trans5, 2.5, 10, YImpedance_Longi, 1, 1)
        Results_Trans5.append(transverse_results_Trans5)
        end = time.time()
        print('Calculation time for Simulation Number: ' + str(simulation_counter))
        print((end - start) / 60)
        print(Results_Trans5)

    except:
        print('Something went wrong for simulation' + str(simulation_counter))
        pass

    time.sleep(120)

    # try:
    #     path = 'C:/Users/pakrkoti/cernbox/Documents/DRF/Simulations/CST/Impedance_DRF/DRF_150_Trans6.cst'
    #     pathsplitter(path)
    #     Results_Trans6 = []
    #
    #     start = time.time()
    #     simulation_counter = simulation_counter + 1
    #     print('Current Simulation Number: ' + str(simulation_counter))
    #     solver = wakefield_cst(path, xDip=0, yDip=0, xInt=0, yInt=-5, angle=DRFangle, cpw=175)
    #     [XImpedance_Trans6, YImpedance_Trans6, ZImpedance_Trans6] = get_wakefield_results(path)
    #     plot_wakefield_results(XImpedance_Trans6, YImpedance_Trans6, ZImpedance_Trans6)
    #     transverse_results_Trans6 = transverse_impedance(YImpedance_Trans6, 2.5, -5, XImpedance_Trans6, 1, 1)
    #     Results_Trans6.append(transverse_results_Trans6)
    #     end = time.time()
    #     print('Calculation time for Simulation Number: ' + str(simulation_counter))
    #     print((end - start) / 60)
    #     print(Results_Trans6)
    #
    # except:
    #     print('Something went wrong for simulation' + str(simulation_counter))
    #     pass

end = time.time()

print('Total calculation time')
print(str((end-start)/3600) + ' hours')