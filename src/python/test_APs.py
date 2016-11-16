import ap_simulator
import numpy as np
import matplotlib.pyplot as plt
import time

model_number = 1
params = [120,36,0.3]

stim_amp = -25
stim_duration = 2
stim_period = 1000
stim_start = 20

solve_start = 0
solve_end = 80
sampling_timestep = 0.2

rel_tol = 1e-6
abs_tol = 1e-8

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
