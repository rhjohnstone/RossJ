import ap_simulator as ap
import mcmc_setup as ms
import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
import time

model = 4
protocol = 1
c_seed = 1
noise_sd = 0.25

python_seed = c_seed+1
npr.seed(python_seed)

def normal_loglikelihood_uniform_priors(test_trace,expt_trace,sigma):
    num_pts = len(test_trace)
    sum_of_square_diffs = np.sum((test_trace-expt_trace)**2)
    return -num_pts*np.log(sigma)-sum_of_square_diffs/(2.*sigma**2)
    
original_gs, g_parameters = ms.get_original_params(model) # list, list

chain_file, figs_dir = ms.nonhierarchical_chain_file_and_figs_dir(model,protocol,c_seed)

start_time = 0.
end_time = 400.
timestep = 0.2
expt_times = np.arange(start_time,end_time+timestep,timestep)
    
cell = ap.APSimulator()
cell.DefineProtocol(protocol)
cell.DefineModel(model)
expt_trace = cell.GenerateSyntheticExptTrace(original_gs,noise_sd,c_seed)

sigma_cur = 0.25
theta_cur = np.copy(original_gs+[sigma_cur])
test_trace = cell.SolveForVoltageTraceWithParams(original_gs)
log_target_cur = normal_loglikelihood_uniform_priors(test_trace,expt_trace,sigma_cur)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()
ax.plot(expt_times,expt_trace,color='red',label='Expt')
ax.plot(expt_times,test_trace,color='blue',label='Initial')
ax.legend()
print "log_target_cur:", log_target_cur
#plt.show(block=True)

num_params = len(theta_cur)

first_iteration = np.concatenate((theta_cur,[log_target_cur]))

loga = 0.
proposal_covariance = 0.01*np.diag(theta_cur**2)

acceptance = 0.
acceptance_target = 0.25
when_to_adapt = 100*num_params

num_total_iterations = 100000
thinning = 5
assert(num_total_iterations%thinning==0)

num_saved_iterations = num_total_iterations/thinning
how_many_updates = 20

when_to_update = num_total_iterations / how_many_updates

fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()

burn = num_saved_iterations/2
mcmc = np.zeros((num_saved_iterations+1,num_params+1))
mcmc[0,:] = first_iteration
start = time.time()
for it in xrange(1,num_total_iterations+1):
    accepted = 0.
    theta_star = npr.multivariate_normal(theta_cur,np.exp(loga)*proposal_covariance)
    if np.all(theta_star>0):
        test_trace = cell.SolveForVoltageTraceWithParams(theta_star[:-1])
        log_target_star = normal_loglikelihood_uniform_priors(test_trace,expt_trace,theta_star[-1])
        alpha = npr.rand()
        if ( np.log(alpha) < log_target_star-log_target_cur ):
            theta_cur = theta_star
            log_target_cur = log_target_star
            accepted = 1.
    if (it%thinning==0):
        mcmc[it/thinning,:] = np.concatenate((theta_cur,[log_target_cur]))
        if (it>=burn):
            ax.plot(expt_times,test_trace,alpha=0.01)
    if (it>when_to_adapt):
        s = it - when_to_adapt
        gamma_s = 1./(s+1.)**0.6
        loga += gamma_s*(accepted-acceptance_target)
    acceptance = ((it-1.)*acceptance + accepted)/it
    if (it%when_to_update==0):
        print it/when_to_update, "/", how_many_updates
        print "acceptance:", acceptance
        print "loga:", loga
time_taken = time.time()-start
print "Time taken: {} s".format(round(time_taken,2))    
    
print mcmc[:,-1]
    
ax.plot(expt_times,expt_trace,color='red')

for i in xrange(num_params):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid()
    ax.hist(mcmc[burn:,i],normed=True,bins=40)
    
plt.show(block=True)




