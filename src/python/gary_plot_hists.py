import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from glob import glob

params_file = "gary_decker_params.txt"
num_params = params_file.shape[1]
expt_params = np.loadtxt(params_file)

best_fit_params_files = sorted(glob("gary_decker_expt_*_best_fit_params.txt"))
print best_fit_params_files
expts = [int(x.split("_")[3]) for x in best_fit_params_files]
num_expts = len(expts)
print expts

best_fit_params = np.zeros((num_expts, num_params))
for i in xrange(num_expts):
    best_fit_params[i, :] = np.loadtxt(best_fit_params_files[expts[i]])
print best_fit_params
