# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 09:52:36 2018

@author: bernardo
"""


import numpy as np
from isttok_magnetics import isttok_mag, buildIs2Bpol

import matplotlib.pyplot as plt
from StartSdas import StartSdas
from getMirnov import getSignal, getMirnovInt, plotAllPoloid, ch_vert, ch_hor, ch_prim

#Estimation of probe signals
# Alternative Coil Position
Vcl1=np.array([
      [ 0.60,  0.08, -1.  ],
      [ 0.59,  0.07, -1.  ],
      [ 0.58,  0.07, -1.  ],
      [ 0.59,  0.07, -1.  ],
      [ 0.60,  0.06, -1.  ],
      
      [ 0.58, -0.07, -5.  ],
      [ 0.35,  0.07,  5.  ],
      [ 0.35, -0.07,  5.  ]])


Hcl1=np.array([
       [ 0.56,  0.08,  1.0  ],
       [ 0.58,  0.07,  1.0  ],
       [ 0.58,  0.06,  1.0  ],
       [ 0.59,  0.07,  1.0  ],
       [ 0.58, -0.07, -4.0 ]])

Hcl2=np.array([
       [ 0.58,  0.07,  1.0  ],   # wrong placements ?
       [ 0.58,  0.07,  1.0  ],
       [ 0.58,  0.07,  1.0  ],
       [ 0.58,  0.07,  1.0  ],
       [ 0.35,  -0.07,  1.0  ],
       [ 0.58, -0.07, -6.0 ]])

Hcl3=np.array([
       [ 0.58,  0.07,  0.0  ],   
       [ 0.58, -0.07, -1.0 ]]) # Ideal Coil Position

Vcl1=np.array([
      [ 0.60,  0.08, -1.  ],
      [ 0.59,  0.07, -1.  ],
      [ 0.58,  0.07, -1.  ],
      [ 0.59,  0.07, -1.  ],
      [ 0.60,  0.06, -1.  ],
      
      [ 0.58, -0.07, -5.  ],
      [ 0.35,  0.07,  5.  ],
      [ 0.35, -0.07,  5.  ]])

Pcl=np.array([isttok_mag['RPfcPrim'], isttok_mag['ZPfcPrim'], isttok_mag['TurnsPfcPrim']]).T

radiusHCoil0=0.13893
angleHCoil0= 0.5280 #  np.arctan(7./12) 
radiusHCoil=0.136
angleHCoil=-0.8

RHCoil2=isttok_mag['RM']+ radiusHCoil*np.cos(angleHCoil)
ZHCoil2= radiusHCoil*np.sin(angleHCoil)

print("Rcoi %g, Zcoil %g" %(RHCoil2, ZHCoil2))

Hcl2=np.array([
       [ 0.58,  0.07,  0.0  ],   
       [ RHCoil2, ZHCoil2, -4.0 ]]) # Ideal Coil Position
BpolEst2=buildIs2Bpol(Vcl1, Hcl2, Pcl)

Hcl11=np.array([
       [ 0.58,  0.07,  4.0  ],   
       [ 0.58, -0.07, 0.0 ]]) # Ideal Coil Position

Hcl11=np.array([
       [ 0.58,  0.07,  4.0  ],   
       [ 0.58, -0.07, 0.0 ]]) # Ideal Coil Position

radiusHCoil=0.13
angleHCoil= 1.035

RHCoil11=isttok_mag['RM'] + radiusHCoil*np.cos(angleHCoil)
ZHCoil11= radiusHCoil*np.sin(angleHCoil)

Hcl11=np.array([
       [ RHCoil11, ZHCoil11,  4.0  ],   
       [ 0.58, -0.07, 0.0 ]]) # Ideal Coil Position

print("Rcoi %g, Zcoil %g" %(RHCoil11, ZHCoil11))

BpolEst11=buildIs2Bpol(Vcl1, Hcl11, Pcl)

prbNums = np.arange(1,13)

client = StartSdas()
#B2MirnFlux = FLux on Mirn probes (Turns * Area  ) in V.s
B2FluxMirn= 50 * 49e-6
scale=1e6 # values in uV.s

#Nshot=44330 # Horizontal Field
#PfcHCurrent = -175.0 # in shot=44330

#Nshot=44330 # Horizontal Field
Nshot=44123 # Horizontal Field
PfcHCurrent = -190 # -175.0 
flatSample = 3700 # sample with flat values

#Nshot=42966 # Horizontal Field
#PfcHCurrent = 260.0 
#flatSample = 2000 # sample with flat values

times, dataH =getMirnovInt(client, Nshot, correctWO='Post');
dataHarr =np.array(dataH)
#plotAllPoloid(times, dataHarr*scale, show=True, title="Horizontal Field Coils # " +str(Nshot),  ylim=10.0)

#fig, ax = plt.subplots()
#fig.suptitle("Horizontal Field Coils # " +str(Nshot))
#lines = ax.plot(times,dataHarr.T*scale) 
#ax.legend(lines, ['m1', 'm2', 'm3','m4', 'm5', 'm6','m7', \
#                             'm8', 'm9','m10', 'm11', 'm12'],loc='right')
#ax.set_ylabel('MirnFlux / uV.s')
#ax.set_xlabel('Time / us')
#plt.show()

fig, ax = plt.subplots()
fig.suptitle("Horizontal Field Coils # " +str(Nshot) + " Sample#: "  +str(flatSample) )
linesV2 = ax.plot(prbNums, BpolEst2[:,1]*B2FluxMirn*PfcHCurrent *scale,label='Hor Pfc 2 Estimated Field') #   
linesV11 = ax.plot(prbNums, BpolEst11[:,1]*B2FluxMirn*PfcHCurrent *scale,label='Hor Pfc 11 Estimated Field') #   
linesTot = ax.plot(prbNums,(BpolEst2[:,1] + BpolEst11[:,1])*B2FluxMirn*PfcHCurrent *scale,label='Hor Pfc Total Estimated Field') #   
linesMirnV = ax.plot(prbNums,dataHarr[:,flatSample]*scale, label='measured') #   
ax.set_xticks(prbNums)
ax.legend()
ax.set_ylabel('MirnFlux / uV.s')
ax.set_xlabel('Mirn Probe')
plt.show()

       
