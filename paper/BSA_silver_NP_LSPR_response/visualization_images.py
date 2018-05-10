'''This file contains functions that help to produce the images of the proteins
locations respect to the sensor. 
'''

import numpy
from matplotlib import pyplot, rcParams

def read_data_vis(sensor, prt_one, prt_two):
    '''Reads the mesh files (.vert and .face) necessary to plot the 
    sensor-proteins display and save them as png. 

    Arguments:
    ---------
    sensor : str, path to the sensor mesh files without the extention. 
    prt_one: str, path to the protein one mesh files without the extention. 
    prt_two: str, path to the protein two files without the extention.

    Example:
    If the location of the mesh files, sensor.vert and sensor.face, is mesh_files/
    then:
    sensor = 'mesh_files/sensor' 
    '''
