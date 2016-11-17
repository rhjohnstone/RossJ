import ap_simulator
import numpy as np
import matplotlib.pyplot as plt
import time

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

model_number = 4

if (model_number == 1):
    params = [120,36,0.3]
    solve_end = 80
elif (model_number == 2):
    params = [4e-2,0.0035,0.008,9e-4]
    solve_end = 400
elif (model_number == 3):
    params = [23,0.282,0.6047,0.09,0.03921,0.0183]
    solve_end = 400
elif (model_number == 4) or (model_number == 8):
    params = [14.838,0.000175,5.405,0.096,0.245,1000,0.294,0.000592,0.00029,0.825,0.0146,1.362]
    solve_end = 400
elif (model_number == 5):
    params = [75,0.0001,0.003,0.1908,0.046,0.0034,0.0008,30,0.02,2.5e-8,3.75e-10,0.0005,0.0075]
    solve_end = 400
elif (model_number == 6):
    params = [8.25,0.000243,0.5,0.00276,0.00746925,0.0138542,0.0575,0.0000007980336,5.85,0.61875,0.1805,4e-7,0.000225,0.011]
    solve_end = 400
elif (model_number == 7):
    params = [3671.2302,8.635702e-5,28.1492,2.041,29.8667,0.4125,4900,0.69264,1.841424,29.9038,0.9,30.10312]
    solve_end = 400

stim_amp = -25.5
stim_duration = 2
stim_period = 1000
stim_start = 10

solve_start = 0

sampling_timestep = 0.2

rel_tol = 1e-7
abs_tol = 1e-9

times = np.arange(solve_start,solve_end+sampling_timestep,sampling_timestep)

ap = ap_simulator.APSimulator()

ap.DefineStimulus(stim_amp,stim_duration,stim_period,stim_start)
ap.DefineModel(model_number)

ap.SetTolerances(rel_tol,abs_tol)

how_many = 1

start = time.time()
for _ in xrange(how_many):
    trace = ap.SolveForVoltageTraceWithParams(params,solve_start,solve_end,sampling_timestep)
time_taken = time.time()-start

print "Time taken: {} s".format(round(time_taken,2))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(times,trace)
plt.show(block=True)
