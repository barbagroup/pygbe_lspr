'''This file contains functions that help to analyze and plot data related
to the single silver sphere verification.
'''

import numpy
from matplotlib import pyplot, rcParams



def Cext_analytical(radius, wavelength, diel_out, diel_in):
    '''Calculates the analytical solution of the extinction cross section.
       This solution is valid when the nano particle involved is a sphere. 
    
    Arguments:
    ----------
    radius    : float, radius of the sphere in [nm].
    wavelength: float/array of floats, wavelength of the incident
                electric field in [nm].
    diel_out  : complex/array of complex, dielectric constant inside surface.
    diel_in   : complex/array of complex, dielectric constant inside surface. 

    Returns:
    --------
    Cext_an   : float/array of floats, extinction cross section.
      
    '''
    wavenumber = 2*numpy.pi*numpy.sqrt(diel_out)/wavelength
    C1 = wavenumber**2*(diel_in/diel_out-1)/(diel_in/diel_out+2)
    Cext_an = 4*numpy.pi*radius**3/wavenumber.real * C1.imag 
    
    return Cext_an

def plot_cext_wave(lamb, cext, cext_an, ylim_s, ylim_e, xpoints, title=None, 
                    file_name=None, file_ext=None):

    rcParams['font.family'] = 'serif'
    rcParams['font.size'] = 14
    rcParams['xtick.top'] = True
    rcParams['ytick.right'] = True
    rcParams['axes.linewidth'] = 2
    
    pyplot.figure(figsize=(9,6))

    pyplot.plot(lamb, cext, ls='', marker='o', color='0.4', mew=1.5, mfc='w', ms=7, label='PyGBe')
    pyplot.plot(lamb, cext_an, ls='--', marker='None',  c='k', lw=1.5, label='Analytical')


    pyplot.xlabel('Wavelength [nm]')
    pyplot.ylabel('Extinction cross section [$nm^2$]')
    pyplot.xlim(min(lamb), max(lamb))
    pyplot.ylim(ylim_s, ylim_e)

    pyplot.xticks(numpy.linspace(min(lamb), max(lamb), xpoints), rotation=25)
    pyplot.tick_params(axis='both', length=8, width=1, direction='in')
    
    if title:
        pyplot.title(title)
    
    pyplot.legend(loc='best')
    pyplot.grid(linestyle=':')

    if file_name and file_ext:
        pyplot.savefig(file_name+'.'+file_ext, format=file_ext, dpi=80, 
                        bbox_inches='tight', pad_inches=0.1)

