"""
To run this case you need to creat the corresponding problem folders with the
appropriate meshes. Here we call them BSA_sensor_d=1, BSA_sensor_d=2,
BSA_sensor_d=4 and for the case of no protein BSA_sensor_d=infty. 
"""

import numpy
import time
import os

import pygbe
from pygbe.util.read_data import read_fields
from pygbe.lspr import main

from cext_wavelength_scanning import Cext_wave_scan

#Importing data
l_w, er_w, ei_w = numpy.loadtxt('../../data/wave_cext_d_prot_sensor/wave_water_diel_ang.txt',
                                unpack=True)
l_s, er_s, ei_s = numpy.loadtxt('../../data/wave_cext_d_prot_sensor/wave_silver_diel_ang.txt',
                                unpack=True)
l_p, er_p, ei_p = numpy.loadtxt('../../data/wave_cext_d_prot_sensor/wave_prot_diel_ang.txt',
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

field_dict_single = read_fields('../../../pygbe/examples/BSA_sensor_d=infty/sph_sensor.config')

tic_single = time.time() 
elec_field = -1
wave_single, Cext_single = Cext_wave_scan(elec_field, wavelength, E_field_single, field_dict_single,
                     '../../../pygbe/examples/BSA_sensor_d=infty')
toc_single = time.time()

numpy.savetxt('../../data/wave_cext_d_prot_sensor/wave_cext_d_infty.txt', 
              list(zip(wave_single, Cext_single)),
              fmt = '%.1f %.8f', 
              header = 'lambda [Ang], Cext, d=infty')


#Building E field for dictionary (protein)
E_field = [list(eps) for eps in zip(e_w, e_s, e_p)]


distance_path_folders = ['BSA_sensor_d=1', 
						 'BSA_sensor_d=2',
						 'BSA_sensor_d=4']

tic_d = time.time()
elec_field = -1
for path in distance_path_folders:

    folder_path = '../../../pygbe/examples/' + path
    full_path = os.path.abspath(folder_path)+'/'
    os.environ['PYGBE_PROBLEM_FOLDER'] = full_path
    
    field_dict = read_fields(folder_path+'/sphere_bsa.config')
    wave, Cext = Cext_wave_scan(elec_field, wavelength, E_field, field_dict,
                     '../../../pygbe/examples/'+path)
    toc=time.time()

    numpy.savetxt('../../data/wave_cext_d_prot_sensor/'+path+'.txt', 
              list(zip(wave, Cext)),
              fmt = '%.1f %.8f', 
              header = 'lambda [Ang], Cext'+path)
toc_d = time.time()

with open('../../data/wave_cext_d_prot_sensor/time_wave_Cext_d.txt', 'w') as f:
        print('total run time: {}'.format((toc_single-tic_single)+(toc_d-tic_d)),
                                    file=f)
