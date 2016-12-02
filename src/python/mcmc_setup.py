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
    
def nonhierarchical_chain_file_and_figs_dir(model,protocol,c_seed): # synthetic data
    # keeping it outside of Chaste build folder, in case that gets wiped in a clean build, or something
    output_dir = os.path.expanduser('~/RossJ_output/model_{}/protocol_{}/c_seed_{}/')
    chain_dir = output_dir + 'chain/'
    figs_dir = output_dir + 'figures/'
    for d in [chain_dir,figs_dir]:
        if not os.path.exists(d):
            os.makedirs(d)
    chain_file = chain_dir + 'model_{}_protocol_{}_c_seed_{}_mcmc.txt'.format(model,protocol,c_seed)
    return chain_file, figs_dir
    















