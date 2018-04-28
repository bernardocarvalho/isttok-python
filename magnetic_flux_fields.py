#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# magnetic-flux-fields.py
"""
Computation of analytical values for magnetic caused by current rings in cylindrical coordinates (R,z,phi)
Axixsymetric

https://ntrs.nasa.gov/search.jsp?R=20010038494

"""

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import scipy as scp
import scipy.constants as cnst
#https://uiuc-cse.github.io/2014-01-30-cse/lessons/thw-scipy/tutorial.html
import scipy.special as spcl

def subs(a, z0, R, z):
    """

    """
    a2=a*a
    R2=R*R
    z2=np.square(z-z0)
    alpha2=a2 + R2 + z2 - 2.0 * a*R
    beta2 =a2 + R2 + z2 + 2.0 * a*R
    #k2=m
    k2 = 1.0 - alpha2/beta2
    C = cnst.mu_0 /np.pi
    
    return a2,R2,z2,alpha2,beta2,k2,C

def Aphi(a, z0, R, z):
    """
    rho, z0 coordinates of current ring (I=1A)
    Poloidal Flux Phi=2*pi*R*Aphi
    """
    a2,R2,z2,alpha2,beta2,k2,C = subs(a, z0, R, z)
    #   a2=a*a
    #   R2=R*R
    #   z2=np.square(z-z0)
    #   alpha2=a2 + R2 + z2 - 2.0 * a*R
    #   beta2 =a2 + R2 + z2 + 2.0 * a*R
    #   #k2=m
    #   k2 = 1.0 - alpha2/beta2
    #   C = cnst.mu_0 /np.pi
    #https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.ellipk.html
    Aphi= ((2 - k2) * spcl.ellipk(k2) - 2 * spcl.ellipe(k2)) / k2
    Aphi=  Aphi * 4 * a  / np.sqrt(beta2)
    Aphi=  Aphi * C / 4.0
    return Aphi

def Bloop(a, z0, R, z):
    "rho, z0 coordinates of current ring (I=1A)"
    a2,R2,z2,alpha2,beta2,k2,C = subs(a, z0, R, z)
    Bz=C / 2.0 / alpha2 / np.sqrt(beta2)
    BR=Bz*(z-z0)/R
    Bz=Bz*((a2 - R2 - z2) * spcl.ellipe(k2) + alpha2 * spcl.ellipk(k2))
    BR=BR*((a2 + R2 + z2) * spcl.ellipe(k2) - alpha2 * spcl.ellipk(k2))
    return BR, Bz

def BpolBrad(BR,BZ, angles):
    ""
    Bpol=BZ* np.cos(angles) - BR* np.sin(angles)
    Brad=BZ* np.sin(angles) + BR* np.cos(angles)
    return Bpol, Brad

def Bzloop(a, z):
    """
    Field on Axis of Current Loop  (I=1A)
    Checked against
    Bzloop(1, 0)    = 6.283185307179586e-07 T
    Bzloop(0.1, .1) = 2.221441469079183e-06
    http://hyperphysics.phy-astr.gsu.edu/hbase/magnetic/curloo.html

    """
    a2=a*a
    z2=z*z
    Bz = cnst.mu_0 /2.0 * a2 / (a2 + z2)**(3./2.)
    
    return Bz

def selfLoop(R, a, Y=0.5):
    """
    Self inductance of a wire loop 
    Y = 0 if the current flows in the wire surface, 
    Y = 1/2 when the current is homogeneous across the wire.
    Ring with radius R.
    Wire with circular cross section, radius a
    https://aemjournal.org/index.php/AEM/article/view/331/pdf
    checked agains https://www.eeweb.com/tools/loop-inductance (+/-)
    """
    Lc= cnst.mu_0 * R *(np.log(8.0*R/a) - 2 + Y/2) # + mu_0 * O(a^2/R)
    
    return Lc

def mutualL(a, z0, R, z):
    """
    Mutual inductance of two wire loops 
    a, z0 coordinates of current ring (I=1A)
    Poloidal Flux Phi=2*pi*Aphi
    """
    return 2*np.pi * R * Aphi(a, z0, R, z)

#ISTTOK
#
rm = 0.085 #Minor radius
RM = 0.46   # Major radius
Rmirn = 0.0935  #Raio do centro às mirnov  9.35  

n_pbrs = 12
angles_pbr = np.array([(23./24 - i/n_pbrs)*2*np.pi for i in range(n_pbrs)])

Rprb =RM + Rmirn * np.cos(angles_pbr)
zprb =Rmirn * np.sin(angles_pbr)

ISTTOK = {'RM': 0.46, 'rm': 0.085, 'Rmirn': 0.0935 , 'Rcopper': 0.105, 'n_pbrs':n_pbrs, \
          'angles_pbr':angles_pbr, 'Rprb':Rprb , 'zprb':zprb }

if __name__ == "__main__":
    #Vertical Coils: 4 coils, 5 turns, R1,2=58 [cm],R2,3=35 [cm],z=±7 [cm]
    #
    #n = 12     # number of probes
    #angles_pbr = np.array([(23./24 - i/n)*2*np.pi for i in range(n)])
    #angles_pbr = np.array([(23./24 - i/n)*2*np.pi for i in range(n)])/np.pi*180.0
    Rprb =ISTTOK['RM']+ ISTTOK['Rmirn'] * np.cos(angles_pbr)
    zprb =ISTTOK['Rmirn'] * np.sin(angles_pbr)
    
    a=Aphi(0.46, 0.0, 0.2, 0)
    b=Bzloop(0.46, .1)
    
#    br,bz=Bloop(0.46, 0.0, 1e-8, .1)
    #Wire loop in the center of vessel
    #Horizontal Coils: 2 coils , 4 turns, R1,2=58 [cm],z=±7[cm]
    # Rhor=0.58
    # Zhor =0.07

    #Horizontal Coils: 2 coils , 4 turns, R1,2=58 [cm],z=±7[cm]
    Rhor =[0.58, 0.58,]
    Zhor =[0.07, -0.07]
    HorTurns=[4., -4.]

    #Vertical Coils: 4 coils, 5 turns, R1,2=58 [cm],R2,3=35 [cm],z=±7 [cm]
    Rver =[0.58, 0.58, 0.35, 0.35]
    Zver =[0.07, -0.07, 0.07, -0.07]
    Turns=[-5., -5., 5., 5.]
    BR = 0.0 
    BZ = 0.0
    for i in range(len(Turns)):
        br,bz=Bloop(Rver[i], Zver[i], Rprb, zprb)
        BR += Turns[i]*br
        BZ += Turns[i]*bz 
        
        # mutual inductance matrices between the elements of the passive structure
    bpol, brad = BpolBrad(BR,BZ, angles_pbr)
    Bpols=bpol # Poloidal field for I=1A in the coil (Vert)
    
#     
    np.set_printoptions(precision=3)
    print('Bpoloidal:')
    print(bpol)
    print('Bradial:')
    print(brad)
    print('BR:')
    print(br)
    print('BZ:')
    print(bz)
    
    #bpol * 1e7
    #brad * 1e7
    plt.figure() 
    
    #plt.axes([0.025, 0.025, 0.95, 0.95])
    plt.quiver(Rprb,zprb,BR,BZ)
    plt.xlim((0.36, 0.56  ))
    plt.axis('equal')
    #plt.ylim((-0.2, 0.2 ))
    plt.show()
    
    #plt.plot(angles_pbr, bz, angles_pbr, br)
