import unittest
import ap_simulator
import time
import numpy as np
import subprocess

def example_loglikelihood(x):
    return np.sum(x**2)

class TestCompareStdOut(unittest.TestCase):

    def test_rossj(self):
        
        
        model_number = 1

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
        
        ap = ap_simulator.APSimulator()
        ap.DefineStimulus(stim_amp,stim_duration,stim_period,stim_start)
        ap.DefineModel(model_number)
        
        
        how_many_repeats = 1
        
        start = time.time()
        for _ in xrange(how_many_repeats):
            test_trace = ap.SolveForVoltageTraceWithParams(params,solve_start,solve_end,sampling_timestep)
            #example_loglikelihood_1 = example_loglikelihood(test_trace)
            example_loglikelihood_1 = ap.ExampleLogLikelihoodFunction(test_trace)
        time_taken = time.time()-start
        print "\nTime taken by ap_simulator SolveForVoltageTraceWithParams: {} s\n".format(round(time_taken,2))
        
        print test_trace
        
        
        #EXE_NAME = "./projects/RossJ/apps/TimesByTwoApp"
        EXE_NAME = "/home/rossj/chaste-build/projects/RossJ/apps/APApp" # this needs to be more general for chaste build path
        process = subprocess.Popen(EXE_NAME, False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        PROVENANCE_HEADER = "This version of Chaste was compiled on:"
	
        reading_values, looking_for_blank = False, False
        while (not reading_values):
            line = process.stdout.readline()
            if line.startswith(PROVENANCE_HEADER):
                looking_for_blank = True
            elif looking_for_blank and line.strip() == "":
                reading_values = True
                
                
        process.stdin.write(str(stim_amp) + '\n')
        process.stdin.write(str(stim_duration) + '\n')
        process.stdin.write(str(stim_period) + '\n')
        process.stdin.write(str(stim_start) + '\n')
        process.stdin.write(str(model_number) + '\n')
        
        process.stdin.write(str(solve_start) + '\n')
        process.stdin.write(str(solve_end) + '\n')
        process.stdin.write(str(sampling_timestep) + '\n')
        
        
        start = time.time()
        for _ in xrange(how_many_repeats):
            output_string_to_c = " ".join(map(str, params)) + '\n'
            process.stdin.write(output_string_to_c)
            example_loglikelihood_2 = float(process.stdout.readline())
        time_taken = time.time()-start
        print "\nTime taken by APApp: {} s\n".format(round(time_taken,2))
        
        if ( example_loglikelihood_1==example_loglikelihood_2 ):
            print "The two outputted 'log-likelihoods' are the same, don't worry."
        else:
            print example_loglikelihood_1
            print example_loglikelihood_2


if __name__ == '__main__':
    unittest.main()
