import ap_simulator
import numpy as np
import matplotlib.pyplot as plt
import time
import mcmc_setup

def example_likelihood_function(trace):
    return np.sum(trace**2)

# 1. Hodgkin Huxley
# 2. Beeler Reuter
# 3. Luo Rudy
# 4. ten Tusscher
# 5. O'Hara Rudy
# 6. Davies (canine)
# 7. Paci (SC-CM ventricular)

for model_number in xrange(1,8):
    #model_number = 4
    protocol_number = 1
    
    noise_sd = 0.25
    c_seed = 1

    original_gs, g_parameters = mcmc_setup.get_original_params(model_number)

    #times = np.arange(solve_start,solve_end+sampling_timestep,sampling_timestep)

    ap = ap_simulator.APSimulator()

    ap.DefineProtocol(protocol_number)
    ap.DefineModel(model_number)
    expt_trace = ap.GenerateSyntheticExptTrace(original_gs,noise_sd,c_seed)


    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax.plot(times,trace)
    ax.plot(expt_trace)
    plt.show(block=True)
