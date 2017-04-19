import ap_simulator as ap
import mcmc_setup as ms
import numpy as np
import matplotlib.pyplot as plt

expt_dir = "/home/rossj/Documents/roche_data/2017-01_data/170123_2_2"
traces_dir = expt_dir + '/traces'
output_dir = expt_dir + '/output'
trace_number = 65
AP = np.loadtxt(traces_dir+'/{}.csv'.format(trace_number),delimiter=',')
expt_times = AP[:,0]
expt_trace = AP[:,1]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()
ax.plot(expt_times,expt_trace,color='red')

model = 7
original_gs, g_parameters = ms.get_original_params(model) # list, list
#original_gs[0] *= 4

solve_start = expt_times[0]
solve_end = expt_times[-1]
solve_timestep = expt_times[1] - expt_times[0]

data_clamp_on = 50
data_clamp_off = 52

num_solves = 100

stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time = 0, 1, 1000, 0

# need to make sure these are always same as in C++ protocol
# might have to change it to have protocols hard-coded into Python instead of C++

expt_times = np.arange(solve_start,solve_end+solve_timestep,solve_timestep)
num_pts = len(expt_times)
    
cell = ap.APSimulator()
cell.SetNumberOfSolves(num_solves)
cell.DefineStimulus(stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time)
cell.DefineSolveTimes(solve_start,solve_end,solve_timestep)
cell.DefineModel(model)
cell.UseDataClamp(data_clamp_on, data_clamp_off)
cell.SetExperimentalTraceAndTimesForDataClamp(expt_times, expt_trace)
test_trace = cell.SolveForVoltageTraceWithParams(original_gs)
print "len(test_trace) =", len(test_trace)
print "len(expt_times) =", len(expt_times)
ax.plot(expt_times,test_trace,color='blue')
ax.axvline(data_clamp_on,color='green')
ax.axvline(data_clamp_off,color='green')

plt.show(block=True)
