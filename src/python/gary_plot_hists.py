import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from glob import glob

params_file = "gary_decker_params.txt"
expt_params = np.loadtxt(params_file)

best_fit_params = glob("gary_decker_expt_*_best_fit_params.txt")
print best_fit_params
