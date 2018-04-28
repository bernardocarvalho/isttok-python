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


if __name__ == "__main__":
    np.set_printoptions(precision=3)
    nc = 6 # number of copper shell 'wires'
    ns = 1 # number of active coils
    ResCopper = 1.0e-4 # 1 mOhm
    aCopper = 10.0e-3  # 'wire' radius 10 mm
    
    # mutual inductance matrices between the elements of the passive structure
    Mcc=np.zeros((nc,nc))
    # mutual inductance matrices of the elements of the passive structure 
    # and active coils
    Mcs=np.zeros((nc,ns))
    # diagonal resistance matrix Rc
    Rc = np.diag([1.0e-4, 0.5e-4, 1.0e-4, 1.0e-4, 1.0e-4, 1.0e-4])

    # Copper 'wires' positions
    anglesIc = np.array([(i/nc)*2*np.pi for i in range(nc)])
    RIc = mf.ISTTOK['RM'] + mf.ISTTOK['Rcopper']  * np.cos(anglesIc)
    ZIc = mf.ISTTOK['Rcopper']  * np.sin(anglesIc)
    #Vertical Coils: 4 coils, 5 turns, R1,2=58 [cm],R2,3=35 [cm],z=±7 [cm]
    Rver =[0.58, 0.58, 0.35, 0.35]
    Zver =[0.07, -0.07, 0.07, -0.07]
    VerTurns=[-5., -5., 5., 5.]
    #Horizontal Coils: 2 coils , 4 turns, R1,2=58 [cm],z=±7[cm]
    Rhor =[0.58, 0.58,]
    Zhor =[0.07, -0.07]
    HorTurns=[4., -4.]

    #RIc = ISTTOK['Rcopper'] * np.ones(nc) # Major radius of shell 'wires' 
    for i in range(nc):
        Mcc[i,i] = mf.selfLoop(RIc[i], aCopper)
        for j in range(i+1, nc):
            Mcc[i,j] = mf.mutualL(RIc[i], ZIc[i],RIc[j], ZIc[j])
            Mcc[j,i] = Mcc[i,j]
    for i in range(nc):
        Mcs[i,:] =0.0
        for k in range(len(VerTurns)):
            Mcs[i,0] += VerTurns[k] * mf.mutualL(Rver[k], Zver[k], RIc[i], ZIc[i])           
#        for k in range(len(HorTurns)):
#            Mcs[i,1] += HorTurns[k] * mf.mutualL(Rhor[k], Zhor[k], RIc[i], ZIc[i]) 
    
    # Poloidal field for I=1A in the ith copper 'wire'
    Bpolc=np.zeros((nc, mf.ISTTOK['n_pbrs'])) 
    #br,bz=mf.Bloop(RIc[0], ZIc[0], mf.ISTTOK['Rprb'], mf.ISTTOK['Rprb'])
    #bpol, brad = mf.BpolBrad(br,bz, mf.ISTTOK['angles_pbr'])
    for i in range(nc):
        br,bz=mf.Bloop(RIc[i], ZIc[i], mf.ISTTOK['Rprb'], mf.ISTTOK['Rprb'])
        bpol, brad = mf.BpolBrad(br,bz, mf.ISTTOK['angles_pbr'])
        Bpolc[i,:] = bpol 
    
    #https://apmonitor.com/pdc/index.php/Main/ModelSimulation
    # Model 
    invMcc = np.linalg.inv(Mcc)
    A = -np.matmul(Rc,invMcc)
    Bs = -np.matmul(A,Mcs)
    C = invMcc
    Ds =-np.matmul(invMcc,Mcs)
    
    sys = signal.StateSpace(A,Bs,C,Ds)
    t,ic = signal.step(sys)
    
    # Stability
    w, vect = np.linalg.eig(A)
    # Eigenvalues should all be negative
    print(w)
    
    BR = 0.0 
    BZ = 0.0
    for i in range(len(Turns)):
        br,bz=Bloop(Rver[i], Zver[i], Rprb, zprb)
        BR += Turns[i]*br
        BZ += Turns[i]*bz 

#    plt.plot(t2,y2,'g:',linewidth=2,label='State Space')
    lineObjects = plt.plot(t,ic,linewidth=1)

    plt.xlabel('Time')
    plt.ylabel('Response (y)')
    plt.legend(lineObjects, ['ic0', 'ic1', 'ic2','ic3', 'ic4', 'ic5'],loc='best')
    plt.show()

            


 