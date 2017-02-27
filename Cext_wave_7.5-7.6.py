import numpy
import time


import pygbe
from pygbe.util.read_data import read_fields
from pygbe.main import main

from cext_wavelength_scanning import create_diel_list, Cext_wave_scan, Cext_analytical


#Import silver case
lambda_75, ns_75, ks_75, nw_75, kw_75 = numpy.loadtxt('data/lambda_n_k_silver-7.5.txt',
                                                       unpack = True)

#Import gold case
lambda_76, ng_76, kg_76, nw_76, kw_76 = numpy.loadtxt('data/lambda_n_k_gold-7.6.txt',
                                                       unpack = True)


#Creating dielectric list for silver
diel_wat_75, diel_sil_75, diel_list_75 = create_diel_list(nw_75, kw_75, ns_75, ks_75)

#Creating dielectric list for gold
diel_wat_76, diel_gold_76, diel_list_76 = create_diel_list(nw_76, kw_76, ng_76, kg_76)

