import ap_simulator as ap
import mcmc_setup as ms
import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
import time
import sys

model = sys.argv[1]
protocol = 1
c_seed = 1
noise_sd = 0.25

original_gs, g_parameters = ms.get_original_params(model) # list, list

chain_file, figs_dir = ms.synthetic_nonhierarchical_chain_file_and_figs_dir(model,protocol,c_seed)
with open(chain_file,"w") as outfile:
    outfile.write("# Synthetic nonhierarchical MCMC\n")
    outfile.write("# Model {}, protocol {}, c_seed {}\n".format(model,protocol,c_seed))
    outfile.write("# noise_sd {}\n".format(noise_sd))


python_seed = c_seed+1
npr.seed(python_seed)

def normal_loglikelihood_uniform_priors(test_trace,expt_trace,sigma):
    num_pts = len(test_trace)
    sum_of_square_diffs = np.sum((test_trace-expt_trace)**2)
    return -num_pts*np.log(sigma)-sum_of_square_diffs/(2.*sigma**2)
    


chain_file, figs_dir = ms.synthetic_nonhierarchical_chain_file_and_figs_dir(model,protocol,c_seed)

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
mean_estimate = np.copy(theta_cur)
test_trace = cell.SolveForVoltageTraceWithParams(original_gs)
log_target_cur = normal_loglikelihood_uniform_priors(test_trace,expt_trace,sigma_cur)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlabel('Time (ms)')
ax.set_ylabel('Membrane voltage (mV)')
ax.plot(expt_times,expt_trace,color='red',label='Synthetic expt')
ax.plot(expt_times,test_trace,color='blue',label='Initial')
ax.legend()
fig.tight_layout()
fig.savefig(figs_dir+'initial_and_expt_traces.png')
plt.close()
print "log_target_cur:", log_target_cur

num_params = len(theta_cur)

first_iteration = np.concatenate((theta_cur,[log_target_cur]))


loga = 0.
initial_proposal_scale = 0.01
cov_estimate = initial_proposal_scale*np.diag(theta_cur**2)


acceptance = 0.
acceptance_target = 0.25
when_to_adapt = 100*num_params

num_total_iterations = 200000
thinning = 5
assert(num_total_iterations%thinning==0)

num_saved_iterations = num_total_iterations/thinning
how_many_updates = 20

when_to_update = num_total_iterations / how_many_updates

fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlabel('Time (ms)')
ax.set_ylabel('Membrane voltage (mV)')
ax.set_title('All (post-burn, thinned) MCMC sample traces')

burn = num_saved_iterations/4
mcmc = np.zeros((num_saved_iterations+1,num_params+1))
mcmc[0,:] = first_iteration
start = time.time()
for it in xrange(1,num_total_iterations+1):
    accepted = 0.
    theta_star = npr.multivariate_normal(theta_cur,np.exp(loga)*cov_estimate)
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
        temp_covariance_bit = np.array([theta_cur-mean_estimate])
        cov_estimate = (1-gamma_s) * cov_estimate + gamma_s * temp_covariance_bit.T.dot(temp_covariance_bit)
        mean_estimate = (1-gamma_s) * mean_estimate + gamma_s * theta_cur
        loga += gamma_s*(accepted-acceptance_target)
    acceptance = ((it-1.)*acceptance + accepted)/it
    if (it%when_to_update==0):
        time_taken_so_far = time.time()-start
        estimated_time_left = time_taken_so_far/it*(num_total_iterations-it)
        print it/when_to_update, "/", how_many_updates
        print "Time taken: {} s = {} min".format(round(time_taken_so_far,1),round(time_taken_so_far/60.,2))
        print "acceptance:", acceptance
        print "loga:", loga
        print "Estimated time remaining: {} s = {} min".format(round(estimated_time_left,1),round(estimated_time_left/60.,2))
time_taken = time.time()-start
print "Time taken: {} s".format(round(time_taken,2))

ax.plot(expt_times,expt_trace,color='red',label='Synthetic expt')
ax.legend()
fig.tight_layout()
fig.savefig(figs_dir+'mcmc_sample_traces.png')
plt.close()
    
with open(chain_file,"a") as outfile:
    np.savetxt(outfile,mcmc)
    


for i in xrange(num_params):
    if (i<num_params-1):
        original_value = original_gs[i]
        label = g_parameters[i]
    elif (i==num_params-1):
        original_value = noise_sd
        label = r"\sigma"
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid()
    ax.hist(mcmc[burn:,i],normed=True,bins=40,color='blue',edgecolor='blue')
    ax.axvline(original_value,color='red',lw=2)
    ax.set_ylabel('Probability density')
    ax.set_xlabel('$'+label+'$')
    fig.tight_layout()
    fig.savefig(figs_dir+label.translate(None,r'\\{}')+'_marginal.png') # need double slashes to get rid of the sigma slash for some reason
    plt.close()




