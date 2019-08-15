#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 13 August 2019

@author: Curro Rodriguez Montero, School of Physics and Astronomy,
            University of Edinburgh, JCMB, King's Buildings

This codes obtains the equivalent width for a set of particular lines from the galactic spectra output
of the pyloser code.

For questions about the code:
s1650043@ed.ac.uk
"""
# Import necessary libraries
import numpy as np 
import h5py
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="white")

MODEL = sys.argv[1]
WIND = sys.argv[2]
SNAP = int(sys.argv[3])
GALAXY = [int(sys.argv[4])]

def EW_hdelta(flux,waves):
    hd_window = np.array([4088,4116]) # in Angstroms, as given by Balogh et al. (1999)
    ind_start = np.argmin(abs(waves-hd_window[0]))
    ind_end = np.argmin(abs(waves-hd_window[1]))
    f = flux[ind_start:ind_end+1]
    w = waves[ind_start:ind_end+1]
    w_p = np.array([w[0],w[-1]])
    f_p = np.array([f[0],f[-1]])
    f_0 = np.interp(w,w_p,f_p)
    d = abs(w[1] - w[0])
    W = np.sum((1-f/f_0)*d)
    return W, w_p

def plot_spectra(flux,waves,gal,snap):
    # Just do a simple spectra plot for the input of flux and wavelenghts given.
    fig = plt.figure(num=None, figsize=(8, 5), dpi=80, facecolor='w', edgecolor='k')
    ax = fig.add_subplot(1,1,1)
    ax.plot(waves,flux,'k-')
    W, w_p = EW_hdelta(flux,waves)
    ax.text(0.5,0.9,r'EW(H$_{\delta}$) = '+'{:.2}'.format(W)+'$\AA$',transform=ax.transAxes)
    ax.axvspan(w_p[0],w_p[1],alpha=0.6)
    ax.set_xlabel(r'$\lambda [\AA$]', fontsize=16)
    ax.set_ylabel('Flux',fontsize=16)
    fig.tight_layout()
    fig.savefig('../color_plots/spectra_'+str(gal)+'_'+str(snap)+'.png',format='png', dpi=250, bbox_inches='tight')
def read_pyloser(model,wind,snap,gals):

    loser_file = '/home/rad/data/%s/%s/Groups/loser_%s_%03d.hdf5' % (model,wind,model,snap)
    f = h5py.File(loser_file,'r')
    wavelengths = np.asarray(f['myspec_wavelengths'][:])
    fluxes = np.zeros((len(gals),len(wavelengths)))
    for i in range(0,len(gals)):
        fluxes[i,:] = f['myspec'][int(gals[i]),:]
    return wavelengths,fluxes




wave,flux = read_pyloser(MODEL,WIND,SNAP,GALAXY)
plot_spectra(flux[0,:],wave,GALAXY[0],SNAP)