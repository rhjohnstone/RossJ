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
# 8. ten Tusscher (Opt)

for model_number in xrange(1,8):
    #model_number = 4
    protocol_number = 1

    original_gs, g_parameters = mcmc_setup.get_original_params(model_number)

    #times = np.arange(solve_start,solve_end+sampling_timestep,sampling_timestep)

    ap = ap_simulator.APSimulator()

    ap.DefineProtocol(protocol_number)
    ap.DefineModel(model_number)


    how_many = 100

    start = time.time()
    for _ in xrange(how_many):
        trace = ap.SolveForVoltageTraceWithParams(original_gs)
    time_taken = time.time()-start

    print "Model {}, time taken for {} solves: {} s".format(model_number,how_many,round(time_taken,2))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax.plot(times,trace)
    ax.plot(trace)
    plt.show(block=True)
