#################################################

# PICSA Version 0.1
# By Patrick Krkotic

#################################################

######### Libraries

# Python
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize, stats
from matplotlib.pyplot import plot, draw, show
import colorama
from colorama import Fore, Style
import dictionary as dict
import os.path
import shutil
import csv


#Include the path for your computer where CST is installed
sys.path.append(r"C:/Program Files (x86)/CST Studio Suite 2020/AMD64/python_cst_libraries")

#CST
import cst
import cst.interface
from cst.interface import Project
import cst.results



############ Open CST file, change parameters and run the Wakefield Solver

def wakefield_cst(path,**kwargs):
    parameter_preamble = 'Sub Main () '
    parameters = []
    parameter_appendix = '\nRebuildOnParametricChange (bfullRebuild, bShowErrorMsgBox)\nEnd Sub'
    para = list(kwargs.keys())
    tara = list(kwargs.values())
    parameters.append(parameter_preamble)
    for todo in np.arange(len(kwargs)):
        parameters.append('\nStoreParameter("' + str(para[todo]) + '", ' + str(tara[todo]) + ')')
    parameters.append(parameter_appendix)
    parameter_changes = ''.join(parameters)
    the_cst = cst.interface.DesignEnvironment()
    cst_opener = cst.interface.DesignEnvironment.open_project(the_cst, str(path))
    print(Fore.BLUE + 'Project opened' + Style.RESET_ALL)
    cst.interface.DesignEnvironment.in_quiet_mode = True
    cst_opener.schematic.execute_vba_code(parameter_changes, timeout=None)
    print('Solver started')
    runscript = cst_opener.modeler.run_solver()
    protocol_path = CST_protocols(path)
    print('Solver finished and closing CST')
    cst.interface.DesignEnvironment.close(the_cst)
    os.remove(protocol_path + 'Model.log')
    os.remove(protocol_path + 'output.txt')
    return runscript




############ Extract CST Results

def get_wakefield_results(path):

    project = cst.results.ProjectFile(path)

    Ximpedance_cst = project.get_3d().get_result_item(r'1D Results\Particle Beams\ParticleBeam1\Wake impedance\X')
    Yimpedance_cst = project.get_3d().get_result_item(r'1D Results\Particle Beams\ParticleBeam1\Wake impedance\Y')
    Zimpedance_cst = project.get_3d().get_result_item(r'1D Results\Particle Beams\ParticleBeam1\Wake impedance\Z')

    frequency = np.array(Zimpedance_cst.get_xdata())
    XImpedance = np.array(Ximpedance_cst.get_ydata())
    YImpedance = np.array(Yimpedance_cst.get_ydata())
    ZImpedance = np.array(Zimpedance_cst.get_ydata())

    foldername = pathsplitter(path)

    rows = zip(frequency, np.real(XImpedance), np.imag(XImpedance), np.real(YImpedance), np.imag(YImpedance), np.real(ZImpedance), np.imag(ZImpedance))

    if not os.path.exists(foldername + '/' + str(path.split('.')[1]) + '_Wake_Results_CST.csv'):
        with open(foldername + '/' + str(path.split('.')[1]) + '_Wake_Results_CST.csv', "w") as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)

        print(Fore.BLUE + 'The CST impedance data has been stored under the name: Wake_Results_CST.csv' + Style.RESET_ALL)
    else:
        counter = 1
        while os.path.exists(foldername + '/' + str(path.split('.')[1]) + '_Wake_Results_CST.csv'):
            if not os.path.exists(foldername + '/' + str(path.split('.')[1]) + '_Wake_Results_CST_' + str(counter) + '.csv'):
                with open(foldername + '/' + str(path.split('.')[1]) + '_Wake_Results_CST_' + str(counter) + '.csv', "w") as f:
                    writer = csv.writer(f)
                    for row in rows:
                        writer.writerow(row)
                print(Fore.BLUE + 'The CST impedance data has been stored under the name: Wake_Results_CST' + str(
                    counter) + '.csv' + Style.RESET_ALL)
                break
            else:
                counter = counter + 1

    return Ximpedance_cst, Yimpedance_cst, Zimpedance_cst





############################### Plot the extracted CST Data

def plot_wakefield_results(Ximpedance_cst,Yimpedance_cst,Zimpedance_cst):

    frequency = np.array(Zimpedance_cst.get_xdata())
    XImpedance = np.array(Ximpedance_cst.get_ydata())
    YImpedance = np.array(Yimpedance_cst.get_ydata())
    ZImpedance = np.array(Zimpedance_cst.get_ydata())

    font = {'weight': 'bold',
            'size': 13}

    plt.rc('font', **font)

    fig, ax = plt.subplots()
    ax.plot(frequency, np.abs(XImpedance), label='X-component', linewidth=3.0)
    ax.plot(frequency, np.abs(YImpedance), label='Y-component', linewidth=3.0)
    ax.plot(frequency, np.abs(ZImpedance), label='Z-component', linewidth=3.0)
    ax.set_xlabel(r'Frequency [GHz]', fontsize=15, fontweight='bold')
    ax.set_ylabel(r'Z[$\Omega$]', fontsize=15, fontweight='bold')
    ax.set_title('Absolute Impedance', fontsize=10, fontweight='bold')
    ax.grid(alpha=0.8)
    ax.legend(fontsize=12)
    # change all spines
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(3)
    ax.tick_params(width=3)
    plt.xlim([0, max(frequency)])
    plt.draw()
    if not os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Results_CST_Absolute.png'):
        plt.savefig(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Results_CST_Absolute.png')
        print(Fore.BLUE + 'The CST impedance data plot has been stored under the name: Results_CST_Absolute' + Style.RESET_ALL)
    else:
        counter = 1
        while os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Results_CST_Absolute.png'):
            if not os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Results_CST_Absolute_' + str(counter) + '.png'):
                plt.savefig(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Results_CST_Absolute_' + str(counter) + '.png')
                print(Fore.BLUE + 'The CST impedance data plot has been stored under the name: Results_CST_Absolute' + str(
                    counter) + Style.RESET_ALL)
                break
            else:
                counter = counter + 1
    plt.show()





    fig2, ax2 = plt.subplots()
    ax2.plot(frequency, np.real(XImpedance), label='X-component', linewidth=3.0)
    ax2.plot(frequency, np.real(YImpedance), label='Y-component', linewidth=3.0)
    ax2.plot(frequency, np.real(ZImpedance), label='Z-component', linewidth=3.0)
    ax2.set_xlabel(r'Frequency [GHz]', fontsize=15, fontweight='bold')
    ax2.set_ylabel(r'Z[$\Omega$]', fontsize=15, fontweight='bold')
    ax2.set_title('Real Impedance', fontsize=10, fontweight='bold')
    ax2.grid(alpha=0.8)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax2.spines[axis].set_linewidth(3)
    ax2.tick_params(width=3)
    ax2.legend(fontsize=12)
    plt.xlim([0, max(frequency)])
    plt.draw()
    if not os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Results_CST_Real.png'):
        plt.savefig(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Results_CST_Real.png')
        print(Fore.BLUE + 'The CST impedance data plot has been stored under the name: Results_CST_Real' + Style.RESET_ALL)
    else:
        counter = 1
        while os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Results_CST_Real.png'):
            if not os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Results_CST_Real_' + str(counter) + '.png'):
                plt.savefig(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Results_CST_Real_' + str(counter) + '.png')
                print(Fore.BLUE + 'The CST impedance data plot has been stored under the name: Results_CST_Real_' + str(
                    counter) + Style.RESET_ALL)
                break
            else:
                counter = counter + 1

    plt.show()



    fig3, ax3 = plt.subplots()
    ax3.plot(frequency, np.imag(XImpedance), label='X-component', linewidth=3.0)
    ax3.plot(frequency, np.imag(YImpedance), label='Y-component', linewidth=3.0)
    ax3.plot(frequency, np.imag(ZImpedance), label='Z-component', linewidth=3.0)
    ax3.set_xlabel(r'Frequency [GHz]', fontsize=15, fontweight='bold')
    ax3.set_ylabel(r'Z[$\Omega$]', fontsize=15, fontweight='bold')
    ax3.set_title('Imaginary Impedance', fontsize=10, fontweight='bold')
    ax3.grid(alpha=0.8)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax3.spines[axis].set_linewidth(3)
    ax3.tick_params(width=3)
    ax3.legend(fontsize=12)
    plt.xlim([0, max(frequency)])
    plt.draw()
    if not os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Results_CST_Imaginary.png'):
        plt.savefig(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Results_CST_Imaginary.png')
        print(Fore.BLUE + 'The CST impedance data plot has been stored under the name: Results_CST_Imaginary'+ Style.RESET_ALL)
    else:
        counter = 1
        while os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Results_CST_Imaginary.png'):
            if not os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Results_CST_Imaginary_' + str(counter) + '.png'):
                plt.savefig(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Results_CST_Imaginary_' + str(counter) + '.png')
                print(Fore.BLUE + 'The CST impedance data plot has been stored under the name: Results_CST_Imaginary' + str(
                    counter) + Style.RESET_ALL)
                break
            else:
                counter = counter + 1

    plt.show()

    return True






############ Fitting Functions

def linear_func(x, m, b):
    return m * x + b

def func_trans(x, m, b):
    return m * x + b







############ Longitudinal impedance

def longitudinal_impedance(Impedance_cst, frequency_limit, revolution_frequency):
    freq = frequency_limit
    frequency = np.array(Impedance_cst.get_xdata())
    Impedance = np.array(Impedance_cst.get_ydata())

    iteration = True
    number_of_iterations = 0
    while iteration:
        fit_frequency = frequency[frequency < frequency_limit]
        fit_impedance = Impedance[frequency < frequency_limit]

        pars_imag, pars_covariance_imag = optimize.curve_fit(linear_func, fit_frequency, np.imag(fit_impedance))
        oneSigmaVariance_imag = np.sqrt(np.diag(pars_covariance_imag))

        if abs(pars_imag[1]) < 0.01:
            iteration = False
        else:
            frequency_limit = frequency_limit - 0.1
            fit_frequency = frequency[frequency < frequency_limit]
            fit_impedance = Impedance[frequency < frequency_limit]
            number_of_iterations = number_of_iterations + 1
            continue

    print(Fore.GREEN + 'Imaginary Part' + Style.RESET_ALL)
    print('Number of iterations for longitudinal linear fit: ' + str(number_of_iterations))
    print('Linear fit result: f(x)=' + str(pars_imag[0]) + '* x' + str(pars_imag[1]))
    print('One sigma error:' + str(pars_imag[0]) + '+-' + str(oneSigmaVariance_imag[0]) + str(pars_imag[1]) + '+-' + \
          str(oneSigmaVariance_imag[1]))
    print('Frequency limit cut:' + str(frequency_limit))

    Z_over_n = pars_imag[0] * revolution_frequency * 10 ** -9

    print(Style.BRIGHT + Fore.BLUE + 'The determined "Z/n" value is: ' + str(Z_over_n) + ' [\u03A9]' + Style.RESET_ALL)

    fig4, ax4 = plt.subplots()
    ax4.plot(fit_frequency[0:-1:10], np.imag(fit_impedance[0:-1:10]), 'o', label='Data')
    ax4.plot(fit_frequency, linear_func(fit_frequency, pars_imag[0], pars_imag[1]), '--r', label='Fit')
    ax4.text(0, max(np.imag(fit_impedance)) - 2,
             "y = ({:.3f} +/- {:.3f}) * x + ({:.3f} +/- {:.3f})".format(pars_imag[0], oneSigmaVariance_imag[0], pars_imag[1],
                                                                        oneSigmaVariance_imag[1]))
    ax4.set_xlabel(r'Frequency [GHz]', fontsize=15, fontweight='bold')
    ax4.set_ylabel(r'Z[$\Omega$]', fontsize=15, fontweight='bold')
    ax4.set_title('Imaginary Impedance', fontsize=10, fontweight='bold')
    ax4.grid(alpha=0.8)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax4.spines[axis].set_linewidth(3)
    ax4.tick_params(width=3)
    ax4.legend(fontsize=12)
    ax4.legend(loc='lower right')
    plt.xlim([0, max(fit_frequency)])
    plt.draw()
    if not os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_linear_fit_imag_Longitudinal.png'):
        plt.savefig(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_linear_fit_imag_Longitudinal.png')
        print(Fore.BLUE + 'The linear longitudinal fit plot has been stored under the name: linear_fit_imag_Longitudinal' + Style.RESET_ALL)
    else:
        counter = 1
        while os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_linear_fit_imag_Longitudinal.png'):
            if not os.path.exists(
                    dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_linear_fit_imag_Longitudinal_' + str(counter) + '.png'):
                plt.savefig(
                    dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_linear_fit_imag_Longitudinal_' + str(counter) + '.png')
                print(Fore.BLUE + 'The linear longitudinal fit plot has been stored under the name: linear_fit_imag_Longitudinal_' + str(counter) + Style.RESET_ALL)
                break
            else:
                counter = counter + 1

    plt.show()

    print(Fore.GREEN + 'Real Part' + Style.RESET_ALL)

    frequency_limit = freq
    frequency = np.array(Impedance_cst.get_xdata())
    Impedance = np.array(Impedance_cst.get_ydata())
    iteration = True
    number_of_iterations = 0

    while iteration:
        fit_frequency = frequency[frequency < frequency_limit]
        fit_impedance = Impedance[frequency < frequency_limit]

        pars_real, pars_covariance_real = optimize.curve_fit(linear_func, fit_frequency, np.real(fit_impedance))
        oneSigmaVariance_real = np.sqrt(np.diag(pars_covariance_real))

        if abs(pars_real[1]) < 0.01:
            iteration = False
        else:
            frequency_limit = frequency_limit - 0.1
            fit_frequency = frequency[frequency < frequency_limit]
            fit_impedance = Impedance[frequency < frequency_limit]
            number_of_iterations = number_of_iterations + 1
            continue

    print('Number of iterations for longitudinal linear fit: ' + str(number_of_iterations))
    print('Linear fit result: f(x)=' + str(pars_real[0]) + '* x' + str(pars_real[1]))
    print('One sigma error:' + str(pars_real[0]) + '+-' + str(oneSigmaVariance_real[0]) + str(pars_real[1]) + '+-' + \
          str(oneSigmaVariance_real[1]) )
    print('Frequency limit cut:' + str(frequency_limit))

    Z_over_n_real = pars_real[0] * revolution_frequency * 10 ** -9

    print(Style.BRIGHT + Fore.BLUE + 'The determined "Z/n" value is: ' + str(Z_over_n_real) + ' [\u03A9]' + Style.RESET_ALL)

    fig6, ax6 = plt.subplots()
    ax6.plot(fit_frequency[0:-1:10], np.real(fit_impedance[0:-1:10]), 'o', label='Data')
    ax6.plot(fit_frequency, linear_func(fit_frequency, pars_real[0], pars_real[1]), '--r', label='Fit')
    ax6.text(0, max(np.real(fit_impedance)) - 2,
             "y = ({:.3f} +/- {:.3f}) * x + ({:.3f} +/- {:.3f})".format(pars_real[0], oneSigmaVariance_real[0], pars_real[1],
                                                                        oneSigmaVariance_real[1]))
    ax6.set_xlabel(r'Frequency [GHz]', fontsize=15, fontweight='bold')
    ax6.set_ylabel(r'Z[$\Omega$]', fontsize=15, fontweight='bold')
    ax6.set_title('Real Impedance', fontsize=10, fontweight='bold')
    ax6.grid(alpha=0.8)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax6.spines[axis].set_linewidth(3)
    ax6.tick_params(width=3)
    ax6.legend(fontsize=12)
    ax6.legend(loc='lower right')
    plt.xlim([0, max(fit_frequency)])
    plt.draw()
    if not os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_linear_fit_real_Longitudinal.png'):
        plt.savefig(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_linear_fit_real_Longitudinal.png')
        print(Fore.BLUE + 'The linear longitudinal fit plot has been stored under the name: linear_fit_real_Longitudinal' + Style.RESET_ALL)
    else:
        counter = 1
        while os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_linear_fit_real_Longitudinal.png'):
            if not os.path.exists(
                    dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_linear_fit_real_Longitudinal_' + str(counter) + '.png'):
                plt.savefig(
                    dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_linear_fit_real_Longitudinal_' + str(counter) + '.png')
                print(Fore.BLUE + 'The linear longitudinal fit plot has been stored under the name: linear_fit_real_Longitudinal_' + str(counter) + Style.RESET_ALL)
                break
            else:
                counter = counter + 1

    plt.show()

    rows = [float(Z_over_n), float(pars_imag[0]), float(oneSigmaVariance_imag[0]), float(pars_imag[1]), float(oneSigmaVariance_imag[1]), float(Z_over_n_real), float(pars_real[0]), float(oneSigmaVariance_real[0]), float(pars_real[1]), float(oneSigmaVariance_real[1])]

    if not os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Longitudinal_Fit.dat'):
        np.savetxt(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Longitudinal_Fit.dat', rows , delimiter=',')
        print(Fore.BLUE + 'The fitted impedance data has been stored under the name: Longitudinal_Fit.dat' + Style.RESET_ALL)
    else:
        counter = 1
        while os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Longitudinal_Fit.dat'):
            if not os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Longitudinal_Fit_' + str(counter) + '.dat'):
                with open(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Longitudinal_Fit_' + str(counter) + '.dat', "w") as f:
                    np.savetxt(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Longitudinal_Fit_' + str(counter) + '.dat', rows , delimiter=',')
                print(Fore.BLUE + 'The fitted impedance data has been stored under the name: Longitudinal_Fit_' + str(
                    counter) + '.dat' + Style.RESET_ALL)
                break
            else:
                counter = counter + 1

    return Z_over_n, pars_imag, oneSigmaVariance_imag, Z_over_n_real, pars_real, oneSigmaVariance_real








############ Transverse impedance

def transverse_impedance(Impedance_cst, frequency_limit, displacement, Impedance_cst_centered, beta, beta_average):


    frequency = np.array(Impedance_cst.get_xdata())
    Impedance = np.array(Impedance_cst.get_ydata())
    impedance_centered = np.array(Impedance_cst_centered.get_ydata())


    fit_frequency_trans = frequency[frequency < frequency_limit]
    fit_impedance_trans = (-1) * Impedance[frequency < frequency_limit] / displacement * 10**3
    fit_impedance_trans2 = (-1) * ((Impedance[frequency < frequency_limit]) - impedance_centered[frequency < frequency_limit]) / displacement *10**3

    Z_over_beta_ave = np.average(np.imag(fit_impedance_trans)) * beta / beta_average
    Z_over_beta2_ave = np.average(np.imag(fit_impedance_trans2)) * beta / beta_average

    Z_over_beta_medi = np.median(np.imag(fit_impedance_trans)) * beta / beta_average
    Z_over_beta2_medi = np.median(np.imag(fit_impedance_trans2)) * beta / beta_average

    print(Style.BRIGHT + 'The determined "Z/\u03B2" value is: ' + str(Z_over_beta_ave) + ' [\u03A9]' + Style.RESET_ALL)
    print(Style.BRIGHT + 'The determined "Z/\u03B2" value is: ' + str(Z_over_beta2_ave) + ' [\u03A9]' + Style.RESET_ALL)
    print(Style.BRIGHT + 'The determined "Z/\u03B2" value is: ' + str(Z_over_beta_medi) + ' [\u03A9]' + Style.RESET_ALL)
    print(Style.BRIGHT + 'The determined "Z/\u03B2" value is: ' + str(Z_over_beta2_medi) + ' [\u03A9]' + Style.RESET_ALL)

    fig5, ax5 = plt.subplots()
    ax5.plot(fit_frequency_trans[0:-1:10], np.imag(fit_impedance_trans[0:-1:10]),'o',label='Data')
    ax5.plot(fit_frequency_trans, func_trans(fit_frequency_trans, 0, np.average(np.imag(fit_impedance_trans))), '--r',
             label='Fit')
    ax5.plot(fit_frequency_trans, func_trans(fit_frequency_trans, 0, np.median(np.imag(fit_impedance_trans))) ,'--b',label='Fit')
    ax5.plot(fit_frequency_trans, func_trans(fit_frequency_trans, 0, np.average(np.imag(fit_impedance_trans2))), '--g',
             label='Fit')
    plt.plot(fit_frequency_trans, func_trans(fit_frequency_trans, 0, np.median(np.imag(fit_impedance_trans2))), '--k',
             label='Fit')
    ax5.text(0, max(np.imag(fit_impedance_trans)) - 2,
             "median and average = ({:.3f} & {:.3f})".format(np.median(np.imag(fit_impedance_trans)), np.average(np.imag(fit_impedance_trans))) )
    ax5.text(0, max(np.imag(fit_impedance_trans)) - 2,
             "median and average = ({:.3f} & {:.3f})".format(np.median(np.imag(fit_impedance_trans2)),
                                                             np.average(np.imag(fit_impedance_trans2))))
    ax5.set_xlabel(r'Frequency [GHz]', fontsize=15, fontweight='bold')
    ax5.set_ylabel(r'Z[$\Omega$/m]', fontsize=15, fontweight='bold')
    ax5.set_title('Absolute Impedance', fontsize=10, fontweight='bold')
    ax5.grid(alpha=0.8)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax5.spines[axis].set_linewidth(3)
    ax5.tick_params(width=3)
    ax5.legend(fontsize=12)
    ax5.legend(loc='lower right')
    plt.xlim([0, max(fit_frequency_trans)])
    plt.draw()
    if not os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_linear_fit_Transverse.png'):
        plt.savefig(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_linear_fit_Transverse.png')
        print(
            Fore.BLUE + 'The linear transverse fit plot has been stored under the name: linear_fit_Transverse' + Style.RESET_ALL)

    else:
        counter = 1
        while os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_linear_fit_Transverse.png'):
            if not os.path.exists(
                    dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_linear_fit_Transverse_' + str(counter) + '.png'):
                plt.savefig(
                    dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_linear_fit_Transverse_' + str(counter) + '.png')
                print(Fore.BLUE + 'The linear longitudinal fit plot has been stored under the name: linear_fit_Longitudinal_' + str(counter) + Style.RESET_ALL)
                break
            else:
                counter = counter + 1

    plt.show()

    rows = [float(Z_over_beta_ave), float(Z_over_beta2_ave), float(Z_over_beta_medi), float(Z_over_beta2_medi)]

    if not os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Transverse_Fit.dat'):
        np.savetxt(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Transverse_Fit.dat', rows,
                   delimiter=',')
        print(
            Fore.BLUE + 'The fitted impedance data has been stored under the name: Transverse_Fit.dat' + Style.RESET_ALL)
    else:
        counter = 1
        while os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Transverse_Fit.dat'):
            if not os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Transverse_Fit_' + str(
                    counter) + '.dat'):
                with open(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Transverse_Fit_' + str(
                        counter) + '.dat', "w") as f:
                    np.savetxt(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_Transverse_Fit_' + str(
                        counter) + '.dat', rows, delimiter=',')
                print(Fore.BLUE + 'The fitted impedance data has been stored under the name: Transverse_Fit_' + str(
                    counter) + '.dat' + Style.RESET_ALL)
                break
            else:
                counter = counter + 1

    return Z_over_beta_ave, Z_over_beta2_ave, Z_over_beta_medi, Z_over_beta2_medi






############ Pathsplit

def pathsplitter(path):
    dict.filename = path.split('/')[-1]
    dict.foldername = '/'.join(path.split('/')[0:-1])
    print(Fore.GREEN + Style.BRIGHT + '\n' + 'Executing CST file: ' + dict.filename + Style.RESET_ALL)

    return dict.foldername






############ Extraction of CST protocolls and messages

def CST_protocols(path):
    protocol_path = path.split('.')[0] + '/Result/'
    solver_info = open(protocol_path + 'Model.log',"r")
    message_output = open(protocol_path + 'output.txt',"r")

    # print(Fore.LIGHTBLUE_EX + Style.BRIGHT + 'CST Message Output:' + Style.RESET_ALL)
    # print(message_output.read())
    # print(Fore.LIGHTBLUE_EX + Style.BRIGHT + 'CST Log Output:' + Style.RESET_ALL)
    # print(solver_info.read())

    if not os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_logfile.log'):
        shutil.copy(protocol_path + 'Model.log', dict.foldername + '/' + dict.filename.split('.')[0] + '_logfile.log')
        shutil.copy(protocol_path + 'output.txt', dict.foldername + '/' + dict.filename.split('.')[0] + '_messages.txt')
        print(Fore.BLUE + 'The CST log-data has been stored under the name: ' + str(dict.filename.split('.')[0]) + '_logfile.log' + Style.RESET_ALL)
        print(Fore.BLUE + 'The CST messages have been stored under the name: ' + str(dict.filename.split('.')[0]) + '_messages.txt' + Style.RESET_ALL)
    else:
        counter = 1
        while os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_logfile.log'):
            if not os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_' + str(counter) + '_logfile.log'):
                shutil.copy(protocol_path + 'Model.log', dict.foldername + '/' + dict.filename.split('.')[0] + '_' + str(counter) + '_logfile.log')
                shutil.copy(protocol_path + 'output.txt', dict.foldername + '/' + dict.filename.split('.')[0] + '_' +  str(counter) + '_messages.txt')
                print(Fore.BLUE + 'The CST log-data has been stored under the name: ' + str(dict.filename.split('.')[0]) + '_' +  str(counter) + '_logfile.log' + Style.RESET_ALL)
                print(Fore.BLUE + 'The CST messages have been stored under the name: ' + str(dict.filename.split('.')[0]) + '_' +  str(counter) + '_messages.txt' + Style.RESET_ALL)
                break
            else:
                counter = counter + 1

    return protocol_path



############ Open CST file, change parameters and run the Eigenmode Solver

def eigenmode_cst(path, **kwargs):

    parameter_preamble = 'Sub Main () '
    parameters = []
    parameter_appendix = '\nRebuildOnParametricChange (bfullRebuild, bShowErrorMsgBox)\nEnd Sub'

    para = list(kwargs.keys())
    tara = list(kwargs.values())
    parameters.append(parameter_preamble)

    for todo in np.arange(len(kwargs)):
        parameters.append('\nStoreParameter("' + str(para[todo]) + '", ' + str(tara[todo]) + ')')

    parameters.append(parameter_appendix)

    parameter_changes = ''.join(parameters)

    the_cst = cst.interface.DesignEnvironment()
    cst_opener = cst.interface.DesignEnvironment.open_project(the_cst, str(path))
    print(Fore.BLUE + 'Project opened' + Style.RESET_ALL)
    cst.interface.DesignEnvironment.in_quiet_mode = True
    cst_opener.schematic.execute_vba_code(parameter_changes, timeout=None)
    print('Solver started')
    runscript = cst_opener.modeler.run_solver()

    protocol_path = CST_protocols(path)

    print('Solver finished and closing CST')
    cst.interface.DesignEnvironment.close(the_cst)

    os.remove(protocol_path + 'Model.log')
    os.remove(protocol_path + 'output.txt')
    return runscript



############ export the eigenmode results of the pre-defined post-processing in CST

def get_eigenmode_results(path, *args):

    post_results = []

    project = cst.results.ProjectFile(path)

    for post in args:
        Q = project.get_3d().get_result_item(r'Tables' + '\\' + '1D Results' + '\\' + str(post))
        post_results.append(np.array(Q.get_xdata()))
        post_results.append(np.array(Q.get_ydata()))



    for plotter in np.arange(len(post_results) -1):

        if plotter % 2 == 0:

            fig7, ax7 = plt.subplots()
            ax7.plot(post_results[plotter], post_results[plotter+1], 's', label='Data', markersize = 7)
            ax7.set_xlabel(r'Mode Number', fontsize=10, fontweight='bold')
            ax7.set_ylabel(str(args[int(plotter/2)]), fontsize=10, fontweight='bold')
            ax7.set_title('Post-Processed Data CST', fontsize=10, fontweight='bold')
            ax7.grid(alpha=0.8)
            for axis in ['top', 'bottom', 'left', 'right']:
                ax7.spines[axis].set_linewidth(3)
            ax7.tick_params(width=3)
            ax7.legend(fontsize=12)
            ax7.legend(loc='lower right')
            # plt.xlim([0, max(fit_frequency_trans)])
            plt.draw()
            if not os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_' + str(args[int(plotter/2)]) + '.png'):
                plt.savefig(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_' +  str(args[int(plotter/2)]) +'.png')
                print(
                    Fore.BLUE + 'The plot has been stored under the name: '+ str(args[int(plotter/2)]) + Style.RESET_ALL)

            else:
                counter = 1
                while os.path.exists(dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_' + str(args[int(plotter/2)]) + '.png'):
                    if not os.path.exists(
                            dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_' + str(args[int(plotter/2)]) + str(counter) + '.png'):
                        plt.savefig(
                            dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_' + str(args[int(plotter/2)]) + str(counter) + '.png')
                        print(
                            Fore.BLUE + 'The plot has been stored under the name: ' + str(args[int(plotter/2)]) + str(
                                counter) + Style.RESET_ALL)
                        break
                    else:
                        counter = counter + 1

            plt.show()

    foldername = pathsplitter(path)

    post_results_array = np.array(post_results)
    transpose = post_results_array.T
    post_results_transposed = transpose.tolist()


    if not os.path.exists(foldername + '/' + str(path.split('.')[1]) + '_Eigenmode_Results_CST.csv'):
        with open(foldername + '/' + str(path.split('.')[1]) + '_Eigenmode_Results_CST.csv', "w") as f:
            writer = csv.writer(f)
            for row in post_results_transposed:
                writer.writerow(row)

        print(
            Fore.BLUE + 'The CST impedance data has been stored under the name: Eigenmode_Results_CST.csv' + Style.RESET_ALL)
    else:
        counter = 1
        while os.path.exists(foldername + '/' + str(path.split('.')[1]) + '_Eigenmode_Results_CST.csv'):
            if not os.path.exists(
                    foldername + '/' + str(path.split('.')[1]) + '_Eigenmode_Results_CST_' + str(counter) + '.csv'):
                with open(foldername + '/' + str(path.split('.')[1]) + '_Eigenmode_Results_CST_' + str(counter) + '.csv',
                          "w") as f:
                    writer = csv.writer(f)
                    for row in post_results_transposed:
                        writer.writerow(row)
                print(Fore.BLUE + 'The CST impedance data has been stored under the name: Eigenmode_Results_CST' + str(
                    counter) + '.csv' + Style.RESET_ALL)
                break
            else:
                counter = counter + 1

    return post_results



############ calculate longitudinal LRC impedance 

def resonant_impedance(qfactor, resonance, shunt, f_start, f_stop, f_points):

    frequency_range = np.logspace(f_start, f_stop, f_points)
    # res_impedance = [[0 for x in range(len(qfactor))] for x in range(len(frequency_range))]

    res_impedance =[]

    for freq in np.arange(len(frequency_range)):
        collector = []
        for runner in np.arange(len(qfactor)):
            collector.append((0.5* shunt[runner] / (1 + 1j * qfactor[runner] * ((frequency_range[freq]/resonance[runner]) - (resonance[runner]/frequency_range[freq])))))
        res_impedance.append(collector)


    sum_res_impedance = [sum(res_impedance[pk]) for pk in np.arange(len(res_impedance)) ]

    fig8, ax8 = plt.subplots()
    ax8.loglog(frequency_range, np.real(sum_res_impedance), '-d', markersize=7)
    ax8.loglog(frequency_range, np.imag(sum_res_impedance), '-o', markersize=7)
    ax8.set_xlabel(r'Frequency [Hz]', fontsize=10, fontweight='bold')
    ax8.set_ylabel(r'Resonant impedance [$\Omega$]', fontsize=10, fontweight='bold')
    # ax8.set_title('Post-Processed Data CST', fontsize=10, fontweight='bold')
    ax8.grid(alpha=0.8)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax8.spines[axis].set_linewidth(3)
    ax8.tick_params(width=3)
    # ax8.legend(fontsize=12)
    # ax8.legend(loc='lower right')
    # plt.xlim([0, max(fit_frequency_trans)])
    plt.draw()
    if not os.path.exists(
            dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_' + 'resonant_impedance.png'):
        plt.savefig(
            dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_' + 'resonant_impedance.png')
        print(
            Fore.BLUE + 'The plot has been stored under the name: resonant_impedance' + Style.RESET_ALL)

    else:
        counter = 1
        while os.path.exists(
                dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_' + 'resonant_impedance.png'):
            if not os.path.exists(
                    dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_resonant_impedance_' + str(
                        counter) + '.png'):
                plt.savefig(
                    dict.foldername + '/' + str(dict.filename.split('.')[0]) + '_resonant_impedance_' + str(
                        counter) + '.png')
                print(
                    Fore.BLUE + 'The plot has been stored under the name: ' + '_resonant_impedance_' + str(
                        counter) + Style.RESET_ALL)
                break
            else:
                counter = counter + 1

    plt.show()
    return sum_res_impedance
