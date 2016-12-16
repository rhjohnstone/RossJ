"""
CHOICE OF CELL MODEL 

1. Hodgkin Huxley '52
2. Beeler Reuter '77
3. Luo Rudy '91
4. Ten Tusscher Epi. '04
5. O'Hara Rudy Endo. '11
6. Davies 2012
7. Paci ventricular

"""

import numpy as np
import os
import sys

def get_original_params(model):
    if (model==1): # Hodgkin Huxley
        original_gs = [120,36,0.3]
        g_parameters = ['G_{Na}', 'G_K', 'G_l']
    elif (model==2): # Beeler Reuter
        original_gs = [0.04, 0.0035, 0.008, 9e-4]
        g_parameters = ['G_{Na}', 'G_{K1}', 'G_K', 'G_{CaL}']
    elif (model==3): # Luo Rudy
        original_gs = [23, 0.282, 0.6047, 0.09, 0.03921, 0.0183]
        g_parameters = ['G_{Na}', 'G_K', 'G_{K1}','G_{CaL}', 'G_l', 'G_{Kp}']
    elif (model==4): # Ten Tusscher Epi. 04
        original_gs = [14.838, 0.000175, 5.405, 0.096, 0.245, 1000, 0.294, 0.000592, 0.00029, 0.825, 0.0146, 1.362]
        g_parameters = ['G_{Na}', 'G_{CaL}', 'G_{K1}', 'G_{Kr}', 'G_{Ks}', 'k_{NaCa}',
                          'G_{to}', 'G_{bCa}', 'G_{bNa}', 'G_{pCa}', 'G_{pK}', 'P_{NaK}']
    elif (model==5): # O'Hara Rudy Endo. 11
        original_gs = [75, 0.0001, 0.003, 0.1908, 0.046, 0.0034, 0.0008, 30, 0.02, 2.5e-8, 3.75e-10, 0.0005, 0.0075]
        g_parameters = ['G_{Na}', 'G_{CaL}', 'G_{bK}', 'G_{K1}',
                          'G_{Kr}', 'G_{Ks}', 'k_{NaCa}', 'P_{NaK}',
                          'G_{to}', 'G_{bCa}', 'G_{bNa}', 'G_{pCa}', 'G_{NaL}']
    elif (model==6): # Davies 2012 dog
        original_gs = [8.25, 0.000243, 0.5, 0.00276,
                   0.00746925, 0.0138542, 0.0575, 0.0000007980336,
                   5.85, 0.61875, 0.1805, 4e-7,
                   0.000225, 0.011]
        g_parameters = ['G_{Na}', 'G_{CaL}', 'G_{K1}', 'G_{pK}',
                        'G_{Ks}', 'G_{Kr}', 'G_{pCa}', 'G_{bCa}',
                        'k_{NaCa}', 'P_{NaK}', 'G_{to1}', 'G_{to2}',
                        'G_{bCl}', 'G_{NaL}']
    elif (model==7): # Paci ventricular-like SC-CM
        original_gs = [3671.2302, 8.635702e-5, 28.1492, 2.041,
                   29.8667, 0.4125, 4900, 0.69264,
                   1.841424, 29.9038, 0.9, 30.10312]
        g_parameters = ['G_{Na}', 'G_{CaL}', 'G_{K1}', 'G_{Ks}',
                        'G_{Kr}', 'G_{pCa}', 'K_{NaCa}', 'G_{bCa}',
                        'P_{NaK}', 'G_{to}', 'G_{bNa}', 'G_f']
    return original_gs, g_parameters
    
def get_protocol_details(protocol): # pre-defined protocols
    if (protocol==1):
        solve_start = 0.
        solve_end = 400.
        solve_timestep = 0.2
        stimulus_magnitude = -25.5
        stimulus_duration = 2
        stimulus_period = 1000
        stimulus_start_time = 20
    return solve_start,solve_end,solve_timestep,stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time
    
def synthetic_nonhierarchical_chain_file_and_figs_dir(model,protocol,python_seed): # synthetic data
    # keeping it outside of Chaste build folder, in case that gets wiped in a clean build, or something
    output_dir = os.path.expanduser('~/RossJ_output/synthetic/nonhierarchical/model_{}/protocol_{}/python_seed_{}/'.format(model,protocol,python_seed))
    chain_dir = output_dir + 'chain/'
    figs_dir = output_dir + 'figures/'
    for d in [chain_dir,figs_dir]:
        if not os.path.exists(d):
            os.makedirs(d)
    chain_file = chain_dir + 'model_{}_protocol_{}_python_seed_{}_synthetic_nonhierarchical_mcmc.txt'.format(model,protocol,python_seed)
    return chain_file, figs_dir
    
def synthetic_hierarchical_chain_file_and_figs_dir(model,protocol,num_expts,python_seed): # synthetic data
    # keeping it outside of Chaste build folder, in case that gets wiped in a clean build, or something
    output_dir = os.path.expanduser('~/RossJ_output/synthetic/hierarchical/model_{}/protocol_{}/num_expts_{}/python_seed_{}/'.format(model,protocol,num_expts,python_seed))
    chain_dir = output_dir + 'chain/'
    figs_dir = output_dir + 'figures/'
    for d in [chain_dir,figs_dir]:
        if not os.path.exists(d):
            os.makedirs(d)
    chain_file = chain_dir + 'model_{}_protocol_{}_num_expts_{}_python_seed_{}_synthetic_hierarchical_mcmc.txt'.format(model,protocol,num_expts,python_seed)
    info_file = output_dir + 'model_{}_protocol_{}_num_expts_{}_python_seed_{}_synthetic_hierarchical_info.txt'.format(model,protocol,num_expts,python_seed)
    return chain_file, figs_dir, info_file
    















