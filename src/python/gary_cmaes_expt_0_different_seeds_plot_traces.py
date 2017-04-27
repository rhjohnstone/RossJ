import numpy as np
import numpy.random as npr
import mcmc_setup as ms
import ap_simulator
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cma
import multiprocessing as mp


def sum_of_square_diffs(temp_params, expt_trace):
    if np.any(temp_params < lower_bounds) or np.any(temp_params > upper_bounds):
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


params = np.loadtxt(params_file)
traces = np.loadtxt(traces_file)

num_expts, num_params = params.shape

best_params_file = "gary_decker_expt_0_different_seeds_best_fits.txt"

e = 0

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(times, traces[e,:], label='Synth expt')
#ax.plot(times, ap.SolveForVoltageTraceWithParams(params[e,:]))
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Membrane voltage (mV)")

best_paramses = np.loadtxt("gary_decker_expt_0_different_seeds_best_fits.txt")
best_index = 0
best_sos = 2e9
for i in xrange(best_paramses.shape[0]):
    temp_sos = sum_of_square_diffs(best_paramses[i,:], traces[e,:])
    #print i, temp_sos
    if temp_sos < best_sos:
        best_sos = temp_sos
        best_index = i
dp = 1
ap.LoadStateVariables()
ax.plot(times, ap.SolveForVoltageTraceWithParams(best_paramses[best_index,:]),label='Best fit, sos = {}'.format(round(best_sos,dp)))
true_sos = sum_of_square_diffs(params[e,:], traces[e,:])
print "true_sos:", true_sos
print "best_sos:", best_sos
ap.LoadStateVariables()
ax.plot(times, ap.SolveForVoltageTraceWithParams(params[e,:]),label='True params, sos = {}'.format(round(true_sos,dp)))
ax.legend()
#plt.show(block=True)

test_params = np.copy(best_paramses[best_index,:])
test_params[0] = params[e,0]
test_sos = sum_of_square_diffs(test_params, traces[e,:])
print "test_sos:", test_sos

print np.abs((best_paramses[best_index,:]-params[e,:])/params[e,:])
