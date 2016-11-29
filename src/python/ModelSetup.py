# This will be imported into CMA-ES and MCMC scripts after command line arguments have been read

"""
CHOICE OF CELL MODEL 

1. Hodgkin-Huxley '52
2. Noble '62
3. Beeler-Reuter '77
4. Luo-Rudy '91
5. Ten-Tusscher Epi. '04
6. O'Hara-Rudy Endo. '11
7. Ten Tusscher Epi. '06
8. Courtemanche '98
9. Earm Noble '90
13. Beeler-Reuter '77 WITH DATA CLAMP
19. Davies 2012
"""

"""
CHOICE OF PROTOCOL
1. 1 pacing rate
2. 2 pacing rates
3. 1 pacing rate, with one current knocked out half-way
4. Extracellular potassium concentration halved
5. Extracellular potassium concentration doubled
6. Noise standard deviation is doubled
7. Noise s.d. quadrupled
13. Same as 1 but WITH DATA CLAMP for dog
"""

import numpy as np
import os
import sys

how_many_models = 9
how_many_protocols = 11
sigma = 0.25 # noise standard deviation

def ChooseModel(model,first_dog=None,allow_zero=False):
    global g_parameters
    if (model!=13) and (model!=14) and (model!=15) and (model!=16) and (model!=17) and (model!=18) and (model!=19) and (model!=20) and (model!=21) and (not (1 <= model <= how_many_models)):
        print "Only", how_many_models, "models available - got", model
        sys.exit()
    if model==1: # Hodgkin Huxley
        true_gs = [120,36,0.3]
        g_parameters = ['G_{Na}', 'G_K', 'G_l']
    elif model==2: # Noble
        true_gs = [400, 0.015, 1.2, 0.075]
        g_parameters = ['G_{Na}', 'G_{K1}', 'G_K', 'G_l']
    elif ((model==3) or (model==13)): # Beeler Reuter, regular and with data clamp, respectively
        true_gs = [0.04, 0.0035, 0.008, 9e-4]
        g_parameters = ['G_{Na}', 'G_{K1}', 'G_K', 'G_{CaL}']
    elif ((model==4) or (model==14)): # Luo Rudy, regular and with data clamp, respectively
        true_gs = [23, 0.282, 0.6047, 0.09, 0.03921, 0.0183]
        g_parameters = ['G_{Na}', 'G_K', 'G_{K1}','G_{CaL}', 'G_l', 'G_{Kp}']
    elif ((model==5) or (model==15)): # Ten Tusscher 04, regular and with data clamp, respectively
        true_gs = [14.838, 0.000175, 5.405, 0.096, 0.245, 1000, 0.294, 0.000592, 0.00029, 0.825, 0.0146, 1.362]
        g_parameters = ['G_{Na}', 'G_{CaL}', 'G_{K1}', 'G_{Kr}', 'G_{Ks}', 'k_{NaCa}',
                          'G_{to}', 'G_{bCa}', 'G_{bNa}', 'G_{pCa}', 'G_{pK}', 'P_{NaK}']
    elif ((model==6) or (model==16)): # O'Hara Rudy, regular and with data clamp, respectively
        true_gs = [75, 0.0001, 0.003, 0.1908, 0.046, 0.0034, 0.0008, 30, 0.02, 2.5e-8, 3.75e-10, 0.0005, 0.0075]
        g_parameters = ['G_{Na}', 'G_{CaL}', 'G_{bK}', 'G_{K1}',
                          'G_{Kr}', 'G_{Ks}', 'k_{NaCa}', 'P_{NaK}',
                          'G_{to}', 'G_{bCa}', 'G_{bNa}', 'G_{pCa}', 'G_{NaL}']
    elif ((model==17) or (model==18)): # Decker dog model, regular and with data clamp, respectively
        true_gs = [9.075, 0.00015552, 0.5, 0.00276,
                   0.0826, 0.0138542, 0.0575, 1.99508e-7,
                   4.5, 1.4, 0.497458, 9e-7,
                   0.000225, 0.0065, 3.2e-9]
        g_parameters = ['G_{Na}', 'G_{CaL}', 'G_{K1}', 'G_{pK}',
                        'G_{Ks}', 'G_{Kr}', 'G_{pCa}', 'G_{bCa}',
                        'k_{NaCa}', 'P_{NaK}', 'G_{to1}', 'G_{to2}',
                        'G_{bCl}', 'G_{NaL}', 'G_{bNa}']
    elif model==7:
        true_gs = [14.838, 0.0000398, 5.405, 0.153, 0.392, 1000, 0.294, 0.000592, 0.00029, 0.1238, 0.0146, 2.724]
        g_parameters = ['g_{Na}', 'g_{CaL}', 'g_{K1}', 'g_{Kr}', 'g_{Ks}', 'g_{NaCa}',
                          'g_{to}', 'g_{bCa}', 'g_{bNa}', 'g_{pCa}', 'g_{pK}', 'P_{NaK}']
    elif model==8:
        true_gs = [7.8, 0.12375, 0.09, 0.029411765,
                   0.12941176, 1600, 0.1652, 0.001131,
                   0.0006744375, 0.275, 0.59933874, 1]
        g_parameters = ['g_{Na}', 'g_{CaL}', 'g_{K1}', 'g_{Kr}', 'g_{Ks}', 'g_{NaCa}',
                          'g_{to}', 'g_{bCa}', 'g_{bNa}', 'g_{pCa}', 'P_{NaK}', 'g_{Kur}']
    elif model==9:
        true_gs = [0.5, 0.05, 0.017, 0.0001,
                   0.01, 5e-5, 0.0017, 0.00012,
                   0.14]
        g_parameters = ['g_{Na}', 'g_{CaL}', 'g_{K1}', 'g_{NaCa}', 'g_{to}',
                          'g_{bCa}', 'g_{bK}', 'g_{bNa}', 'P_{NaK}']
    elif model==19:
        true_gs = [8.25, 0.000243, 0.5, 0.00276,
                   0.00746925, 0.0138542, 0.0575, 0.0000007980336,
                   5.85, 0.61875, 0.1805, 4e-7,
                   0.000225, 0.011]
        g_parameters = ['G_{Na}', 'G_{CaL}', 'G_{K1}', 'G_{pK}',
                        'G_{Ks}', 'G_{Kr}', 'G_{pCa}', 'G_{bCa}',
                        'k_{NaCa}', 'P_{NaK}', 'G_{to1}', 'G_{to2}',
                        'G_{bCl}', 'G_{NaL}']
    elif model==20:
        true_gs = [3671.2302, 8.635702e-5, 28.1492, 2.041,
                   29.8667, 0.4125, 4900, 0.69264,
                   1.841424, 29.9038, 0.9, 30.10312]
        g_parameters = ['G_{Na}', 'G_{CaL}', 'G_{K1}', 'G_{Ks}',
                        'G_{Kr}', 'G_{pCa}', 'K_{NaCa}', 'G_{bCa}',
                        'P_{NaK}', 'G_{to}', 'G_{bNa}', 'G_f']
    elif model==21:
        true_gs = [6646.185, 8.635702e-5, 19.1925, 2.041,
                   29.8667, 0.4125, 2450, 0.69264,
                   1.4731392, 59.8077, 0.9, 30.10312]
        g_parameters = ['G_{Na}', 'G_{CaL}', 'G_{K1}', 'G_{Ks}',
                        'G_{Kr}', 'G_{pCa}', 'K_{NaCa}', 'G_{bCa}',
                        'P_{NaK}', 'G_{to}', 'G_{bNa}', 'G_f']
        
    assert(len(true_gs)==len(g_parameters))
    number_of_parameters = len(true_gs)+1
    true_gs.append(sigma)
    true_gs = np.array(true_gs)
    g_intervals = np.zeros((number_of_parameters,2))
    if (not allow_zero):
        if not first_dog:
            g_intervals[:,0] = 0.1*true_gs
            g_intervals[:,1] = 10*true_gs
        else:
            g_intervals[:,0] = 0.01*true_gs
            g_intervals[:,1] = 100*true_gs
    else:
        if not first_dog:
            g_intervals[:,0] = 0
            g_intervals[:,1] = 10*true_gs
        else:
            g_intervals[:,0] = 0
            g_intervals[:,1] = 100*true_gs
    return number_of_parameters, true_gs, g_parameters, g_intervals

def CheckProtocolChoice(protocol):
    if ((protocol!=13) and (protocol!=99) and (not (1 <= protocol <= how_many_protocols))):
        print "Only", how_many_protocols, "protocols available, got", protocol
        sys.exit()
    else:
        return None

def CheckFreeze(freeze,number_of_parameters):
    if (freeze < 0) or (freeze > number_of_parameters-2):
        return -1
    else:
        return freeze
        
def CreateHierarchicalMCMCOutputFiles(model,protocol,c_seed,python_seed,dog_traces=None,allow_zero=False):
    if dog_traces:
        directory = '~/MCMC/hierachical/AP_simulations/dog_traces/allow_zero/model_'+str(model)+'/protocol_'+str(protocol)+'/dog_traces_'
        for trace in dog_traces[:-1]:
            directory += str(trace)+'_'
        directory += str(dog_traces[-1])+'/'
    else:
        directory = '~/MCMC/hierachical/AP_simulations/synthetic/model_'+str(model)+'/protocol_'+str(protocol)+'/'
    directory = os.path.expanduser(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if dog_traces:
        final_states_file = directory + 'hierarchical_MCMC_m_'+str(model)+'_p_'+str(protocol)+'_python_seed_'+str(python_seed)+'_c_seed_'+str(c_seed)+'dog_traces_'
        for trace in dog_traces[:-1]:
            final_states_file += str(trace)+'_'
        final_states_file += str(dog_traces[-1])+'.txt'
    else:
        final_states_file = directory + 'synthetic_hierarchical_MCMC_m_'+str(model)+'_p_'+str(protocol)+'_python_seed_'+str(python_seed)+'_c_seed_'+str(c_seed)+'.txt'
    return directory, final_states_file

def CreateCMAESTestOutputFiles(model,protocol,c_seed,freeze,python_seed,first_dog=None,final_dog=None,allow_zero=False):
    if (not first_dog) and (allow_zero):
        directory = '~/MCMC/test/CMA-ES/synthetic_data/allow_zero/model_'+str(model)+'/protocol_'+str(protocol)+'/'
    if (not first_dog) and (not allow_zero):
        directory = '~/MCMC/test/CMA-ES/synthetic_data/no_zero/model_'+str(model)+'/protocol_'+str(protocol)+'/'
    elif (first_dog) and (not final_dog) and (allow_zero):
        directory = '~/MCMC/test/CMA-ES/dog_trace/allow_zero/model_'+str(model)+'/protocol_'+str(protocol)+'/dog_trace_'+str(first_dog)+'/'
    elif (first_dog) and (final_dog) and (allow_zero):
        directory = '~/MCMC/test/CMA-ES/dog_trace/allow_zero/model_'+str(model)+'/protocol_'+str(protocol)+'/dog_traces_'+str(first_dog)+'_to_'+str(final_dog)+'/'
    if (protocol==3):
        directory += g_parameters[freeze]+'/'
    directory = os.path.expanduser(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if (not first_dog):
        final_states_file_path = directory+'minimizer_final_states_python_seed_'+str(python_seed)+'_c_seed_'+str(c_seed)+'.txt'
    elif (first_dog) and (not final_dog):
        final_states_file_path = directory+'minimizer_final_states_python_seed_'+str(python_seed)+'_dog_trace_'+str(first_dog)+'.txt'
    elif (first_dog) and (final_dog):
        final_states_file_path = directory+'minimizer_final_states_python_seed_'+str(python_seed)+'_dog_traces_'+str(first_dog)+'_to_'+str(final_dog)+'.txt'
    return directory, final_states_file_path

def CreateCAMESOutputFiles(model,protocol,c_seed,freeze,python_seed,first_dog=None,final_dog=None,allow_zero=False):
    if (not allow_zero):
        if (not first_dog):
            if (protocol != 3):
                directory = '~/MCMC/synthetic_data/no_zero/minimizer/CMA-ES/model_'+str(model)+'/protocol_'+str(protocol)+'/'
            else:
                directory = '~/MCMC/synthetic_data/no_zero/minimizer/CMA-ES/model_'+str(model)+'/protocol_3/'+g_parameters[freeze]+'/'
        else:
            if (protocol != 3):
                directory = '~/MCMC/dog_trace/no_zero/minimizer/CMA-ES/model_'+str(model)+'/protocol_'+str(protocol)+'/'
            else:
                directory = '~/MCMC/dog_trace/no_zero/minimizer/CMA-ES/model_'+str(model)+'/protocol_3/'+g_parameters[freeze]+'/'
    else:
        if (not first_dog):
            if (protocol != 3):
                directory = '~/MCMC/synthetic_data/allow_zero/minimizer/CMA-ES/model_'+str(model)+'/protocol_'+str(protocol)+'/'
            else:
                directory = '~/MCMC/synthetic_data/allow_zero/minimizer/CMA-ES/model_'+str(model)+'/protocol_3/'+g_parameters[freeze]+'/'
        else:
            if (protocol != 3):
                directory = '~/MCMC/dog_trace/allow_zero/minimizer/CMA-ES/model_'+str(model)+'/protocol_'+str(protocol)+'/'
            else:
                directory = '~/MCMC/dog_trace/allow_zero/minimizer/CMA-ES/model_'+str(model)+'/protocol_3/'+g_parameters[freeze]+'/'
    directory = os.path.expanduser(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if (not first_dog):
        final_states_file_path = directory+'minimizer_final_states_python_seed_'+str(python_seed)+'_c_seed_'+str(c_seed)+'.txt'
    elif (first_dog) and (not final_dog):
        final_states_file_path = directory+'minimizer_final_states_python_seed_'+str(python_seed)+'_dog_trace_'+str(first_dog)+'.txt'
    else:
        final_states_file_path = directory+'minimizer_final_states_python_seed_'+str(python_seed)+'_dog_traces_'+str(first_dog)+'_to_'+str(final_dog)+'.txt'
    return directory, final_states_file_path

def CreateTestMCMCOutputFiles(model,protocol,c_seed,freeze,python_seed,first_dog,final_dog,allow_zero,thinning):
    if (not allow_zero):
        if (not first_dog):
            if (protocol != 3):
                directory = '~/MCMC/test/synthetic_data/no_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_'+str(protocol)+'/'
            else:
                directory = '~/MCMC/test/synthetic_data/no_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_3/'+g_parameters[freeze]+'/'
        elif (first_dog) and (not final_dog):
            if (protocol != 3):
                directory = '~/MCMC/test/dog_trace/no_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_'+str(protocol)+'/dog_trace_'+str(first_dog)+'/'
            else:
                directory = '~/MCMC/test/dog_trace/no_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_3/'+g_parameters[freeze]+'/dog_trace_'+str(first_dog)+'/'
        else:
            if (protocol != 3):
                directory = '~/MCMC/test/dog_trace/no_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_'+str(protocol)+'/dog_traces_'+str(first_dog)+'_to_'+str(final_dog)+'/'
            else:
                directory = '~/MCMC/test/dog_trace/no_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_3/'+g_parameters[freeze]+'/dog_traces_'+str(first_dog)+'_to_'+str(final_dog)+'/'
    else:
        if (not first_dog):
            if (protocol != 3):
                directory = '~/MCMC/test/synthetic_data/allow_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_'+str(protocol)+'/'
            else:
                directory = '~/MCMC/test/synthetic_data/allow_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_3/'+g_parameters[freeze]+'/'
        elif (first_dog) and (not final_dog):
            if (protocol != 3):
                directory = '~/MCMC/test/dog_trace/allow_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_'+str(protocol)+'/dog_trace_'+str(first_dog)+'/'
            else:
                directory = '~/MCMC/test/dog_trace/allow_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_3/'+g_parameters[freeze]+'/dog_trace_'+str(first_dog)+'/'
        else:
            if (protocol != 3):
                directory = '~/MCMC/test/dog_trace/allow_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_'+str(protocol)+'/dog_traces_'+str(first_dog)+'_to_'+str(final_dog)+'/'
            else:
                directory = '~/MCMC/test/dog_trace/allow_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_3/'+g_parameters[freeze]+'/dog_traces_'+str(first_dog)+'_to_'+str(final_dog)+'/'
    directory = os.path.expanduser(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if (freeze < 0) and (protocol != 3):
        if (not first_dog):
            file_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_python_seed_'+str(python_seed)+'_c_seed_'+str(c_seed)+'.txt'
            covariance_estimate_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_python_seed_'+str(python_seed)+'_c_seed_'+str(c_seed)+'_covariance_estimate.txt'
        elif (first_dog) and (not final_dog):
            file_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_python_seed_'+str(python_seed)+'_dog_trace_'+str(first_dog)+'.txt'
            covariance_estimate_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_python_seed_'+str(python_seed)+'_dog_trace_'+str(first_dog)+'_covariance_estimate.txt'
        else:
            file_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_python_seed_'+str(python_seed)+'_dog_traces_'+str(first_dog)+'_to_'+str(final_dog)+'.txt'
            covariance_estimate_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_python_seed_'+str(python_seed)+'_dog_traces_'+str(first_dog)+'_to_'+str(final_dog)+'_covariance_estimate.txt'
    elif (freeze < 0) and (protocol == 3):
        file_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_no_freezing_python_seed_'+str(python_seed)+'_c_seed_'+str(c_seed)+'.txt'
        covariance_estimate_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_no_freezing_python_seed_'+str(python_seed)+'_c_seed_'+str(c_seed)+'_covariance_estimate.txt'
    else:
        file_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_'+g_parameters[freeze]+'_python_seed_'+str(python_seed)+'_c_seed_'+str(c_seed)+'.txt'
        covariance_estimate_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_'+g_parameters[freeze]+'_python_seed_'+str(python_seed)+'_c_seed_'+str(c_seed)+'_covariance_estimate.txt'
    return directory, file_path, covariance_estimate_path

def CreateMCMCOutputFiles(model,protocol,c_seed,freeze,python_seed,first_dog,allow_zero,thinning):
    if (not allow_zero):
        if (not first_dog):
            if (protocol != 3):
                directory = '~/MCMC/synthetic_data/no_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_'+str(protocol)+'/'
            else:
                directory = '~/MCMC/synthetic_data/no_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_3/'+g_parameters[freeze]+'/'
        elif (first_dog) and (not final_dog):
            if (protocol != 3):
                directory = '~/MCMC/dog_trace/no_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_'+str(protocol)+'/dog_trace_'+str(first_dog)+'/'
            else:
                directory = '~/MCMC/dog_trace/no_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_3/'+g_parameters[freeze]+'/dog_trace_'+str(first_dog)+'/'
        else:
            if (protocol != 3):
                directory = '~/MCMC/dog_trace/no_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_'+str(protocol)+'/dog_traces_'+str(first_dog)+'_to_'+str(final_dog)+'/'
            else:
                directory = '~/MCMC/dog_trace/no_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_3/'+g_parameters[freeze]+'/dog_traces_'+str(first_dog)+'_to_'+str(final_dog)+'/'
    else:
        if (not first_dog):
            if (protocol != 3):
                directory = '~/MCMC/synthetic_data/allow_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_'+str(protocol)+'/'
            else:
                directory = '~/MCMC/synthetic_data/allow_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_3/'+g_parameters[freeze]+'/'
        elif (first_dog) and (not final_dog):
            if (protocol != 3):
                directory = '~/MCMC/dog_trace/allow_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_'+str(protocol)+'/dog_trace_'+str(first_dog)+'/'
            else:
                directory = '~/MCMC/dog_trace/allow_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_3/'+g_parameters[freeze]+'/dog_trace_'+str(first_dog)+'/'
        else:
            if (protocol != 3):
                directory = '~/MCMC/dog_trace/allow_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_'+str(protocol)+'/dog_traces_'+str(first_dog)+'_to_'+str(final_dog)+'/'
            else:
                directory = '~/MCMC/dog_trace/allow_zero/adaptive_MCMC/thinned_every_'+str(thinning)+'/model_'+str(model)+'/protocol_3/'+g_parameters[freeze]+'/dog_traces_'+str(first_dog)+'_to_'+str(final_dog)+'/'
    directory = os.path.expanduser(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if (freeze < 0) and (protocol != 3):
        if (not first_dog):
            file_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_python_seed_'+str(python_seed)+'_c_seed_'+str(c_seed)+'.txt'
            covariance_estimate_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_python_seed_'+str(python_seed)+'_c_seed_'+str(c_seed)+'_covariance_estimate.txt'
        elif (first_dog) and (not final_dog):
            file_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_python_seed_'+str(python_seed)+'_dog_trace_'+str(first_dog)+'.txt'
            covariance_estimate_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_python_seed_'+str(python_seed)+'_dog_trace_'+str(first_dog)+'_covariance_estimate.txt'
        else:
            file_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_python_seed_'+str(python_seed)+'_dog_traces_'+str(first_dog)+'_to_'+str(final_dog)+'.txt'
            covariance_estimate_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_python_seed_'+str(python_seed)+'_dog_traces_'+str(first_dog)+'_to_'+str(final_dog)+'_covariance_estimate.txt'
    elif (freeze < 0) and (protocol == 3):
        file_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_no_freezing_python_seed_'+str(python_seed)+'_c_seed_'+str(c_seed)+'.txt'
        covariance_estimate_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_no_freezing_python_seed_'+str(python_seed)+'_c_seed_'+str(c_seed)+'_covariance_estimate.txt'
    else:
        file_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_'+g_parameters[freeze]+'_python_seed_'+str(python_seed)+'_c_seed_'+str(c_seed)+'.txt'
        covariance_estimate_path = directory+'model_'+str(model)+'_protocol_'+str(protocol)+'_MCMC_noisy_adaptive_covariance_matrix_thinned_every_'+str(thinning)+'_'+g_parameters[freeze]+'_python_seed_'+str(python_seed)+'_c_seed_'+str(c_seed)+'_covariance_estimate.txt'
    return directory, file_path, covariance_estimate_path
