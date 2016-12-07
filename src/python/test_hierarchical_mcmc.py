import ap_simulator as ap
import mcmc_setup as ms
import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
import scipy.stats as st
import time
import sys

def new_eta(old_eta,samples): # for sampling from conjugate prior-ed N-IG
    assert(len(old_eta)==4)
    x_bar = np.mean(samples)
    num_samples = len(samples)
    mu, nu, alpha, beta = old_eta # they should already be floats, not ints
    new_mu = ((nu*mu + num_samples*x_bar) / (nu + num_samples))
    new_nu = nu + num_samples
    new_alpha = alpha + 0.5*num_samples
    new_beta = beta + 0.5*np.sum((samples-x_bar)**2) + 0.5*((num_samples*nu)/(nu+num_samples))*(x_bar-mu)**2
    return np.array([new_mu,new_nu,new_alpha,new_beta])
    
def sample_from_N_IG(eta):
    mu, nu, alpha, beta = eta
    sigma_squared = st.invgamma.rvs(alpha,scale=beta)
    sample = mu + np.sqrt(sigma_squared/nu)*npr.randn()
    return np.array([sample,sigma_squared])

def log_pi_theta_i(theta_i,theta,sigma_squareds,sigma,data_i,test_i):
    sum_1 = np.sum(((data_i-test_i)/sigma)**2)
    sum_2 = np.sum(((theta_i-theta)**2)/sigma_squareds)
    return -0.5 * (sum_1 + sum_2)

def log_pi_sigma(expt_datas,test_datas,sigma,N_e,num_pts,uniform_noise_prior):
    if (not (uniform_noise_prior[0] < sigma < uniform_noise_prior[1])):
        return -np.inf
    else:
        return -N_e*num_pts*np.log(sigma) - np.sum((expt_datas-test_datas)**2) / (2*sigma**2)

model = int(sys.argv[1])
protocol = 1
python_seed = 1
noise_sd = 0.25

num_expts = 5

npr.seed(python_seed)

original_gs, g_parameters = ms.get_original_params(model) # list, list

num_g_params = len(original_gs)

print "original_gs:", original_gs

expt_params_cov_matrix = 0.005*np.diag(np.array(original_gs)**2)

expt_params = npr.multivariate_normal(original_gs,expt_params_cov_matrix,num_expts)

# make sure no params are negative
where_params_negative = np.where(expt_params<0.)
expt_params[where_params_negative] = 0.

print expt_params

chain_file, figs_dir = ms.synthetic_hierarchical_chain_file_and_figs_dir(model,protocol,python_seed)
with open(chain_file,"w") as outfile:
    outfile.write("# Synthetic hierarchical MCMC\n")
    outfile.write("# Model {}, protocol {}, python_seed {}\n".format(model,protocol,python_seed))
    outfile.write("# noise_sd {}\n".format(noise_sd))


python_seed = python_seed+1
npr.seed(python_seed)

def normal_loglikelihood_uniform_priors(test_trace,expt_trace,sigma):
    num_pts = len(test_trace)
    sum_of_square_diffs = np.sum((test_trace-expt_trace)**2)
    return -num_pts*np.log(sigma)-sum_of_square_diffs/(2.*sigma**2)

chain_file, figs_dir = ms.synthetic_nonhierarchical_chain_file_and_figs_dir(model,protocol,python_seed)

# need to make sure these are always same as in C++ protocol
# might have to change it to have protocols hard-coded into Python instead of C++
start_time = 0.
end_time = 400.
timestep = 0.2
expt_times = np.arange(start_time,end_time+timestep,timestep)
num_pts = len(expt_times)
    
cell = ap.APSimulator()
cell.DefineProtocol(protocol)
cell.DefineModel(model)

expt_traces = []
fig = plt.figure()
ax = fig.add_subplot(111)
for i in xrange(num_expts):
    temp_trace = cell.SolveForVoltageTraceWithParams(expt_params[i,:])
    temp_trace += noise_sd*npr.randn(len(temp_trace))
    expt_traces.append(temp_trace)
    ax.plot(expt_times,temp_trace)
print expt_traces
plt.show(block=True)

initial_theta_curs = np.copy(expt_params)

starting_mean = np.mean(initial_theta_curs,axis=0)
starting_var = np.var(initial_theta_curs,axis=0)

old_eta_js = np.zeros((num_g_params,4),dtype=float)
old_eta_js[:,0] = starting_mean
old_eta_js[:,1] = 1. * num_expts
old_eta_js[:,2] = 0.5 * num_expts
old_eta_js[:,3] = 0.5 * num_expts * starting_var

print old_eta_js

top_theta_cur = np.copy(starting_mean)
top_sigma_squareds_cur = np.copy(starting_var)
theta_is_cur = np.copy(initial_theta_curs)
noise_sigma_cur = noise_sd

# set negative param values to 0
top_theta_cur[np.where(top_theta_cur<0)] = 0.
top_sigma_squareds_cur[np.where(top_sigma_squareds_cur<0)] = 0.
theta_is_cur[np.where(theta_is_cur<0)] = 0.

first_iteration = np.concatenate((top_theta_cur,top_sigma_squareds_cur,theta_is_cur.flatten(),[noise_sigma_cur])) # not including likelihoods
num_all_params = len(first_iteration)


temp_test_traces = [cell.SolveForVoltageTraceWithParams(params) for params in theta_is_cur]

print temp_test_traces

proposal_scale = 0.001

covariances = [proposal_scale*np.eye(num_g_params)*original_gs for i in xrange(num_expts)]

print covariances

sys.exit()

logas = [0.]*num_expts
acceptances = [0.]*num_expts
sigma_loga = 0.
sigma_acceptance = 0.

acceptance_target = 0.25
when_to_adapt = 100*num_params

num_total_iterations = 10000
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
mcmc = np.zeros((num_saved_iterations+1,num_all_params))
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




