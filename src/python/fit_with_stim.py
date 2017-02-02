import ap_simulator
import numpy as np
import matplotlib.pyplot as plt
import time
import mcmc_setup as ms
import cma
import multiprocessing as mp
import itertools as it



def prior_upper_bounds(original_gs):
    return 100*np.array(original_gs)


    

temp_dog_AP_file = "projects/RossJ/python/input/ken/033-2016090801_ControlRO01_1Hz_averagedTrace.txt"
dog_AP = np.loadtxt(temp_dog_AP_file)#,delimiter=',')
expt_times = dog_AP[:,0]
expt_trace = dog_AP[:,1]

print expt_times
print expt_trace


# 1. Hodgkin Huxley
# 2. Beeler Reuter
# 3. Luo Rudy
# 4. ten Tusscher
# 5. O'Hara Rudy
# 6. Davies (canine)
# 7. Paci (SC-CM ventricular)

model_number = 3
protocol = 1

#solve_start,solve_end,solve_timestep,stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time = ms.get_protocol_details(protocol)

stimulus_start_time = 0 # manually from looking, should really set it exactly from original trace files
stimulus_magnitude = -25.5
stimulus_duration = 2
stimulus_period = 1000

solve_start = expt_times[0]
solve_end = expt_times[-1]
solve_timestep = expt_times[1]-expt_times[0]

print (solve_end-solve_start)/solve_timestep
print len(expt_times)

noise_sd = 0.25
c_seed = 1

extra_K_conc = 4

original_gs, g_parameters = ms.get_original_params(model_number)
upper_bounds = prior_upper_bounds(original_gs)

times = np.arange(solve_start,solve_end+solve_timestep,solve_timestep)

ap = ap_simulator.APSimulator()
ap.DefineSolveTimes(solve_start,solve_end,solve_timestep)
ap.DefineStimulus(stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time)
ap.DefineModel(model_number)
ap.SetExtracellularPotassiumConc(extra_K_conc)

opts = cma.CMAOptions()
opts['seed'] = 1
x0 = np.copy(original_gs)

def sum_of_square_diffs(params):#,expt_trace,upper_bounds,ap):
    if np.any(params<0) or np.any(params>upper_bounds):
        #print test_gs
        return np.inf
    test_trace = ap.SolveForVoltageTraceWithParams(params)
    return np.sum((test_trace-expt_trace)**2)

original_obj_fun = sum_of_square_diffs(x0)#,expt_trace,upper_bounds,ap)
print "original_obj_fun =", original_obj_fun

start = time.time()

num_cores = mp.cpu_count()-1
if (num_cores < 1):
    num_cores = 1
pool = mp.Pool(num_cores)

sigma0 = 0.00001
es = cma.CMAEvolutionStrategy(x0, sigma0, opts)
while not es.stop():
    X = es.ask()
    f_vals = pool.map_async(sum_of_square_diffs,X).get(9999)
    #temp_vals = [sum_of_square_diffs(x,expt_trace,upper_bounds,ap) for x in X]
    es.tell(X, f_vals)
    es.disp()
pool.close()
res = es.result()
time_taken = time.time()-start
print "res[0] =", res[0]
best_gs = res[0]

print "\nTime taken: {} s\n".format(round(time_taken,1))

best_fit_trace = ap.SolveForVoltageTraceWithParams(best_gs)

print "original_gs:", original_gs
print "best_gs:", best_gs

#print original_gs/best_gs

true_trace = ap.SolveForVoltageTraceWithParams(original_gs)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()
ax.plot(expt_times,expt_trace,color='red', label='Expt')
ax.plot(times,true_trace,color='blue',label='Original')
ax.plot(times,best_fit_trace,color='green',label='Best fit')
ax.legend()
fig.tight_layout()
fig.savefig("ken_trace_fit_to_model_{}.png".format(model_number))
plt.close()
