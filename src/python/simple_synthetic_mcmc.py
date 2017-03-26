# it only solves once, so it's not doing steady-state fitting

import ap_simulator
import mcmc_setup as ms
import numpy as np
import numpy.random as npr
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from time import time
import multiprocessing as mp
import itertools as it
import sys




python_seed = 1
npr.seed(python_seed)  # seed random number generator so we can reproduce results

def get_test_trace(params):
    return ap.SolveForVoltageTraceWithParams(params)

def log_target(params,expt_trace,num_pts,upper_bounds):
    if np.any(params < 0) or np.any(params > upper_bounds):
        return -np.inf
    else:
        temp_g_params = params[:-1]
        temp_sigma = params[-1]
        temp_test_trace = get_test_trace(temp_g_params)
        return -num_pts * np.log(temp_sigma) - np.sum((temp_test_trace-expt_trace)**2)/(2*temp_sigma**2)

"""
def CalculateMAPE(thetaStar, true_gs):
    length = len(thetaStar)
    MAPE = 0.
    for i in range(length):
        MAPE += abs(thetaStar[i]-true_gs[i]) / true_gs[i]
    MAPE /= length
    return MAPE
"""

# 1. Hodgkin Huxley
# 2. Beeler Reuter
# 3. Luo Rudy
# 4. ten Tusscher
# 5. O'Hara Rudy
# 6. Davies (canine)
# 7. Paci (SC-CM ventricular)

model = 1
protocol = 1

solve_start,solve_end,solve_timestep,stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time = ms.get_protocol_details(protocol)
original_gs, g_parameters = ms.get_original_params(model)

ap = ap_simulator.APSimulator()
ap.DefineSolveTimes(solve_start,solve_end,solve_timestep)
ap.DefineStimulus(stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time)
ap.DefineModel(model)

chain_file, figs_dir = ms.synthetic_nonhierarchical_chain_file_and_figs_dir(model,protocol,python_seed)

noise_sigma = 1.





num_pts = int((solve_end-solve_start)/solve_timestep)+1
expt_times = np.linspace(solve_start,solve_end,num_pts)
expt_trace = get_test_trace(original_gs)
expt_trace += noise_sigma*(npr.randn(num_pts))
#plt.plot(expt_trace)
#plt.show(block=True)



theta_cur = np.concatenate((original_gs,[noise_sigma]))
upper_bounds = np.copy(100*theta_cur)
log_target_cur = log_target(theta_cur,expt_trace,num_pts,upper_bounds)



num_params = len(theta_cur)

thinning = 10 # remove auto-correlation by thinning the samples, i.e. keep every 10th step, say

theta_star = np.zeros(num_params)

loga = 0.
acceptance = 0.

mean_estimate = np.copy(theta_cur)

cov_estimate = np.diag(10*theta_cur)


    
print "covariance matrix:\n", cov_estimate

with open(chain_file, 'w') as outfile:
        outfile.write('# Model '+str(model)+', protocol ' + str(protocol) + '\n')
        outfile.write('# Adaptive covariance matrix\n')
        outfile.write('# Thinned by taking saving only every ' + str(thinning) + '-th accepted state\n')
        outfile.write('# 1-'+str(num_params)+'. parameters, '+str(1+num_params)+'. log_target, '
                      +str(2+num_params)+'. acceptance rate\n')

how_many = 100000
num_saved = how_many / thinning + 1
burn = num_saved / 4


chain = np.zeros((num_saved,2+num_params))
chain[0,:] = np.concatenate((theta_cur,[log_target_cur, acceptance]))

when_to_adapt = 100*num_params

t=0
start = time()
while t<=how_many:
    if t%(500)==0 and t>0:
        print t/500, "/", how_many/500
        print "acceptance =", acceptance
        print "loga =", loga
        print "covariance of g_{Na}:", cov_estimate[0,0]
        print "Current log_target_cur:", log_target_cur
        print "Time taken:", time() - start, "sec"
        print "Proposed theta:", theta_star, "\n"
    # propose new parameter values by sampling from normal centred on current guess
    cov_matrix_for_proposal = np.exp(loga)*cov_estimate
    #if (1000*num_params + 1 < t < 2000*num_params):
        #cov_matrix_for_proposal *= 10
    theta_star = npr.multivariate_normal(theta_cur,cov_matrix_for_proposal)
        
    accepted = 0      
    log_target_star = log_target(theta_star,expt_trace,num_pts,upper_bounds)
    # accept/reject  	
    u = npr.rand()
    log_u = np.log(u)
    log_alpha = log_target_star - log_target_cur
    if log_u < log_alpha:
        accepted = 1
        theta_cur = np.copy(theta_star)
        log_target_cur = log_target_star
    
    # start to update covariance matrix
    if t > when_to_adapt:
        s = t - when_to_adapt
        gamma_s = 1/(s+1)**0.6
        temp_covariance_bit = np.array([theta_cur-mean_estimate])
        cov_estimate = (1-gamma_s) * cov_estimate + gamma_s * np.dot(np.transpose(temp_covariance_bit),temp_covariance_bit)
        mean_estimate = (1-gamma_s) * mean_estimate + gamma_s * theta_cur
        loga += gamma_s*(accepted-0.25)
    
    acceptance = (t*acceptance + accepted)/(t+1)
    
    if t%thinning==0 and t>0:
        chain[t/thinning,:] = np.concatenate((theta_cur,[log_target_cur, acceptance]))
    t=t+1
time_taken = time() - start
print "\nTotal time taken by MCMC:", time_taken, "s\n"

with open(chain_file,'a') as outfile:
    np.savetxt(outfile,chain)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(chain[burn:,0],bins=40)
plt.show(block=True)



