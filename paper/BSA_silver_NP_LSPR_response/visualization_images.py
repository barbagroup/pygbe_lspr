'''This file contains functions that help to produce the images of the proteins
locations respect to the sensor. 
'''

import numpy
from matplotlib import pyplot, rcParams

def read_data_plot(sensor, prt_one, prt_two, elev, azim, 
                    file_name=None, file_ext=None):
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

    elev  : float, set the elevation of the axes (elevation angle in the z plane). 
    azim  : float, set the azimuth of the axes (azimuth angle in the x,y plane).    
    '''

    #load sensor
    xs, ys, zs = numpy.loadtxt(fname=sensor+'.vert', unpack=True)
    face_s = numpy.loadtxt(fname=sensor+'.face') 
    face_sensor = face_s[:][:] - 1

    #load protein 1
    xp1, yp1, zp1 = numpy.loadtxt(fname=prt_one+'.vert', unpack=True) 
    f_11, f_21, f_31, g1, h1 = numpy.loadtxt(fname=prt_one+'.face', unpack=True)

    face_prt1 = numpy.array(list(zip(f_11, f_21, f_31)))
    face_protein_1 = face_prt1[:][:] - 1

    #load protein 2
    xp2, yp2, zp2 = numpy.loadtxt(fname=prt_two+'.vert', unpack=True)  
    f_12, f_22, f_32, g2, h2 = numpy.loadtxt(fname=prt_two+'.face', unpack=True)

    face_prt2 = numpy.array(list(zip(f_12, f_22, f_32)))
    face_protein_2 = face_prt2[:][:] - 1
