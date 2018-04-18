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
   #https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.ellipk.html
   
   return spcl.ellipk(k2)

