import numpy as np
import numpy.random as npr
import mcmc_setup as ms

params_file = "gary_decker_params.txt"

seed = 1
npr.seed(seed)

model_number = 8  # Decker dog
original_gs, g_parameters = ms.get_original_params(model_number)
original_gs = np.array(original_gs)
print original_gs, "\n"

mu = 1.1*original_gs
Sigma = np.diag((0.15*original_gs)**2)
num_expts = 120

expt_params = npr.multivariate_normal(mu, Sigma, num_expts)

expt_params[np.where(expt_params<0)] = 0.

np.savetxt(params_file, expt_params)
