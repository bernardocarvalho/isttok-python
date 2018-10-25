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
#    np.set_printoptions(precision=3)
from scipy import signal
import matplotlib.pyplot as plt
#import scipy as scp
#import scipy.constants as cnst

import magnetic_flux_fields as mf
# ISTTOK Geometric parameters 
from isttok_magnetics import isttok_mag

from getMirnov import FsamplingMARTe

def buildLtiModel(RIc, ZIc):
    """
    Build LTI system state model for a asissymetric Tokamak with passive conductors
    # State variable: Psi_c (Pol Flux at the eddy current positions)
    # SS Model: dot(Psi_c) = A * Psi_c + [Bpl  Bs] [ip, is]
    #                   ic = C * Psi_c + [Dpl  Ds] [ipl, is]
    # Dpl, DPl not yet calculates
    #
    #https://apmonitor.com/pdc/index.php/Main/ModelSimulation

    Args:
#        nc: number of passive copper shell filaments
        ns: number of PFC active coils (sources)
        RIc, ZIc: arrays with position of passive conductors
        
    Returns:
    """

    ResCopper = 1.0e-4 # 0.1 mOhm
    aCopper = 10.0e-3  # 'wire' radius 10 mm
    ns = 2 # number of active coil circuits
    nc= len(RIc) 
     
    # mutual inductance matrices between the elements of the passive structure
    Mcc=np.zeros((nc,nc))
    
    # mutual inductance matrices of the elements of the passive structure 
    # and active coils
    Mcs=np.zeros((nc,ns))
    # diagonal Resistance matrix Rc
#    Rc = np.diag([1.0e-4, 0.5e-4, 1.0e-4, 1.0e-4, 1.0e-4, 1.0e-4])
#    Rc = np.diag([1.0e-4, 0.5e-4, 1.0e-4, 1.5e-4, 1.0e-4, 0.6e-4])
    Rc = np.diag([1.0, 0.5, 1.0, 1.5, 1.0, 0.6]) * ResCopper

    #RIc = ISTTOK['Rcopper'] * np.ones(nc) # Major radius of shell 'wires' 
    for i in range(nc):
        Mcc[i,i] = mf.selfLoop(RIc[i], aCopper)
        for j in range(i+1, nc):
            Mcc[i,j] = mf.mutualL(RIc[i], ZIc[i],RIc[j], ZIc[j])
            Mcc[j,i] = Mcc[i,j]
            
    for i in range(ns):
#        Mcs[i,:] =0.0
        for k in range(len(isttok_mag['TurnsPfcVer'])):
            Mcs[i,0] += isttok_mag['TurnsPfcVer'][k] * mf.mutualL(isttok_mag['RPfcVer'][k], isttok_mag['ZPfcVer'][k], RIc[i], ZIc[i])           
#        for k in range(len(HorTurns)):
#            Mcs[i,1] += HorTurns[k] * mf.mutualL(Rhor[k], Zhor[k], RIc[i], ZIc[i]) 

    # Model dot(Psi_c) = A * Psi_c + [Bp + Bpfc] [ip; ipfc]
    # ic = C * Psi_c + [Dp + Dpfc] [ip; ipfc]
    # State variable Psi_c (Pol Flux at the eddy current positions)
    #
    invMcc = np.linalg.inv(Mcc)
    A = -np.matmul(Rc,invMcc)
    Bs = -np.matmul(A,Mcs)
    C = invMcc
    Ds =-np.matmul(invMcc,Mcs)

    return A, Bs, C, Ds  


def buildIs2Bpol():
    """
    Build B poloidal response Matrix on the poloidal field probes from a set of 
    PFC coil circuits (Vertical + Horizontal)
    Gives poloidal field on each probe for a Is=1A on coils    
    #

    Args:
        
    Returns: 
        Is2Bpol :
    """
    ns = 2 # number of PFC active independent coils circuits (sources)
#       number of poloidal probes
    nPrb = isttok_mag['nPrb']
    
    Rprb = isttok_mag['Rprb']
    Zprb = isttok_mag['Zprb']
    tethaProb = isttok_mag['tethaPrb']
    
    turnsV  = isttok_mag['TurnsPfcVer']
    RPfcVer = isttok_mag['RPfcVer']
    ZPfcVer = isttok_mag['ZPfcVer']
    
    turnsH  = isttok_mag['TurnsPfcHor']
    RPfcHor = isttok_mag['RPfcHor']
    ZPfcHor = isttok_mag['ZPfcHor']
    
    Is2Bpol=np.zeros((nPrb, ns))
#    Vertical Coils
    for k in range(len(turnsV)):
        br,bz= mf.Bloop(RPfcVer[k], ZPfcVer[k], Rprb, Zprb)
        bpol, brad = mf.BpolBrad(br,bz, tethaProb)
        Is2Bpol[:,0] += turnsV[k] * bpol

#    Horizontal Coils
    for k in range(len(turnsH)):
        br,bz= mf.Bloop(RPfcHor[k], ZPfcHor[k], Rprb, Zprb)
        bpol, brad = mf.BpolBrad(br,bz, tethaProb)
        Is2Bpol[:,1] += turnsH[k] * bpol

    return Is2Bpol


def buildIs2BpolA(Vcoil,Hcoil=None,PrimCoil=None):
    """
    Build B poloidal response Matrix on the poloidal field probes from a set of 
    PFC coil circuits (Vertical + Horizontal)
    Gives poloidal field on each probe for a Is=1A on coils    
    #

    Args:
        Vcoil: numpy.array([RPfcVer,ZPfcVer,TurnsPfcVer])
        
    Returns: 
        Is2Bpol :
    """
    ns = 2 # number of PFC active independent coils circuits (sources)
#       number of poloidal probes
    nPrb = isttok_mag['nPrb']    
        
    Rprb = isttok_mag['Rprb']
    Zprb = isttok_mag['Zprb']
    tethaProb = isttok_mag['tethaPrb']

    Is2Bpol=np.zeros((nPrb, ns))

#    Vertical Coils
    for k in range(Vcoil.shape[0]):
        br,bz= mf.Bloop(Vcoil[k,0], Vcoil[k,1], Rprb, Zprb)
        bpol, brad = mf.BpolBrad(br,bz, tethaProb)
        Is2Bpol[:,0] += Vcoil[k,2] * bpol
    
    #if Hcoil != None :    

#    Horizontal Coils
    return Is2Bpol

def buildIc2Bpol(RIc, ZIc):
    """
    Build B poloidal response Matrix on the poloidal field probes from a set of filaments
    Gives poloidal field on each probe for a Is=1A on filament
    #

    Args:
#        np: number of poloidal probes
#        ns: number of PFC active coils (sources)
        
    Returns: 
        MsBpol :
    """
    nc   = len(RIc) 
    nPrb = isttok_mag['nPrb']
    
    Rprb = isttok_mag['Rprb']
    Zprb = isttok_mag['Zprb']
    tethaProb = isttok_mag['tethaPrb']
   
    Ic2Bpol=np.zeros((nPrb, nc))
#    each filamen
    for k in range(len(RIc)):
        br,bz= mf.Bloop(RIc[k], ZIc[k], Rprb, Zprb)
        bpol, brad = mf.BpolBrad(br,bz, tethaProb)
        Ic2Bpol[:,0] +=  bpol

    return Ic2Bpol

#        br,bz=Bloop(Rver[i], Zver[i], Rprb, zprb)
#        BR += Turns[i]*br
#        BZ += Turns[i]*bz 

if __name__ == "__main__":
 Vcl1=np.array([
       [ 0.60,  0.08, -1.  ],
       [ 0.59,  0.07, -1.  ],
       [ 0.58,  0.07, -1.  ],
       [ 0.59,  0.07, -1.  ],
       [ 0.60,  0.08, -1.  ],

       [ 0.58, -0.07, -5.  ],
       [ 0.35,  0.07,  5.  ],
       [ 0.35, -0.07,  5.  ]])
    np.set_printoptions(precision=3)
    nc = 6 # number of copper shell 'wires'
#    ns = 1 # number of active coils
    ResCopper = 1.0e-4 # 0.1 mOhm
    aCopper = 10.0e-3  # 'wire' radius 10 mm
    
    Is2Bpol=buildIs2Bpol()
    
    # make heaviside current signal
    Imax = 400 #A
    n1=np.int(0.2*FsamplingMARTe)
    n2=np.int((0.6 -0.2 )*FsamplingMARTe)
    n3=np.int((1.0 -0.6 )*FsamplingMARTe)
    currVert = np.concatenate([np.zeros(n1,), Imax*np.ones(n2,), np.zeros(n3,)])
    currHor=np.zeros_like(currVert) # Zero current on Hori Field Coils
    IsPfc = np.array([currVert, currHor])
    
        # Copper passive 'filament ' positions
    anglesIc = np.array([(i/nc)*2*np.pi for i in range(nc)])
    RIc = isttok_mag['RM'] + isttok_mag['Rcopper']  * np.cos(anglesIc)
    ZIc = isttok_mag['Rcopper']  * np.sin(anglesIc)


    A,Bs,C,Ds = buildLtiModel(RIc, ZIc) 

    Ic2Bpol=buildIc2Bpol(RIc, ZIc)

   
    magSys = signal.StateSpace(A,Bs,C,Ds)
    #t,ic = signal.step(magSys)
    
    # Stability
    w, vect = np.linalg.eig(A)
    # Eigenvalues should all be negative
    print('LTI system Eigenvalues:')
    print(w)
    
    bPolIs=np.matmul(Is2Bpol,IsPfc)
    time = np.arange(IsPfc.shape[1]) / FsamplingMARTe
    fig, ax = plt.subplots()
    #plt.figure()
    #
    linesBpol = ax.plot(time, bPolIs.T)
#    lines = ax.plot(time, bPolIs.T, label= ['ic0', 'ic1', 'ic2','ic3', 'ic4', 'ic5'])
    ax.legend(linesBpol, ['m0', 'm1', 'm2','m3', 'm4', 'm5','m6', \
                             'm7', 'm8','m9', 'm10', 'm11'],loc='right')
    
    ax.set_xlabel('Time/s')
    #ax.legend()
    plt.show()

    
    # scipy.signal.lsim(system, U, T, X0=None, interp=True)
    #  U: If there are multiple inputs, then each column of the rank-2 array represents an input.
    tout, Ic, x = signal.lsim(magSys,IsPfc.T, time)

#    fig, ax = plt.subplots()
#    linesIc = ax.plot(time, Ic)
#    ax.legend(linesIc, ['ic0', 'ic1', 'ic2','ic3', 'ic4', 'ic5'], loc='best')
# #   lineIsv = ax.plot(time, IsPfc[0,:])
#    ax.set_xlabel('Time/s')
#    plt.show()
#
    bPolIc=np.matmul(Ic2Bpol,Ic.T)

    bPolTot = bPolIs.T +  bPolIc.T
    fig, ax = plt.subplots()
    linesBpol = ax.plot(time, bPolTot)
    ax.legend(linesBpol, ['m0', 'm1', 'm2','m3', 'm4', 'm5','m6', \
                             'm7', 'm8','m9', 'm10', 'm11'],loc='right')
    ax.set_title('Probe response')
    
    ax.set_xlabel('Time/s')
    #ax.legend()
    plt.show()


    #bPolIc=np.matmul(Is2Bpol,IsPfc)
#    BR = 0.0 
#    BZ = 0.0
#    for c in range(len(isttok_mag['RPfcVer'])):
#        br,bz=mf.Bloop(isttok_mag['RPfcVer'][c], isttok_mag['ZPfcVer'][c], isttok_mag['Rprb'], isttok_mag['Zprb'])
#        BR += isttok_mag['TurnsPfcVer'][c]*br
#        BZ += isttok_mag['TurnsPfcVer'][c]*bz 

#    plt.figure()
##    plt.plot(t2,y2,'g:',linewidth=2,label='State Space')
#    lineObjects = plt.plot(t,ic,linewidth=1)
#    plt.xlabel('Time/s')
#    plt.ylabel('Response ((ic) /A ')
#    plt.legend(lineObjects, ['ic0', 'ic1', 'ic2','ic3', 'ic4', 'ic5'],loc='best')
#    plt.show()
    
#    plt.figure()
#    #
#    lineObjs = plt.plot(t,np.matmul(ic,Bpolc) )
#    plt.xlabel('Time/s')
#    plt.ylabel('Bpol ')
#    plt.legend(lineObjs, ['m0', 'm1', 'm2','m3', 'm4', 'm5','m6', \
#                             'm7', 'm8','m9', 'm10', 'm11'],loc='right')
#    plt.show()
        

            


 