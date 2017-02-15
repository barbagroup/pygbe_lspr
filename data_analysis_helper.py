import numpy 
from matplotlib import pyplot
from scipy.interpolate import interp1d, splev, splrep


def linear_interp(lamb, n, k):
    '''Returns the linear interpolation of the real and imaginary refractive index.
    
    Arguments:
    ----------
    lamb: array, wavelengths.
    n   : array, real part of refractive index. 
    k   : array, imaginary part of refractive index.
    
    Returns:
    --------
    real_inter: function, interpolated function of the real part of the refrac index.
    imag_inter: function, interpolated function of the imaginary part the refrac index.
    
    '''
    real_inter = interp1d(lamb, n)
    imag_inter = interp1d(lamb, k)
    
    return real_inter, imag_inter


def spline(lamb, n, k):
    '''Returns the B-spline representations of the real and imaginary refractive index.
    
    Arguments:
    ----------
    lamb: array, wavelengths.
    n   : array, real part of refractive index. 
    k   : array, imaginary part of refractive index.
    
    Returns:
    --------
    real_tuple: tuple, vector of knots, spline coefficients, and the degree of the spline
                of the real part of the refrac index.
    imag_tuple: tuple, vector of knots, spline coefficients, and the degree of the spline
                of the imaginary part of the refrac index.
    '''
    
    real_tuple = splrep(lamb, n)
    imag_tuple = splrep(lamb, k)
    
    return real_tuple, imag_tuple


def spline_eval(x, real_tuple, imag_tuple): 
    '''Evaluates the B-splines of the real and imaginary refractive index.
    
    Arguments:
    ----------
    x         : array,  points at which to return the value of the spline.
    real_tuple: tuple, vector of knots, spline coefficients, and the degree of the spline
                of the real part of the refrac index.
    imag_tuple: tuple, vector of knots, spline coefficients, and the degree of the spline
                of the imaginary part of the refrac index.
    
    
    Returns:
    --------    
    real_spline: array, values representing the spline function evaluated at the points in
                 x for real refractive index.
    imag_spline: array, values representing the spline function evaluated at the points in
                 x for real refractive index.    
    '''
    
    real_spline = splev(x, real_tuple)
    imag_spline = splev(x, imag_tuple)
    
    return real_spline, imag_spline

def plot_refrac(lamb, n, k):    
    """
    Plots the refractive index vs wavelength.
    Plots separately the real and imaginary part of the refractive index.
    
    Arguments:
    ----------
    lamb: array, wavelengths.
    n   : array, real part of refractive index. 
    k   : array, imaginary part of refractive index.
    
    Returns:
    --------
    Plots of refrac_index_real vs lambda, refrac_index_imaginary vs lambda. 
    """
    
    pyplot.figure(figsize=(12,4))  

    pyplot.subplot(121)
    
    pyplot.scatter(lamb,n, color='#2929a3') 
    
    pyplot.xlabel('Wavelength [nm]')
    pyplot.ylabel('Refractive index')
    pyplot.xlim(min(lamb)-5, max(lamb)+5)
    pyplot.xticks(numpy.linspace(min(lamb), max(lamb), 10), rotation=25)
    pyplot.title('Real')
    pyplot.grid()
    
    
    pyplot.subplot(122)
    
    pyplot.scatter(lamb,k, color='#ff5733') 
    
    pyplot.xlabel('Wavelength [nm]')
    #pyplot.ylabel('Refractive index')
    pyplot.xlim(min(lamb)-5, max(lamb)+5)
    pyplot.xticks(numpy.linspace(min(lamb), max(lamb), 10), rotation=25)
    pyplot.title('Imaginary')
    pyplot.grid()

def plot_interpolation(lamb, n, k, lamb_x, real_linear, imag_linear, real_spline, imag_spline):
    '''Plots data, linear interpolation and spline of the real and imaginary refractive index
    
    Arguments:
    ----------    
    lamb       : array, wavelengths.
    n          : array, real part of refractive index. 
    k          : array, imaginary part of refractive index.
    lamb_x     : array,  points at which to return the value of the spline
    real_linear: function, interpolated function of the real part of the refrac index.
    imag_linear: function, interpolated function of the imaginary part the refrac index.
    real_spline: array, values representing the spline function evaluated at the points in
                 x for real refractive index.
    imag_spline: array, values representing the spline function evaluated at the points in
                 x for real refractive index.        
    '''
    
    pyplot.figure(figsize=(12,12))  

    #Real refrac index
    pyplot.subplot(211)
    #data
    pyplot.scatter(lamb, n, color='#2929a3', alpha = 0.8, label = 'data')
    #linear interp
    pyplot.plot(lamb_x, real_linear(lamb_x), color = 'r', ls = '-', label = 'linear')
    #spline interp
    pyplot.plot(lamb_x, real_spline, color = 'g', ls = '--', label = 'spline')
    
    pyplot.xlim(min(lamb)-5, max(lamb)+5)
    pyplot.xticks(numpy.linspace(min(lamb), max(lamb), 20), rotation=25)
    pyplot.title('Real')
    pyplot.ylabel('Refractive index')
    pyplot.legend(loc='best')
    pyplot.grid()
    
    #Imaginary refrac index
    pyplot.subplot(212)
    #data
    pyplot.scatter(lamb, k, color='#2929a3', alpha = 0.8, label = 'data') 
    #linear interp
    pyplot.plot(lamb_x, imag_linear(lamb_x), color = 'r', ls = '-', label = 'linear')
    #spline interp
    pyplot.plot(lamb_x, imag_spline, color = 'g', ls = '--', label = 'spline')
    
    pyplot.xlim(min(lamb)-5, max(lamb)+5)
    pyplot.xticks(numpy.linspace(min(lamb), max(lamb), 20), rotation=25)
    pyplot.title('Imaginary')
    pyplot.ylabel('Refractive index')
    pyplot.xlabel('Wavelength [nm]')
    pyplot.legend(loc='best')
    pyplot.grid()
    
