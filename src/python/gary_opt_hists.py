import numpy as np
import numpy.random as npr
import mcmc_setup as ms
import ap_simulator
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.optimize as so
import multiprocessing as mp
import time


def sum_of_square_diffs(temp_params, expt_trace):
    if np.any(temp_params < 0):
        return 1e9
    else:
        ap.LoadStateVariables()
        temp_trace = ap.SolveForVoltageTraceWithParams(temp_params)
        return np.sum((temp_trace-expt_trace)**2)


model_number = 8  # Decker dog
protocol = 1

solve_start,solve_end,solve_timestep,stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time = ms.get_protocol_details(protocol)

solve_timestep = 0.1
num_solves = 5

params_file = "gary_decker_params.txt"
traces_file = "gary_decker_traces.txt"

seed = 2
npr.seed(seed)

model_number = 8  # Decker dog
original_gs, g_parameters = ms.get_original_params(model_number)
original_gs = np.array(original_gs)
print original_gs, "\n"

lower_bounds = 0.5*original_gs
upper_bounds = 2.0*original_gs

times = np.arange(solve_start,solve_end+solve_timestep,solve_timestep)

true_params = np.loadtxt(params_file)
expt_traces = np.loadtxt(traces_file)

best_params_file = "gary_decker_optimize_best_fits.txt"
best_params = np.loadtxt(best_params_file)
#print "best_params:", best_params

num_expts, num_params = best_params.shape

percent_errors = 100.*np.abs(true_params-best_params)/true_params

"""for p in xrange(num_params):
    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax.hist(true_params[:,p], color='red', alpha=0.5, label="True")
    ax.hist(best_params[:,p], color='blue', alpha=0.5, label="Fits")
    ax.set_xlabel(g_parameters[p])
    ax.set_ylabel("Frequency")
    ax.legend()
    ax2 = fig.add_subplot(122)
    ax2.hist(percent_errors[:,p], color='green', label="% errors")
    ax2.set_xlabel(g_parameters[p])
    ax2.set_ylabel("Frequency")
    ax2.legend()
    fig.tight_layout()
    fig.savefig("gary_decker_opt_errors_{}.png".format(g_parameters[p]))
    plt.close()"""
    #plt.show(block=True)

print g_parameters
print "expt params means:", np.mean(true_params,axis=0)
print "expt params means / original_gs:", np.mean(true_params,axis=0)/original_gs
print "expt params s.d.s:", np.std(true_params,axis=0)
print "expt params s.d.s / original_gs:", np.std(true_params,axis=0)/original_gs
print "best fit params means:", np.mean(best_params,axis=0)
print "best fit params means / original_gs:", np.mean(best_params,axis=0)/original_gs
print "best fit params s.d.s:", np.std(best_params,axis=0)
print "best fit params s.d.s / original_gs:", np.std(best_params,axis=0)/original_gs
print "percent error means:", np.mean(percent_errors,axis=0)
print "percent error s.d.s:", np.std(percent_errors,axis=0)


