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
                    file_name=None, file_ext=None, paper=False):

    if paper:
        file_ext = 'pdf'
        pyplot.switch_backend('agg')
        fig = pyplot.figure(figsize=(3, 2))
        ms = 5
        lw = 1
        fs = 10
        hl = 0.1
        fsl = 9
    else:
        pyplot.figure(figsize=(6, 4))
        ms = 7
        lw = 2
        fs = 12
        hl = 0.5
        fsl = 12

    rcParams['font.family'] = 'serif'
    rcParams['font.size'] = fs
    rcParams['xtick.top'] = True
    rcParams['ytick.right'] = True
    rcParams['axes.linewidth'] = 1
    

    pyplot.plot(lamb, cext, ls='', marker='o', color='0.5', mew=1, mfc='w', ms=ms, label='PyGBe')
    pyplot.plot(lamb, cext_an, ls='--', marker='None',  c='k', lw=lw, label='Analytical')


    pyplot.xlabel('Wavelength [nm]')
    pyplot.ylabel(' $C_{ext}$ [$nm^2$]')
    pyplot.xlim(min(lamb), max(lamb))
    pyplot.ylim(ylim_s, ylim_e)

    pyplot.xticks(numpy.linspace(min(lamb), max(lamb), xpoints), rotation=25)
    pyplot.yticks(numpy.linspace(0, 4000, 9))
    pyplot.tick_params(axis='both', length=5, width=0.8, direction='in')


    
    if title:
        pyplot.title(title)
    
    pyplot.legend(loc='upper right', fontsize=fsl, numpoints=1, handlelength=hl).get_frame().set_lw(0.2)
    pyplot.grid(linestyle=':')

    if file_name and file_ext:
        pyplot.savefig(file_name+'.'+file_ext, format=file_ext, dpi=80, 
                        bbox_inches='tight', pad_inches=0.04)
    if paper :
        pyplot.close(fig)


