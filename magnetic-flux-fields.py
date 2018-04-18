#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Computation of analytical values for magnetic caused by current rings in cylindrical coordinates (R,z,phi)
Axixsymetric 

https://ntrs.nasa.gov/search.jsp?R=20010038494

"""

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


def Aphi(a, z0, R, z):
   "rho, z0 coordinates of current ring (I=1A)"
#   function_suite
   a2=a*a
   R2=R*R
   z2=np.square(z-z0)
   alpha2=a2 + R2 + z2 - 2.0 * a*R
   beta2 =a2 + R2 + z2 + 2.0 * a*R
   #k2=m
   k2 = 1.0 - alpha2/beta2
   C = cnst.mu_0 /np.pi
   
   Aphi= ((2 - k2) * spcl.ellipk(k2) - 2 * spcl.ellipe(k2)) / k2
   Aphi=  Aphi * 4 * a  / np.sqrt(beta2)
   Aphi=  Aphi * C / 4.0 
   
   #https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.ellipk.html
   
   return Aphi

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
    a=Aphi(0.46, 0.0, 0.2, 0)
    b=Bzloop(0.1, .1)

