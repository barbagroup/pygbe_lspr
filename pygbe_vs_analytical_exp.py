import numpy
import time

from matplotlib import pyplot
from scipy.interpolate import interp1d, splev, splrep

import pygbe
from pygbe.util.read_data import read_fields
from pygbe.main import main

from data_analysis_helper import nm_from_ev, linear_interp, wave_filter_interp
from cext_wavelength_scanning import create_diel_list, Cext_wave_scan, Cext_analytical


#Import silver data
ev_s, n_s, k_s = numpy.loadtxt('gold_silver_water_raw-data/silver_JC72.txt', 
                                 unpack=True)

#Import gold data
ev_g, n_g, k_g = numpy.loadtxt('gold_silver_water_raw-data/gold_JC72.txt', 
                                 unpack=True)

#ev_s is equal to ev_g so we convert only one
lambda_s = nm_from_ev(ev_s)

#Save silver data using [nm] in case we need it.
numpy.savetxt('gold_silver_water_raw-data/silver_JC72_nm.txt',
               list(zip(lambda_s, n_s, k_s)), fmt='%.8f %.3e %.3e',
               header='lambda [nm], refrac_index_real, refrac_index_imag') 

#Save gold data using [nm] in case we need it.
numpy.savetxt('gold_silver_water_raw-data/gold_JC72_nm.txt',
               list(zip(lambda_s, n_g, k_g)), fmt='%.8f %.3e %.3e',
               header='lambda [nm], refrac_index_real, refrac_index_imag')

#Import water data 
lambda_w, n_w, k_w = numpy.loadtxt('gold_silver_water_raw-data/water_HQ72.txt',
                                    unpack=True)

#Water linear interpolation
water_real_linear , water_imag_linear = linear_interp(lambda_w, n_w, k_w)

#Removing values of wavelngth that are out of range in the water interpolation
#range
lambda_wsg, idx_min, idx_max = wave_filter_interp(lambda_s, lambda_w)

#Calculate n and k for water. We evaluate the function obtain after interpolation.
n_w = water_real_linear(lambda_wsg)
k_w = water_imag_linear(lambda_wsg)

#Remove values of n and k from silver and gold that are out of range compared
#to the ones for water.
#Silver
n_s = n_s[idx_min:idx_max]
k_s = k_s[idx_min:idx_max]
#Gold
n_g = n_g[idx_min:idx_max]
k_g = k_g[idx_min:idx_max]

#Save data in case we need it 
numpy.savetxt('data/lambda_refrac_water_silv_gold.txt', 
               list(zip(lambda_wsg, n_w, k_w, n_s, k_s, n_g, k_g)),
               fmt='%.8f %.8e %.8e %.8e %.8e %.8e %.8e',
               header='lambda [nm], refrac_real_water, refrac_imag_water, refrac_real_silver, refrac_imag_silver, refrac_real_gold, refrac_imag_gold')

#Creating dielectric list for silver
diel_wat_s, diel_sil, diel_list_silv = create_diel_list(n_w, k_w, n_s, k_s)

#Creating dielectric list for gold
diel_wat_g, diel_gold, diel_list_gold = create_diel_list(n_w, k_w, n_g, k_g)

#Creating dictionary field. We will modify the 'E' key in the for loop.
field_dict = read_fields('sphere_complex.config')

#Calculate Cext(lambda) for silver
wave_s, Cext_silver = Cext_wave_scan(lambda_wsg, diel_list_silv, field_dict,
                     '../pygbe_dev/pygbe/examples/lspr') 

#Calculate Cext(lambda) for gold
wave_g, Cext_gold = Cext_wave_scan(lambda_wsg, diel_list_gold, field_dict,
                     '../pygbe_dev/pygbe/examples/lspr')

#Calculate Cext_analytical(lambda) for silver and gold, radius of sphere=10 nm
r = 10.
#Silver
tic_s = time.time()
Cext_an_silver = Cext_analytical(r, wave_s, diel_wat_s, diel_sil)
toc_s = time.time()

#Gold
tic_g = time.time()
Cext_an_gold = Cext_analytical(r, wave_g, diel_wat_g, diel_gold)
toc_g = time.time()

#Absolute errors
error_silv = abs(Cext_silver-Cext_an_silver)/Cext_an_silver 
error_gold = abs(Cext_gold-Cext_an_gold)/Cext_an_gold

#Save wavelength, Cext, Cext_analytical, error
#Silver
numpy.savetxt('data/lambda_Cext_Cext_an_error_silver_8K.txt', 
              list(zip(wave_s, Cext_silver, Cext_an_silver, error_silv)),
              fmt = '%.8f %.8f %.8f %.8f', 
              header = 'lambda [nm], Cext, Cext_analytical, error - (Mesh of 8K elements)') 

#Gold
numpy.savetxt('data/lambda_Cext_Cext_an_error_gold_8K.txt', 
              list(zip(wave_g, Cext_gold, Cext_an_gold, error_gold)),
              fmt = '%.8f %.8f %.8f %.8f', 
              header = 'lambda [nm], Cext, Cext_analytical, error - (Mesh of 8K elements)') 

time_silver = toc_s - tic_s
time_gold = toc_g - tic_g
time_total = time_silver + time_gold

with open('time_8K.txt', 'w') as f:
    print('time_silver: {} \ntime_gold: {} \ntime_total: {}'.format(time_silver,
          time_gold, time_total), file=f)

