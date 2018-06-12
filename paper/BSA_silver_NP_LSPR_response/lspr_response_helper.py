'''This file contains functions that help to analyze LSPR response to BSA data, 
and to report and plot the main findings.
'''

import numpy
from matplotlib import pyplot, rcParams
import os


def plot_cext_wave_distance(wavelength, cext, linestyles, colors,
                             labels, file_name=None, file_ext=None, paper=False):
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

    if paper:
        file_ext = 'pdf'
        pyplot.switch_backend('agg')
        fig = pyplot.figure(figsize=(3, 2))
        lw = 1
        fs = 10
        fsl = 8
        hl = 0.1
        p = 6
    else:
        fig = pyplot.figure(figsize=(6, 4))
        lw = 2
        fs = 12
        fsl = 10
        hl = 0.5
        p = 11

    rcParams['font.family'] = 'serif'
    rcParams['font.size'] = fs
    rcParams['xtick.top'] = True
    rcParams['ytick.right'] = True
    rcParams['axes.linewidth'] = 1
    
    ax = fig.add_subplot(1,1,1)

    major_yticks = numpy.linspace(2300, 4300, 5)
    minor_yticks = numpy.linspace(2550, 4050, 4)

    ax.set_yticks(major_yticks)                                                       
    ax.set_yticks(minor_yticks, minor=True)

    #pyplot.yticks(numpy.linspace(2300, 4300, 5))

    pyplot.tick_params(axis='both', length=5, width=0.8,which='major', direction='in')
    pyplot.tick_params(axis='both', length=2.5, width=0.8, which='minor', direction='in')


    pyplot.xlabel('Wavelength [nm]')
    pyplot.ylabel('$C_{ext}$ [$nm^2$]')
    pyplot.xlim(382,387)
    pyplot.ylim(2300, 4300)

    #pyplot.title('LSPR response \n')
    
    for i in range(len(wavelength)):
        pts = p
        pyplot.xticks(numpy.linspace(min(wavelength[i]), max(wavelength[i]), pts),
                     rotation=25)

        pyplot.plot(wavelength[i], cext[i], linestyle=linestyles[i], 
                   color=colors[i], linewidth=lw, label=labels[i])
    
    pyplot.legend(loc='upper right', fontsize=fsl, numpoints=1, handlelength=hl).get_frame().set_lw(0.2)
    pyplot.grid(linestyle=':', which='minor')
    pyplot.grid(linestyle=':', which='major')


    if file_name and file_ext:
        pyplot.savefig(file_name+'.'+file_ext, format=file_ext, dpi=80, 
                        bbox_inches='tight', pad_inches=0.04)

    if paper :
        pyplot.close(fig)

def report(sensor_file, bsa_file, file_name=None, file_ext=None, paper=False):
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
                             labels, file_name, file_ext, paper=paper)
    
    if not paper:
        lab = ['d=infty', 'd=1 nm']
        lst = list(zip(cext_d1_00, lab))
        for i in range(len(lst)):
            c, l = lst[i]
            idx = numpy.where(c==max(c))
            print('Cext max at {} is {:.2f} and it occurs at a wavelength of {}'.format(l, 
                    max(c), w_d1_00[idx][0]/10))

def check_file_exists(f_name, f_ext):
    ''' Checks if png image of extinction cross section exists
    '''
    if os.path.exists(f_name+'.'+f_ext):
        file_ext = None
        file_name = None
        print('Plot already exists! If you want to generate it '
            'again, please delete the existing one.')
    else:
        file_ext=f_ext
        file_name = f_name

    return file_ext, file_name