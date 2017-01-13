import ap_simulator
import numpy as np
import matplotlib.pyplot as plt
import time
import mcmc_setup as ms
import cma

def prior_upper_bounds(original_gs):
    return 100*np.array(original_gs)

def sum_of_square_diffs(params,expt_trace,upper_bounds):
    stim_mag, stim_dur, stim_start = params[:3]
    stim_per = 1000
    if (stim_dur <= 0):
        #print "stim_dur <= 0"
        return np.inf
    if not (9 <= stim_start <= 10):
        #print "not (9 <= stim_start <= 10)"
        return np.inf
    test_gs = params[3:]
    if np.any(test_gs<0) or np.any(test_gs>upper_bounds):
        #print test_gs
        return np.inf
    ap.DefineStimulus(stim_mag, stim_dur, stim_per, stim_start)
    #ap.DefineSolveTimes(solve_start,solve_end,solve_timestep)
    ap.DefineModel(model_number)
    test_trace = ap.SolveForVoltageTraceWithParams(test_gs)
    return np.sum((test_trace-expt_trace)**2)

temp_dog_AP_file = "/home/rossj/workspace/RossJ/input/dog_traces_csv/dog_AP_trace_001.csv"
dog_AP = np.loadtxt(temp_dog_AP_file,delimiter=',')
expt_times = 1000*dog_AP[:,0]
expt_trace = 1000*dog_AP[:,1]


# 1. Hodgkin Huxley
# 2. Beeler Reuter
# 3. Luo Rudy
# 4. ten Tusscher
# 5. O'Hara Rudy
# 6. Davies (canine)
# 7. Paci (SC-CM ventricular)

model_number = 6
protocol = 1

solve_start,solve_end,solve_timestep,stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time = ms.get_protocol_details(protocol)

stimulus_start_time = 9.5 # manually from looking, should really set it exactly from original trace files

solve_start = expt_times[0]
solve_end = expt_times[-1]
solve_timestep = expt_times[1]-expt_times[0]

print (solve_end-solve_start)/solve_timestep
print len(expt_times)

noise_sd = 0.25
c_seed = 1

original_gs, g_parameters = ms.get_original_params(model_number)
upper_bounds = prior_upper_bounds(original_gs)

times = np.arange(solve_start,solve_end+solve_timestep,solve_timestep)

ap = ap_simulator.APSimulator()
ap.DefineSolveTimes(solve_start,solve_end,solve_timestep)

opts = cma.CMAOptions()
opts['seed'] = 1
x0 = np.concatenate(([stimulus_magnitude,stimulus_duration,stimulus_start_time],original_gs))

original_obj_fun = sum_of_square_diffs(x0,expt_trace,upper_bounds)
print "original_obj_fun =", original_obj_fun

sigma0 = 0.00001
es = cma.CMAEvolutionStrategy(x0, sigma0, opts)
while not es.stop():
    X = es.ask()
    es.tell(X, [sum_of_square_diffs(x,expt_trace,upper_bounds) for x in X])
    es.disp()
res = es.result()
print "res[0] =", res[0]

print "stimulus_magnitude,stimulus_duration,stimulus_start_time:", stimulus_magnitude,stimulus_duration,stimulus_start_time

stim_mag, stim_dur, stim_start = res[0][:3]
print "stim_mag, stim_dur, stim_start:", stim_mag, stim_dur, stim_start
stim_per = 1000
best_gs = res[0][3:]


ap.DefineStimulus(stim_mag,stim_dur,stim_per,stim_start)
#ap.DefineSolveTimes(solve_start,solve_end,solve_timestep)
ap.DefineModel(model_number)
best_fit_trace = ap.SolveForVoltageTraceWithParams(best_gs)

print "original_gs:", original_gs
print "best_gs:", best_gs

#print original_gs/best_gs


ap.DefineStimulus(stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time)
#ap.DefineSolveTimes(solve_start,solve_end,solve_timestep)
ap.DefineModel(model_number)
true_trace = ap.SolveForVoltageTraceWithParams(original_gs)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()
ax.plot(expt_times,expt_trace,color='red', label='Expt')
ax.plot(times,true_trace,color='blue',label='Original')
ax.plot(times,best_fit_trace,color='green',label='Best fit')
ax.legend()
plt.show(block=True)
