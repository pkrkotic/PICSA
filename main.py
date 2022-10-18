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
#Include the path for your computer where CST is installed
sys.path.append(r"C:/Program Files (x86)/CST Studio Suite 2020/AMD64/python_cst_libraries")

# import the cst library
import cst

# test if cst file path is correct
print(cst.__file__)




#########################
############### Functions

##### Run CST file

#wakefield_cst(path, x_source. y_source, x_integration, y_integration)
    # returns boolean

#### Extract Results
# get_results(path)
    # returns Impedance as given by CST for all three coordinates

#########################

parent_dir = 'C:/Users/pakrkoti/cernbox/Documents/DRF/Simulations/CST/'

# path = 'C:/Users/pakrkoti/cernbox/Documents/DRF/Simulations/CST/PythonTests/2_ClosedDRF_TranPY.cst'
# path = 'C:/Users/pakrkoti/cernbox/Documents/DRF/Simulations/CST/PythonTests/2_ClosedDRF_TranPY_Eigen.cst'

pathsplitter(path)

solver = wakefield_cst(path, 0, 0, 0, 0)
# solver = eigenmode_cst(path,5,0,0)
[XLongi, YLongi, ZLongi] = get_results(path)
# plot_CST(XLongi, YLongi, ZLongi)
[Z_over_n, pars, oneSigmaVariance, Z_over_n_real, pars_real, oneSigmaVariance_real] = longitudinal_impedance(ZLongi, 3, 11245)

# solver = run_cst(path, 5, 0, -5, 0)
# [XTrans, YTrans, ZTrans] = get_results(path)
# plot_CST(XTrans, YTrans, ZTrans)
#[Z_over_beta_ave, Z_over_beta2_ave, Z_over_beta_medi, Z_over_beta2_medi] = transverse_impedance(XTrans, 2.5, 5, XLongi, 1, 1)
#
