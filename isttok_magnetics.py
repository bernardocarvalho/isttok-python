# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 18:53:42 2018

@author: bernardo
"""

from __future__ import print_function
import numpy as np

#ISTTOK
#
rm = 0.085 #Minor radius
RM = 0.46   # Major radius
Rmirn = 0.0935  #Mirnov Probe Radius   9.35  

nPrb = 12
# Poloidal Angle of Mirnov probe
tethaPrb = np.array([(23./24 - i/nPrb)*2*np.pi for i in range(nPrb)])

Rprb =RM + Rmirn * np.cos(tethaPrb)
Zprb =Rmirn * np.sin(tethaPrb)

#Vertical Coils: 4 coils, 5 turns, R1,2=58 [cm],R2,3=35 [cm],z=±7 [cm]
RPfcVer =[0.58, 0.58, 0.35, 0.35]
ZPfcVer =[0.07, -0.07, 0.07, -0.07]
TurnsPfcVer=[-5., -5., 5., 5.]
#Horizontal Coils: 2 coils , 4 turns, R1,2=58 [cm],z=±7[cm]
RPfcHor =[0.58, 0.58,]
ZPfcHor =[0.07, -0.07]
TurnsPfcHor=[4., -4.]

isttok_mag = {'RM': RM, 'rm': rm, 'Rmirn': Rmirn , 'Rcopper': 0.105, 'nPrb':nPrb, \
          'tethaPrb':tethaPrb, 'Rprb':Rprb , 'Zprb':Zprb, \
          'RPfcVer':RPfcVer, 'ZPfcVer':ZPfcVer, 'TurnsPfcVer':TurnsPfcVer, \
          'RPfcHor':RPfcHor, 'ZPfcHor':ZPfcHor, 'TurnsPfcHor':TurnsPfcHor }