import numpy
import pygbe 
from pygbe.main import main

def Cext_wave_scan(wave_diel, field, example_folder_path):

    '''Computes the extinction cross section using PyGBe for different 
       wavelength and associated dielectric constants. 

    Arguments:
    ----------
    wave_diel          : list, each element is a tuple (wavelength, field('E'))
                         where field('E') is a list of the dielectric constant 
                         of each region.       
    field              : dictionary, config dictionary.
    example_folder_path: str, path to the example folder relative to wherever
                         the interpreter was started. 

    Returns:
    --------  
    Cext_wave          : list, list of cross extinction sections. 
    
    '''

    Cext_wave = []
    for wave, E in wave_diel:
        field['E'] = E  
        results = main(['', example_folder_path], field=field,
                  lspr=(-1,wave), return_results_dict=True)
        Cext_wave.append(results['Cext'])

    return Cext_wave


def Cext_analytical(radius, wavelength, diel_in, diel_out):
    '''Calculates the analytical solution of the extinction cross section.
       This solution is valid when the nano particle involved is a sphere. 
    
    Arguments:
    ----------
    radius    : float, radius of the sphere in [nm].
    wavelength: float/array of floats, wavelength of the incident
                electric field in [nm].
    diel_in   : complex/array of complex, dielectric constant inside surface. 
    diel_out  : complex/array of complex, dielectric constant inside surface.

    Returns:
    --------
    Cext_an   : float/array of floats, extinction cross section.
      
    '''
    wavenumber = 2*numpy.pi*numpy.sqrt(diel_out)/wavelength
    C1 = wavenumber**2*(diel_in/diel_out-1)/(diel_in/diel_out+2)
    Cext_an = 4*numpy.pi*radius**3/wavenumber.real * C1.imag 
    
    return Cext_an
