import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from glob import glob

params_file = "gary_decker_params.txt"
expt_params = np.loadtxt(params_file)
num_params = expt_params.shape[1]

best_fit_params_files = glob("gary_decker_expt_*_best_fit_params.txt")
expts = [int(x.split("_")[3]) for x in best_fit_params_files]
sorted_inds = np.argsort(expts)
best_fit_params_files = best_fit_params_files[sorted_inds]
expts = expts[sorted_inds]
num_expts = len(expts)
print expts
print best_fit_params_files

best_fit_params = np.zeros((num_expts, num_params))
for i in xrange(num_expts):
    best_fit_params[i, :] = np.loadtxt(best_fit_params_files[i])
print best_fit_params
