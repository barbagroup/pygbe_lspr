"""
To run this case you need to creat the corresponding problem folders with the
appropriate meshes. Here we call them multiple_sphere_d=1, multiple_sphere_d=2,
multiple_sphere_d=4
"""

import numpy
import time

import pygbe
from pygbe.util.read_data import read_fields
from pygbe.main import main

from scripts.cext_wavelength_scanning import Cext_wave_scan

#Importing data
l_w, er_w, ei_w = numpy.loadtxt('../data/wave_cext_d/wave_water_diel.txt',
                                unpack=True)
l_s, er_s, ei_s = numpy.loadtxt('../data/wave_cext_d/wave_silver_diel.txt',
                                unpack=True)
l_p, er_p, ei_p = numpy.loadtxt('../data/wave_cext_d/wave_prot_diel.txt',
                                unpack=True)

#Check the wavelength ranges are all equal
try:
    all(l_w == l_s) & all(l_s == l_p)
    wavelength = l_w
except:
    raise ValueError('The wavelength ranges are not equal, check data generation')
    

#Complex dielectric assembly
e_w = er_w + 1j*ei_w #water
e_s = er_s + 1j*ei_s #silver
e_p = er_p + 1j*ei_p #protein

#Building E field for single sphere dictionary
E_field_single = [list(eps) for eps in zip(e_w, e_s)]

field_dict_single = read_fields('../../pygbe_dev/pygbe/examples/lspr/sphere_complex.config')

tic_single = time.time() 

wave_single, Cext_single = Cext_wave_scan(wavelength, E_field_single, field_dict_single,
                     '../pygbe_dev/pygbe/examples/lspr')
toc_single = time.time()

numpy.savetxt('../data/wave_cext_d/wave_cext_d_infty.txt', 
              list(zip(wave_single, Cext_single)),
              fmt = '%.3f %.8f', 
              header = 'lambda [nm], Cext, d=infty')


#Building E field for dictionary (protein)
e_list = [list(eps) for eps in zip(e_w, e_s, e_p)]

E_field = []
for lst in e_list:
    E_field.append(lst+[lst[-1]]*5) 


distance_path_folders = ['multiple_sphere_d=1', 
						 'multiple_sphere_d=2',
						 'multiple_sphere_d=4']

tic_d = time.time()
for path in distance_path_folders:

    field_dict = read_fields('../../pygbe_dev/pygbe/examples/'
                            +path+'/seven_sphere_complex.config')
    wave, Cext = Cext_wave_scan(wavelength, E_field, field_dict,
                     '../../pygbe_dev/pygbe/examples/'+path)
    toc=time.time()

    numpy.savetxt('../data/wave_cext_d/'+path+'.txt', 
              list(zip(wave, Cext)),
              fmt = '%.3f %.8f', 
              header = 'lambda [nm], Cext'+path)
toc_d = time.time()

with open('../data/wave_cext_d/time_wave_Cext_d.txt', 'w') as f:
        print('total run time: {}'.format((toc_single-tic_single)+(toc_d-tic_d)),
                                    file=f)
