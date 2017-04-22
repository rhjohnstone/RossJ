import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mcmc_setup as ms
from glob import glob
from scipy.stats import norm

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

num_pts = 201
for p in xrange(num_params):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.hist(fit_expt_params[:, p], normed=True, bins=10, color='blue', edgecolor=None, alpha=0.5, label="Expt", zorder=10)
    ax1.hist(best_fit_params[:, p], normed=True, bins=10, color='red', edgecolor=None, alpha=0.5, label="Best fit", zorder=11)
    ax1.axvline(original_gs[p],color='black')
    ax1.legend()
    ax1.set_xlabel(g_parameters[p])
    ax1.set_ylabel("Normalised histogram")
    x = ax1.get_xlim()
    pdf_x = np.linspace(x[0], x[1], num_pts)
    pdf_y = norm.pdf(pdf_x, loc=1.1*original_gs[p], scale=0.15*original_gs[p])
    ax1.plot(pdf_x, pdf_y, color='green', label="Expt generating")
    fig.tight_layout()
    fig.savefig("gary_decker_{}_hists.png".format(g_parameters[p]))
    plt.close()
    
    
