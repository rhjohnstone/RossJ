import numpy as np
import numpy.random as npr
import mcmc_setup as ms
import ap_simulator
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cma


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

num_expts = params.shape[0]

def run_cmaes(expt):
    expt_trace = traces[expt]
    opts = cma.CMAOptions()
    x0 = np.copy(original_gs)
    sigma0 = 0.1
    es = cma.CMAEvolutionStrategy(x0, sigma0, opts)
    while not es.stop():
        X = es.ask()
        f_vals = [sum_of_square_diffs(x, expt_trace) for x in X]
        es.tell(X, f_vals)
        es.disp()
    res = es.result()
    best_params = res[0]
    ap.LoadStateVariables()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(times, ap.SolveForVoltageTraceWithParams(best_params))
    ax.plot(times, expt_trace)
    fig.savefig("gary_decker_expt_{}_best_fit.png".format(expt)
    plt.close()
    
expt = 0
run_cmaes(expt)


