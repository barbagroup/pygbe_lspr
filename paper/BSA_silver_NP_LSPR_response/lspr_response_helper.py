'''This file contains functions that help to analyze LSPR response to BSA data, 
and to report and plot the main findings.
'''

import numpy
from matplotlib import pyplot, rcParams

def plot_cext_wave_distance(wavelength, cext, linestyles, colors,
                             labels, file_name=None, file_ext=None):
    '''Plots the cross extinction section as a function of wavelength for
    different values of distance at which the proteins are located.

  	Arguments:
    ----------
    wavelength: list of wavelength arrays for each distance case.
    cext      : list of cross extinction section arrays for each distance case.
    linestyles: list of linstyles we desire to use for each distance case.
    colors    : list of colors we desire to use for each distance case.
    labels    : list of labels we desire to use for each distance case.
	'''
    rcParams['font.family'] = 'serif'
    rcParams['font.size'] = 16
    rcParams['xtick.top'] = True
    rcParams['ytick.right'] = True
    rcParams['axes.linewidth'] = 2

    fig=pyplot.figure(figsize=(9,6))
    ax = fig.add_subplot(1,1,1)
    
    major_xticks = numpy.linspace(min(wavelength[0]), max(wavelength[0]), 11)
    minor_xticks = numpy.linspace(min(wavelength[0]), max(wavelength[0]), 21)


    ax.set_xticks(major_xticks)                                                       
    ax.set_xticks(minor_xticks, minor=True)

    pyplot.xticks(rotation=25)
    pyplot.tick_params(axis='both', length=5, width=1, which='major', direction='in')
    pyplot.tick_params(axis='both', length=2.5, width=1, which='minor', direction='in')

    pyplot.xlabel('Wavelength [nm]')
    pyplot.ylabel('Extinction cross section [$nm^2$]')
    pyplot.xlim(382,387)

    pyplot.grid(ls=':', which='minor', alpha=0.6)
    pyplot.grid(ls=':', which='major', alpha=0.8)
    pyplot.title('LSPR response to two BSA located at +/- 1nm z-axis \n')
    
    for i in range(len(wavelength)):
        pyplot.plot(wavelength[i], cext[i], linestyle=linestyles[i], 
                   color=colors[i], linewidth=2, label=labels[i])
    
    pyplot.legend(loc='best')

    if file_name and file_ext:
        fig.tight_layout()
        pyplot.savefig(file_name+'.'+file_ext, format=file_ext, dpi=80, 
                        bbox_inches='tight', pad_inches=0.1)

def report(sensor_file, bsa_file, file_name=None, file_ext=None):
    '''Reports plot of Cext vs wavelength of sensor by itself and when BSA are
       at a distance d of the sensor. 
       It also reports the wavelength at wich the maximum accurs in both cases. 
    '''
    w_d1_00 , Cext_d1_00 = numpy.loadtxt(sensor_file, unpack = True)
    w_d1_2p_00 , Cext_d1_2p_00 = numpy.loadtxt(bsa_file, unpack = True)
    
    wavelength_d1_2p_00 = [w_d1_00/10., w_d1_2p_00/10.]
    cext_d1_00 = [Cext_d1_00, Cext_d1_2p_00]
    linestyles = ['-', ':']
    colors = ['k', '0.6']
    labels = ['$d = \infty$', '$d=1 \,nm$']
    
    plot_cext_wave_distance(wavelength_d1_2p_00, cext_d1_00, linestyles, colors,
                             labels, file_name, file_ext)
    
    lab = ['d=infty', 'd=1 nm']
    lst = list(zip(cext_d1_00, lab))
    for i in range(len(lst)):
        c, l = lst[i]
        idx = numpy.where(c==max(c))
        print('Cext max at {} is {:.2f} and it occurs at a wavelength of {}'.format(l, 
                max(c), w_d1_00[idx][0]/10))
