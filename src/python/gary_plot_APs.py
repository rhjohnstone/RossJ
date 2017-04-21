import ap_simulator
import numpy as np
import numpy.random as npr
import cma
import mcmc_setup as ms
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

expt = 1

params_file = "gary_decker_params.txt"
params = np.loadtxt(params_file)[expt-1, :]

model_number = 8  # Decker dog
protocol = 1

solve_start,solve_end,solve_timestep,stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time = ms.get_protocol_details(protocol)

solve_timestep = 0.1
num_solves = 5

original_gs, g_parameters = ms.get_original_params(model_number)

times = np.arange(solve_start,solve_end+solve_timestep,solve_timestep)

ap = ap_simulator.APSimulator()

ap.DefineStimulus(stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time)
ap.DefineSolveTimes(solve_start,solve_end,solve_timestep)
ap.DefineModel(model_number)
ap.SetNumberOfSolves(num_solves)
ap.LoadStateVariables()
true_trace = ap.SolveForVoltageTraceWithParams(original_gs)
ap.LoadStateVariables()
new_trace = ap.SolveForVoltageTraceWithParams(params)

fig = plt.figure()
ax = fig.add_subplot(111)
#ax.plot(times,trace)
ax.plot(times,true_trace,label='First AP')
ax.plot(times,new_trace,label='New AP')
ax.legend()
plt.show(block=True)
