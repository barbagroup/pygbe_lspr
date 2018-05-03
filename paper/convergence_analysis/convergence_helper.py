'''This file contains functions that help to analyze and plot data related
to the convergence analysis.
'''

import numpy
import pickle
from matplotlib import pyplot, rcParams

def pickleload(pickle_file):
    '''Loads a pickle file and assins it to a variable.
    '''
    with open(pickle_file, 'rb') as f:
        dict_res = pickle.load(f)
    return dict_res

def ord_convergence(array, rate):
    '''Computes the order of convergence given 3 scalar outputs of 3 different
    mesh refinments, saved in an array. The rate is how much the mesh is
    refined. In our case is 4.
    '''

    ord_conv = numpy.log((array[-3] - array[-2])/(array[-2] - array[-1]))/numpy.log(rate)

    return ord_conv

def richardson_extrapolation(array):
    '''Performs an estimate of the exact solution using Richardson 
       extrapolation, given by

    f_ex = (f_1 * f_3 - f_2^2) / (f_3 - 2*f_2+f_1)

    where f_1 is a result from the finest grid and f_3 is from the coarsest.
    The grids f_1, f_2, f_3 should have the same refinement ratio (e.g. 4 -> 8 -> 16)

    Arguments:
    ----------
    array: contains C_ext values of the sensor for the different meshes.

    Returns:
    --------
    f_ex : float, richardson_extrapolation estimated exact solution.  
   '''
    
    f1 = array[-1] 
    f2 = array[-2]
    f3 = array[-3]

    f_ex = (f1 * f3 - f2**2) / (f3 - 2 * f2 + f1)

    return f_ex 


def perc_error(Cext, rich_ext):
    '''Computes the relative and percentage error respect to the richardson
     extrapolation of a scalar quantity, in this case the different meshes 
     values for the extinction cross section of the sensor. 
    
    Arguments:
    ----------
    Cext: array, extinction cross section values of the sensor for the 
    different meshes.
    rich_ext: float, richardson_extrapolation estimated exact solution.
    
    Returns:
    --------
    rel_err :array, relative error values respect to the richardson
    extrapolation. 
    perc_err: array, percentage error values respect to the richardson
    extrapolation.  
    '''
    
    rel_err = abs((Cext - rich_ext)/rich_ext)
    perc_err = rel_err*100
    
    return rel_err, perc_err

def plot_sph_complex_convergence(N, error, file_name=None, file_ext=None):
    pyplot.figure(figsize=(8,5))

    rcParams['font.family'] = 'serif'
    rcParams['font.size'] = 14
    rcParams['xtick.top'] = True
    rcParams['ytick.right'] = True
    rcParams['axes.linewidth'] = 2

    asymp = N[-3]*error[-3]/N

    pyplot.loglog(N, error, ls='',marker='o', c='k', mew=1.5, mfc='w', ms=10, label='BSA_sensor')
    pyplot.loglog(N, asymp, c='k', marker='None', ls=':', lw=2, label=None)


    loc = (3*N[-2]+N[-1])/4

    tex_loc = numpy.array((loc,N[-3]*error[-3]/loc))

    
    pyplot.text(tex_loc[0], tex_loc[1],'N$^{-1}$', fontsize=12,
                rotation=-35,rotation_mode='anchor')
    
    pyplot.xlabel('N')
    pyplot.ylabel('Relative error')
    pyplot.tick_params(axis='both', length=10, width=1, which='major', direction='in')
    pyplot.tick_params(axis='both', length=5, width=1, which='minor', direction='in')
    pyplot.ylim(1e-3,1)
    pyplot.xlim(1e2,1e5)
    pyplot.legend(loc='best')
    pyplot.grid(True, which="both")
    
    if (file_name and file_ext):
        pyplot.savefig(file_name+'.'+file_ext, format=file_ext, dpi=80, bbox_inches='tight', pad_inches=0.1)



