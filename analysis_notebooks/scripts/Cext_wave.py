"""
To run this case you need to creat the corresponding problem folders with the
appropriate meshes. Here we call them lspr_silver/ and lspr_gold/

"""

import numpy
import time


import pygbe
from pygbe.util.read_data import read_fields
from pygbe.main import main

from cext_wavelength_scanning import create_diel_list, Cext_wave_scan, Cext_analytical


#Import silver case
lambda_75, ns_75, ks_75, nw_75, kw_75 = numpy.loadtxt('../../data/lambda_n_k_silver-7.5.txt',
                                                       unpack = True)

#Import gold case
lambda_76, ng_76, kg_76, nw_76, kw_76 = numpy.loadtxt('../../data/lambda_n_k_gold-7.6.txt',
                                                       unpack = True)


#Creating dielectric list for silver
diel_wat_75, diel_sil_75, diel_list_75 = create_diel_list(nw_75, kw_75, ns_75, ks_75)

#Creating dielectric list for gold
diel_wat_76, diel_gold_76, diel_list_76 = create_diel_list(nw_76, kw_76, ng_76, kg_76)

#Creating dictionary field. We will modify the 'E' key in the for loop.
field_dict_Ag = read_fields('../../../pygbe_dev/pygbe/examples/lspr_silver/sphereAg_complex.config')
field_dict_Au = read_fields('../../../pygbe_dev/pygbe/examples/lspr_gold/sphereAu_complex.config')

#Calculate Cext(lambda) for silver
tic_s = time.time()
wave_s, Cext_silver = Cext_wave_scan(lambda_75, diel_list_75, field_dict_Ag,
                     '../../../pygbe_dev/pygbe/examples/lspr_silver') 
toc_s = time.time()

#Calculate Cext(lambda) for gold
tic_g = time.time()
wave_g, Cext_gold = Cext_wave_scan(lambda_76, diel_list_76, field_dict_Au,
                     '../../../pygbe_dev/pygbe/examples/lspr_gold')
toc_g = time.time()

#Calculate Cext_analytical(lambda) for silver and gold, radius of sphere=10 nm
r = 10.
#Silver
Cext_an_silver = Cext_analytical(r, wave_s, diel_wat_75, diel_sil_75)

#Gold
Cext_an_gold = Cext_analytical(r, wave_g, diel_wat_76, diel_gold_76)

#Relative errors
error_silv = abs(Cext_silver-Cext_an_silver)/Cext_an_silver 
error_gold = abs(Cext_gold-Cext_an_gold)/Cext_an_gold

#Save wavelength, Cext, Cext_analytical, error
#Silver
numpy.savetxt('../../data/lambda_Cext_Cext_an_error_silver_7.5.txt', 
              list(zip(wave_s, Cext_silver, Cext_an_silver, error_silv)),
              fmt = '%.8f %.8f %.8f %.8f', 
              header = 'lambda [nm], Cext, Cext_analytical, error') 

#Gold
numpy.savetxt('../../data/lambda_Cext_Cext_an_error_gold_7.6.txt', 
              list(zip(wave_g, Cext_gold, Cext_an_gold, error_gold)),
              fmt = '%.8f %.8f %.8f %.8f', 
              header = 'lambda [nm], Cext, Cext_analytical, error') 

time_silver = toc_s - tic_s
time_gold = toc_g - tic_g
time_total = time_silver + time_gold

with open('../../data/time_7.5-7.6.txt', 'w') as f:
    print('time_silver: {} \ntime_gold: {} \ntime_total: {}'.format(time_silver,
          time_gold, time_total), file=f)

