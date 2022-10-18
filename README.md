# PICSA
Python Induced CST Solver Automation V0.1

PICSA is a python based code capable of communicating with CST
and giving instructions to CST. The code can open and close
files, run simulations, change any pre-defined parameters in
the CST file and extract the results for post-processing. The
benefit lies within that simulations and job queues can be
defined in loops in the python code and executed without the
actual interaction with CST’s graphical user interface. The 
geometry and solver have to be pre-defined within the CST
file. Besides, it allows the user to overcome some of the CST
limitations, e.g., by defining own optimisation routines and
parametric studies based on the already post-processed data.
The functions for PICSA written (until now) -their inputs and
outputs- are summarised in the attached figure. The main idea 
is to upload the source code in GitHub for sharing and further 
collaborative development for automated processes, e.g. impedance
studies of accelerator components or antenna designs.


PICSA only works with python 3.6 due to the CST libraries. 
