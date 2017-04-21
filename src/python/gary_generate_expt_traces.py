import numpy as np
import numpy.random as npr
import mcmc_setup as ms
import ap_simulator

model_number = 8  # Decker dog
protocol = 1

solve_start,solve_end,solve_timestep,stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time = ms.get_protocol_details(protocol)

solve_timestep = 0.1
num_solves = 5

params_file = "gary_decker_params.txt"
traces_file = "gary_decker_traces.txt"

seed = 1
npr.seed(seed)

model_number = 8  # Decker dog
original_gs, g_parameters = ms.get_original_params(model_number)
original_gs = np.array(original_gs)
print original_gs, "\n"

times = np.arange(solve_start,solve_end+solve_timestep,solve_timestep)

ap = ap_simulator.APSimulator()

ap.DefineStimulus(stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time)
ap.DefineSolveTimes(solve_start,solve_end,solve_timestep)
ap.DefineModel(model_number)
ap.SetNumberOfSolves(num_solves)



mu = 1.1*original_gs
Sigma = np.diag((0.15*original_gs)**2)
num_expts = 200

expt_params = npr.multivariate_normal(mu, Sigma, num_expts)

expt_params[np.where(expt_params<0)] = 0.
np.savetxt(params_file, expt_params)

num_pts = int((solve_end-solve_start)/solve_timestep)+1
traces = np.zeros((num_expts, num_pts))

fig = plt.figure()
ax = fig.add_subplot(111)

for i in xrange(num_expts):
    temp_params = expt_params[i, :]
    ap.LoadStateVariables()
    temp_trace = ap.SolveForVoltageTraceWithParams(temp_params)
    noise_sd = (np.max(temp_trace)-np.min(temp_trace))/112.2
    traces[i, :] = temp_trace+noise_sd*npr.randn(num_pts)
    ax.plot(times, traces[i, :],alpha=0.1)
np.savetxt(traces_file, traces)

plt.show(block=True)





