# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 14:23:33 2018

@author: bernardo
"""

import numpy as np
#from isttok_magnetics import isttok_mag, buildIs2Bpol

import matplotlib.pyplot as plt
from StartSdas import StartSdas
from getMirnov import getSignal, getMirnovInt, plotAllPoloid, ch_vert, ch_hor, ch_prim

client = StartSdas()
#B2MirnFlux = FLux on Mirn probes (Turns * Area  ) in V.s
#B2FluxMirn= 50 * 49e-6
scale=1e6 # values in uV.s

#Nshot=44278 # Vartical Field

#Nshot=44501 # Primary Prim +150A
#PfcVCurrent = -400.0 # 
#flatSample = 5500 # sample with flat values
#Nshot=44499 # Primary  com resistência externa
#Nshot=44750
#Nshot =44601
#Nshot = 44769
#Nshot = 44833 
#Nshot = 45015 # Plasma Shot
#Nshot = 45078 #Vertical -+400A, 400ms
#Nshot = 45076 #Horizontal -+200A, 400ms

#Nshot =45076 #Horizontal -+200A, 400ms
Nshot = 45256 #com terminação 180ohm no canal 142 do marte

times, dataMirn =getMirnovInt(client, Nshot, correctWO='Post');
dataMirnArr =np.array(dataMirn)
plotAllPoloid(times, dataMirnArr*scale, show=True, title="Mirnov Signals # " +str(Nshot),  ylim=00.0)
              
fig, ax = plt.subplots()
fig.suptitle("Mirnov PFC # " +str(Nshot))
lines = ax.plot(times,dataMirnArr.T*scale) 
ax.legend(lines, ['m1', 'm2', 'm3','m4', 'm5', 'm6','m7', \
                             'm8', 'm9','m10', 'm11', 'm12'],loc='right')
ax.set_ylabel('MirnFlux / uV.s')
ax.set_xlabel('Time / us')
plt.show()
              
times, coilVData, tbs = getSignal(client, ch_vert, Nshot)
times, coilHData, tbs = getSignal(client, ch_hor, Nshot)
times, coilPrimData, tbs = getSignal(client, ch_prim, Nshot)


fig, ax = plt.subplots()
fig.suptitle(" PFC Currents# " +str(Nshot))
lineV = ax.plot(times,coilVData, label='Ver Pfc ') 
lineH = ax.plot(times,coilHData, label='Hor Pfc ') 
linePrim = ax.plot(times,coilPrimData, label='Prim Pfc ') 
#label='Ver Pfc 2 Estimated Field'
ax.legend()
ax.set_ylabel('Current / A')
ax.set_xlabel('Time / us')
plt.show()
