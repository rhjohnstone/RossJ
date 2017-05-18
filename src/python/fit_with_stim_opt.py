import ap_simulator
import numpy as np
import numpy.random as npr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
import mcmc_setup as ms
import cma
import multiprocessing as mp
import itertools as it
import scipy.optimize as so
import sys
import scipy.io as sio
import os







def prior_upper_bounds(original_gs):
    return 100*np.array(original_gs)


# 1. Hodgkin Huxley
# 2. Beeler Reuter
# 3. Luo Rudy
# 4. ten Tusscher
# 5. O'Hara Rudy
# 6. Davies (canine)
# 7. Paci (SC-CM ventricular)

model_number = 7
protocol = 1

original_gs, g_parameters = ms.get_original_params(model_number)
upper_bounds = [np.inf]*len(original_gs)

stimulus_start_time = 50 # manually from looking, should really set it exactly from original trace files
stimulus_magnitude = 0 # -25.5
stimulus_duration = 2
stimulus_period = 1000

data_clamp_on = 50
data_clamp_off = 52

extra_K_conc = 4

num_solves = 5

mat_file = "/home/rossj/Documents/roche_data/2017-01_data/170123_2/170123_2_2.mat"
output_dir = "/home/rossj/workspace/RossJ/roche_output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
all_APs = sio.loadmat(mat_file)

def do_for_trace(trace_number):


    def sum_of_square_diffs(params, expt_trace):#,expt_trace,upper_bounds,ap):
        if np.any(params<0) or np.any(params>upper_bounds):
            #print test_gs
            return np.inf
        #ap.LoadStateVariables()
        ap.SetToModelInitialConditions()
        test_trace = ap.SolveForVoltageTraceWithParams(params)
        return np.sum((test_trace-expt_trace)**2)
    

    try:
        trace_label = "Trace_2_2_{}_1".format(trace_number)
    except:
        print "No trace", trace_number
        return None
    expt_times = 1000.*all_APs[trace_label][:,0]
    expt_trace = 1000.*all_APs[trace_label][:,1]


    solve_start = expt_times[0]
    solve_end = expt_times[-1]
    solve_timestep = expt_times[1]-expt_times[0]

    times = np.arange(solve_start,solve_end+solve_timestep,solve_timestep)

    ap = ap_simulator.APSimulator()
    ap.SetNumberOfSolves(num_solves)
    ap.DefineSolveTimes(solve_start,solve_end,solve_timestep)
    ap.DefineStimulus(stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time)
    ap.DefineModel(model_number)
    ap.UseDataClamp(data_clamp_on, data_clamp_off)
    ap.SetExperimentalTraceAndTimesForDataClamp(expt_times, expt_trace)
    ap.SetExtracellularPotassiumConc(extra_K_conc)

    for python_seed in xrange(1,4):
        x0 = original_gs * (1. + npr.randn(len(original_gs)))

        x0[np.where(x0<0)] = 1e-5

        print "x0 =", x0

        original_obj_fun = sum_of_square_diffs(x0, expt_trace)#,expt_trace,upper_bounds,ap)
        print "original_obj_fun =", original_obj_fun


        start = time.time()


        res = so.minimize(sum_of_square_diffs, x0, args=(expt_trace,), method='Nelder-Mead')
        time_taken = time.time()-start
        best_gs = res.x
        best_f = res.fun

        print "\nTime taken: {} s\n".format(round(time_taken,1))

        #ap.LoadStateVariables()
        ap.SetToModelInitialConditions()
        best_fit_trace = ap.SolveForVoltageTraceWithParams(best_gs)

        print "original_gs:", original_gs
        print "best_gs:", best_gs

        #ap.LoadStateVariables()
        ap.SetToModelInitialConditions()
        true_trace = ap.SolveForVoltageTraceWithParams(original_gs)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.grid()
        ax.plot(expt_times,expt_trace,color='red', label='Expt')
        ax.plot(times,true_trace,color='blue',label='Original')
        ax.plot(times,best_fit_trace,color='green',label='Best fit')
        ax.legend()
        fig.tight_layout()
        fig.savefig(output_dir + "trace_{}_fit_to_model_{}_python_seed_{}.png".format(trace_number,model_number,python_seed))
        #plt.show()
        plt.close()
    return None
    
trace_numbers = range(90,150)
num_cores = 3
pool = mp.Pool(num_cores)
do_all_traces = pool.map_async(do_for_trace,trace_numbers).get(99999999999)
pool.close()
pool.join()

"""params_file = output_dir + "trace_{}_best_fit_params_model_{}.txt".format(trace_number,model_number)
with open(params_file,'w') as outfile:
    outfile.write("py_seed: " + str(python_seed) + "\n")
    outfile.write("initial: " + str(x0) + "\n")
    outfile.write("best_gs: " + str(best_gs) + "\n")
    outfile.write("best_f:  " + str(best_f) + "\n\n")"""

