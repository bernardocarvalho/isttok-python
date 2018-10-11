#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 14:21:42 2018

@author: bernardo
From
Model-Based Approach for Magnetic
Reconstruction in Axisymmetric
Nuclear Fusion Machines by Cenedese et al
"""

from __future__ import print_function

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
#import scipy as scp
#import scipy.constants as cnst

import magnetic_flux_fields as mf
from isttok_magnetics import isttok_mag


if __name__ == "__main__":
    np.set_printoptions(precision=3)
    nc = 6 # number of copper shell 'wires'
    ns = 1 # number of active coils
    ResCopper = 1.0e-4 # 0.1 mOhm
    aCopper = 10.0e-3  # 'wire' radius 10 mm
    
    # mutual inductance matrices between the elements of the passive structure
    Mcc=np.zeros((nc,nc))
    # mutual inductance matrices of the elements of the passive structure 
    # and active coils
    Mcs=np.zeros((nc,ns))
    # diagonal resistance matrix Rc
#    Rc = np.diag([1.0e-4, 0.5e-4, 1.0e-4, 1.0e-4, 1.0e-4, 1.0e-4])
#    Rc = np.diag([1.0e-4, 0.5e-4, 1.0e-4, 1.5e-4, 1.0e-4, 0.6e-4])
    Rc = np.diag([1.0, 0.5, 1.0, 1.5, 1.0, 0.6]) * ResCopper

    # Copper 'wires' positions
    anglesIc = np.array([(i/nc)*2*np.pi for i in range(nc)])
    RIc = isttok_mag['RM'] + isttok_mag['Rcopper']  * np.cos(anglesIc)
    ZIc = isttok_mag['Rcopper']  * np.sin(anglesIc)


    #RIc = ISTTOK['Rcopper'] * np.ones(nc) # Major radius of shell 'wires' 
    for i in range(nc):
        Mcc[i,i] = mf.selfLoop(RIc[i], aCopper)
        for j in range(i+1, nc):
            Mcc[i,j] = mf.mutualL(RIc[i], ZIc[i],RIc[j], ZIc[j])
            Mcc[j,i] = Mcc[i,j]
    for i in range(nc):
        Mcs[i,:] =0.0
        for k in range(len(isttok_mag['TurnsPfcVer'])):
            Mcs[i,0] += isttok_mag['TurnsPfcVer'][k] * mf.mutualL(isttok_mag['RPfcVer'][k], isttok_mag['ZPfcVer'][k], RIc[i], ZIc[i])           
#        for k in range(len(HorTurns)):
#            Mcs[i,1] += HorTurns[k] * mf.mutualL(Rhor[k], Zhor[k], RIc[i], ZIc[i]) 
    
    # Poloidal field for I=1A in the ith copper 'wire'
    Bpolc=np.zeros((nc, isttok_mag['n_pbrs'])) 
    #br,bz=mf.Bloop(RIc[0], ZIc[0], isttok_mag['Rprb'], isttok_mag['Rprb'])
    #bpol, brad = mf.BpolBrad(br,bz, isttok_mag['angles_pbr'])
    for i in range(nc):
        br,bz=mf.Bloop(RIc[i], ZIc[i], isttok_mag['Rprb'], isttok_mag['Zprb'])
        bpol, brad = mf.BpolBrad(br,bz, isttok_mag['angles_pbr'])
        Bpolc[i,:] = bpol 
    
    #https://apmonitor.com/pdc/index.php/Main/ModelSimulation
    # Model dot(Psi_c) = A * Psi_c + [Bp + Bpfc] [ip; ipfc]
    # ic = C * Psi_c + [Dp + Dpfc] [ip; ipfc]
    # State variable Psi_c (Pol Flux at the eddy current positions)
    #
    invMcc = np.linalg.inv(Mcc)
    A = -np.matmul(Rc,invMcc)
    Bs = -np.matmul(A,Mcs)
    C = invMcc
    Ds =-np.matmul(invMcc,Mcs)
    
    magSys = signal.StateSpace(A,Bs,C,Ds)
    t,ic = signal.step(magSys)
    
    # Stability
    w, vect = np.linalg.eig(A)
    # Eigenvalues should all be negative
    print('Eigenvalues:')
    print(w)
    
    BR = 0.0 
    BZ = 0.0
    for c in range(len(isttok_mag['RPfcVer'])):
        br,bz=mf.Bloop(isttok_mag['RPfcVer'][c], isttok_mag['ZPfcVer'][c], isttok_mag['Rprb'], isttok_mag['Zprb'])
        BR += isttok_mag['TurnsPfcVer'][c]*br
        BZ += isttok_mag['TurnsPfcVer'][c]*bz 

    plt.figure()
#    plt.plot(t2,y2,'g:',linewidth=2,label='State Space')
    lineObjects = plt.plot(t,ic,linewidth=1)
    plt.xlabel('Time/s')
    plt.ylabel('Response ((ic) /A ')
    plt.legend(lineObjects, ['ic0', 'ic1', 'ic2','ic3', 'ic4', 'ic5'],loc='best')
    plt.show()
    
    plt.figure()
    #
    lineObjs = plt.plot(t,np.matmul(ic,Bpolc) )
    plt.xlabel('Time/s')
    plt.ylabel('Bpol ')
    plt.legend(lineObjs, ['m0', 'm1', 'm2','m3', 'm4', 'm5','m6', \
                             'm7', 'm8','m9', 'm10', 'm11'],loc='right')
    plt.show()
        

            


 