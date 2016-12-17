import ap_simulator as ap
import mcmc_setup as ms
import numpy as np
import numpy.random as npr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.stats as st
import time
import sys
import argparse

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

def log_pi_sigma(expt_datas,test_datas,sigma,num_expts,num_pts,uniform_noise_prior):
    if (not (uniform_noise_prior[0] < sigma < uniform_noise_prior[1])):
        return -np.inf
    else:
        return -num_expts*num_pts*np.log(sigma) - np.sum((expt_datas-test_datas)**2) / (2*sigma**2)
        
#if t > 1000*number_of_parameters:
def update_covariance_matrix(t,thetaCur,meanum_exptsstimate,cov_estimate,loga,accepted,when_to_adapt):
    s = t - when_to_adapt
    gamma_s = 1/(s+1)**0.6
    temp_covariance_bit = np.array([thetaCur-meanum_exptsstimate])
    new_cov_estimate = (1-gamma_s) * cov_estimate + gamma_s * np.dot(np.transpose(temp_covariance_bit),temp_covariance_bit)
    new_meanum_exptsstimate = (1-gamma_s) * meanum_exptsstimate + gamma_s * thetaCur
    new_loga = loga + gamma_s*(accepted-0.25)
    return new_cov_estimate, new_meanum_exptsstimate, new_loga
    
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--iterations", type=int, help="number of MCMC iterations",default=1000000)
parser.add_argument("-Ne", "--num-expts", type=int, help="number of synthetic dog AP traces",default=2)
parser.add_argument("-p", "--protocol", type=int, help="protocol number",default=1)
args = parser.parse_args()

model = 6 # just Davies dog for now
protocol = args.protocol
python_seed = 1
noise_sd = 0.25

num_expts = args.num_expts

uniform_noise_prior = [0,50]

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

#sys.exit()


chain_file, figs_dir, info_file = ms.synthetic_hierarchical_chain_file_and_figs_dir(model,protocol,num_expts,python_seed)

npr.seed(python_seed)

def normal_loglikelihood_uniform_priors(test_trace,expt_trace,sigma):
    num_pts = len(test_trace)
    sum_of_square_diffs = np.sum((test_trace-expt_trace)**2)
    return -num_pts*np.log(sigma)-sum_of_square_diffs/(2.*sigma**2)

solve_start,solve_end,solve_timestep,stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time = ms.get_protocol_details(protocol)

# need to make sure these are always same as in C++ protocol
# might have to change it to have protocols hard-coded into Python instead of C++

expt_times = np.arange(solve_start,solve_end+solve_timestep,solve_timestep)
num_pts = len(expt_times)
    
cell = ap.APSimulator()
cell.DefineStimulus(stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time)
cell.DefineSolveTimes(solve_start,solve_end,solve_timestep)
cell.DefineModel(model)

expt_traces = np.zeros((num_expts,num_pts))
fig = plt.figure()
ax = fig.add_subplot(111)
for i in xrange(num_expts):
    temp_trace = cell.SolveForVoltageTraceWithParams(expt_params[i,:])
    temp_trace += noise_sd*npr.randn(len(temp_trace))
    expt_traces[i,:] = temp_trace
    ax.plot(expt_times,temp_trace,label='Expt {}'.format(i+1))
print expt_traces
ax.legend()
fig.tight_layout()
fig.savefig(figs_dir+'expt_traces.png')
plt.close()

#sys.exit()

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

means = np.copy(theta_is_cur)
print "means:\n", means, "\n"

first_iteration = np.concatenate((top_theta_cur,top_sigma_squareds_cur,theta_is_cur.flatten(),[noise_sigma_cur])) # not including likelihoods
num_all_params = len(first_iteration)


temp_test_traces_cur = [cell.SolveForVoltageTraceWithParams(params) for params in theta_is_cur]

print temp_test_traces_cur

proposal_scale = 0.001

covariances = [proposal_scale*np.diag(expt_params[i,:]) for i in xrange(num_expts)]

print covariances

#sys.exit()

logas = [0.]*num_expts
acceptances = [0.]*num_expts
sigma_loga = 0.
sigma_acceptance = 0.

acceptance_target = 0.25
when_to_adapt = 20*num_g_params


with open(chain_file,"w") as outfile:
    outfile.write("# Synthetic hierarchical MCMC\n")
    outfile.write("# Model {}, protocol {}, python_seed {}\n".format(model,protocol,python_seed))
    outfile.write("# noise_sd {}\n".format(noise_sd))



num_total_iterations = args.iterations
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
mcmc = np.zeros((num_saved_iterations+1,num_all_params)) # when do I need to worry about memory?
mcmc[0,:] = first_iteration
start = time.time()
for it in xrange(1,num_total_iterations+1):
    for j in xrange(num_g_params):
        temp_eta = new_eta(old_eta_js[j,:],theta_is_cur[:,j])
        while True:
            temp_top_theta_cur, temp_top_sigma_squared_cur = sample_from_N_IG(temp_eta)
            if (temp_top_theta_cur > 0):
                top_theta_cur[j] = np.copy(temp_top_theta_cur)
                top_sigma_squareds_cur[j] = np.copy(temp_top_sigma_squared_cur)
                break
                
    # theta i's for each experiment
    for i in range(num_expts):
        while True:
            theta_i_star = npr.multivariate_normal(theta_is_cur[i,:],np.exp(logas[i])*covariances[i])
            if (np.all(theta_i_star>=0)):
                break
        temp_test_trace_star = cell.SolveForVoltageTraceWithParams(theta_i_star)
        target_cur = log_pi_theta_i(theta_is_cur[i,:],top_theta_cur,top_sigma_squareds_cur,noise_sigma_cur,expt_traces[i],temp_test_traces_cur[i])
        target_star = log_pi_theta_i(theta_i_star,top_theta_cur,top_sigma_squareds_cur,noise_sigma_cur,expt_traces[i],temp_test_trace_star)
        u = npr.rand()
        if (np.log(u) < target_star - target_cur):
            theta_is_cur[i,:] = np.copy(theta_i_star)
            temp_test_traces_cur[i] = temp_test_trace_star
            accepted = 1
        else:
            accepted = 0
        if (it > when_to_adapt):
            covariances[i],means[i],logas[i] = update_covariance_matrix(it,theta_is_cur[i,:],means[i],covariances[i],logas[i],accepted,when_to_adapt)
        acceptances[i] = (it*acceptances[i] + accepted)/(it+1)
    # noise sigma
    noise_sigma_star = noise_sigma_cur + np.exp(sigma_loga)*proposal_scale*npr.randn()
    
    target_star = log_pi_sigma(expt_traces,temp_test_traces_cur,noise_sigma_star,num_expts,num_pts,uniform_noise_prior)
    target_cur = log_pi_sigma(expt_traces,temp_test_traces_cur,noise_sigma_cur,num_expts,num_pts,uniform_noise_prior)
    
    u = npr.rand()
    if (np.log(u) < target_star - target_cur):
        noise_sigma_cur = noise_sigma_star
        accepted = 1
    else:
        accepted = 0
    sigma_acceptance = (it*sigma_acceptance + accepted)/(it+1)
    if (it > when_to_adapt):
        r = it - when_to_adapt
        gamma_r = 1/(r+1)**0.6
        sigma_loga += gamma_r*(accepted-acceptance_target)
    if ( it%thinning == 0 ):
        mcmc[it/thinning,:] = np.concatenate((top_theta_cur,top_sigma_squareds_cur,theta_is_cur.flatten(),[noise_sigma_cur]))

    if ( it%when_to_update==0 ):
        time_taken_so_far = time.time()-start
        estimated_time_left = time_taken_so_far/it*(num_total_iterations-it)
        print it/when_to_update, "/", how_many_updates
        print "Time taken: {} s = {} min".format(round(time_taken_so_far,1),round(time_taken_so_far/60.,2))
        print "acceptances:", acceptances
        print "logas:", logas
        print "Estimated time remaining: {} s = {} min".format(round(estimated_time_left,1),round(estimated_time_left/60.,2))
time_taken = time.time()-start
print "Time taken: {} s".format(round(time_taken,2))
print mcmc

print "\nShould be saved to", chain_file, "\n"
with open(chain_file,"a") as outfile:
    np.savetxt(outfile,mcmc)
    
with open(info_file,"w") as outfile:
    outfile.write("Model {}, protocol {}\n".format(model,protocol))
    outfile.write("python_seed {}\n".format(python_seed))
    outfile.write("noise_sd {}\n".format(noise_sd))
    outfile.write("num_total_iterations {}\n".format(num_total_iterations))
    outfile.write("num_saved_iterations {}\n".format(num_saved_iterations))
    outfile.write("time_taken = {} s = {} mins = {} hrs\n".format(round(time_taken),round(time_taken/60.,1),round(time_taken/3600.,2)))
    

for expt in xrange(num_expts):
    for i in xrange(num_g_params):
        original_value = expt_params[expt,i]
        label = g_parameters[i]
        param_index = (2+expt)*num_g_params+i
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.grid()
        ax.hist(mcmc[burn:,param_index],normed=True,bins=40,color='blue',edgecolor='blue')
        ax.axvline(original_value,color='red',lw=2)
        ax.set_ylabel('Probability density')
        ax.set_xlabel('Expt {}: $'.format(expt+1)+label+'$')
        fig.tight_layout()
        fig.savefig(figs_dir+"expt_{}_".format(expt+1)+label.translate(None,r'\\{}')+'_marginal.png') # need double slashes to get rid of the sigma slash for some reason
        plt.close()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()
ax.hist(mcmc[burn:,-1],normed=True,bins=40,color='blue',edgecolor='blue')
ax.axvline(noise_sd,color='red',lw=2)
ax.set_ylabel('Probability density')
ax.set_xlabel(r'$\sigma$')
fig.tight_layout()
fig.savefig(figs_dir+'sigma_marginal.png') # need double slashes to get rid of the sigma slash for some reason
plt.close()


for i in xrange(num_g_params):
    original_value = original_gs[i]
    label = g_parameters[i]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid()
    ax.hist(mcmc[burn:,i],normed=True,bins=40,color='blue',edgecolor='blue')
    ax.axvline(original_value,color='red',lw=2)
    ax.set_ylabel('Probability density')
    ax.set_xlabel(r'$\hat{'+label+r'}$')
    fig.tight_layout()
    fig.savefig(figs_dir+"top_"+label.translate(None,r'\\{}')+'_marginal.png') # need double slashes to get rid of the sigma slash for some reason
    plt.close()


for i in xrange(num_g_params):
    original_value = expt_params_cov_matrix[i,i]
    label = g_parameters[i]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid()
    ax.hist(mcmc[burn:,num_g_params+i],normed=True,bins=40,color='blue',edgecolor='blue')
    ax.axvline(original_value,color='red',lw=2)
    ax.set_ylabel('Probability density')
    ax.set_xlabel(r'$\sigma_{'+label+r'}^2$')
    fig.tight_layout()
    fig.savefig(figs_dir+"top_sigma_squared_"+label.translate(None,r'\\{}')+'_marginal.png') # need double slashes to get rid of the sigma slash for some reason
    plt.close()









