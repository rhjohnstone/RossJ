import numpy as np
import numpy.random as npr
import mcmc_setup as ms
import ap_simulator
#import matplotlib
#matplotlib.use('Agg')
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

ap = ap_simulator.APSimulator()

ap.DefineStimulus(stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time)
ap.DefineSolveTimes(solve_start,solve_end,solve_timestep)
ap.DefineModel(model_number)
ap.SetNumberOfSolves(num_solves)


true_params = np.loadtxt(params_file)
expt_traces = np.loadtxt(traces_file)

best_params_file = "gary_decker_optimize_best_fits.txt"
best_params = np.loadtxt(best_params_file)
#print "best_params:", best_params

num_expts = best_params.shape[0]

dp = 1
for e in xrange(num_expts):
#for e in xrange(2):
    print "expt", e
    expt_trace = expt_traces[e, :]
    best_sos = sum_of_square_diffs(best_params[e,:], expt_trace)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(times, expt_trace, color='red', label="Expt")
    ap.LoadStateVariables()
    ax.plot(times, ap.SolveForVoltageTraceWithParams(best_params[e,:]),label='Best fit, sos = {}'.format(round(best_sos,dp)))
    true_sos = sum_of_square_diffs(true_params[e,:], expt_trace)
    print "true_sos:", true_sos
    print "best_sos:", best_sos
    ap.LoadStateVariables()
    ax.plot(times, ap.SolveForVoltageTraceWithParams(true_params[e,:]),label='True params, sos = {}'.format(round(true_sos,dp)))
    ax.legend()
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Membrane voltage (mV)")
    fig.tight_layout()
    fig.savefig("gary_decker_opt_e_{}_best_fit.png".format(e))
    plt.close()
    #plt.show(block=True)

    print np.abs(best_params[e,:] - true_params[e,:]) / true_params[e,:], "\n"

