import ap_simulator
import numpy as np
import matplotlib.pyplot as plt
import time
import mcmc_setup as ms

def example_likelihood_function(trace):
    return np.sum(trace**2)

# 1. Hodgkin Huxley
# 2. Beeler Reuter
# 3. Luo Rudy
# 4. ten Tusscher
# 5. O'Hara Rudy
# 6. Davies (canine)
# 7. Paci (SC-CM ventricular)
# 8. Decker 2009 dog

for model_number in xrange(8,9):
    #model_number = 4
    protocol = 1
    
    solve_start,solve_end,solve_timestep,stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time = ms.get_protocol_details(protocol)
    
    noise_sd = 0.25
    c_seed = 1

    original_gs, g_parameters = ms.get_original_params(model_number)

    times = np.arange(solve_start,solve_end+solve_timestep,solve_timestep)

    ap = ap_simulator.APSimulator()

    for stimulus_magnitude in [0,-25,-100]:
        ap.DefineStimulus(stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time)
        ap.DefineSolveTimes(solve_start,solve_end,solve_timestep)
        ap.DefineModel(model_number)
        true_trace = ap.SolveForVoltageTraceWithParams(original_gs)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        #ax.plot(times,trace)
        ax.plot(times,true_trace)
        plt.show(block=True)
