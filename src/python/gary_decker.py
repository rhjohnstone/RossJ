import ap_simulator
import numpy as np
import numpy.random as npr
import cma
import mcmc_setup as ms
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt



model = 8  # Decker dog
protocol = 1

solve_start,solve_end,solve_timestep,stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time = ms.get_protocol_details(protocol)

noise_sd = 0.25
c_seed = 1

original_gs, g_parameters = ms.get_original_params(model_number)

times = np.arange(solve_start,solve_end+solve_timestep,solve_timestep)

ap = ap_simulator.APSimulator()
ap.DefineStimulus(stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time)
ap.DefineSolveTimes(solve_start,solve_end,solve_timestep)
ap.DefineModel(model_number)
true_trace = ap.SolveForVoltageTraceWithParams(original_gs)

ap2 = ap_simulator.APSimulator()
ap2.DefineStimulus(stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time)
ap2.DefineSolveTimes(solve_start,solve_end,solve_timestep)
ap2.DefineModel(model_number)
ap2.LoadStateVariables()
ss_trace = ap2.SolveForVoltageTraceWithParams(original_gs)

fig = plt.figure()
ax = fig.add_subplot(111)
#ax.plot(times,trace)
ax.plot(times,true_trace,label='First AP')
ax.plot(times,ss_trace,label='SS AP')
plt.show(block=True)
