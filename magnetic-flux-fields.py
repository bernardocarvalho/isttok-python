#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    "rho, z0 coordinates of current ring (I=1A)"
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

if __name__ == "__main__":
    #ISTTOK
    #
    rm = 0.085 #Minor radius
    RM = 0.46   # Major radius
    Rprb = 0.0935  #Raio do centro às mirnov  9.35  
    #Vertical Coils: 4 coils, 5 turns, R1,2=58 [cm],R2,3=35 [cm],z=±7 [cm]
    #Horizontal Coils: 2 coils , 4 turns, R1,2=58 [cm],z=±7[cm]
    #
    n = 12     # number of probes
    angles_pbr = np.array([(23./24 - i/n)*2*np.pi for i in range(n)])
    #angles_pbr = np.array([(23./24 - i/n)*2*np.pi for i in range(n)])/np.pi*180.0
    Rprb =RM + Rprb * np.cos(angles_pbr)
    zprb =Rprb * np.sin(angles_pbr)
    
    a=Aphi(0.46, 0.0, 0.2, 0)
    b=Bzloop(0.46, .1)
    b=Bzloop(0.46, .1)
#    br,bz=Bloop(0.46, 0.0, 1e-8, .1)
    
    br,bz=Bloop(RM, 0.0, Rprb, zprb)
#    br
#    bz
#    br*bz
    bpol=bz* np.cos(angles_pbr) - br* np.sin(angles_pbr)
    brad=bz* np.sin(angles_pbr) + br* np.cos(angles_pbr)
    bpol * 1e7
    brad * 1e7
    #plt.plot(angles_pbr, bz, angles_pbr, br)
