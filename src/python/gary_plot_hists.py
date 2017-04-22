import numpy as np
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mcmc_setup as ms
from glob import glob

model_number = 8
original_gs, g_parameters = ms.get_original_params(model_number)

params_file = "gary_decker_params.txt"
expt_params = np.loadtxt(params_file)
num_params = expt_params.shape[1]

best_fit_params_files = np.array(glob("gary_decker_expt_*_best_fit_params.txt"))
expts = np.array([int(x.split("_")[3]) for x in best_fit_params_files])
sorted_inds = np.argsort(expts)
best_fit_params_files = best_fit_params_files[sorted_inds]
expts = expts[sorted_inds]
num_expts = len(expts)

fit_expt_params = expt_params[sorted_inds,:]

best_fit_params = np.zeros((num_expts, num_params))
for i in xrange(num_expts):
    best_fit_params[i, :] = np.loadtxt(best_fit_params_files[i])
print best_fit_params

for p in xrange(num_params):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.hist(fit_expt_params[:, p], normed=True, bins=10, color='blue', edgecolor=None, alpha=0.5, label="Expt")
    ax1.hist(best_fit_params[:, p], normed=True, bins=10, color='red', edgecolor=None, alpha=0.5, label="Best fit")
    ax1.legend()
    ax1.set_xlabel(g_parameters[i])
    ax1.set_ylabel("Normalised histogram")
    fig.tight_layout()
plt.show()
