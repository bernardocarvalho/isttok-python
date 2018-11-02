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

VclOptim=np.array([
      [ 0.526368,  0.111782, -3.  ],
      [ 0.554752, -0.0975604, -3.  ],
      [ 0.380273,  0.113862,  3.  ],
      [ 0.3905,   -0.120378,  3.  ]])


Hcl=np.array([isttok_mag['RPfcHor'], isttok_mag['ZPfcHor'], isttok_mag['TurnsPfcHor']]).T
Pcl=np.array([isttok_mag['RPfcPrim'], isttok_mag['ZPfcPrim'], isttok_mag['TurnsPfcPrim']]).T

BpolEstOptim=buildIs2Bpol(VclOptim, Hcl, Pcl)

# Nominal coil Position
radiusHCoil0=0.13893
angleHCoil0= 0.5280 #  np.arctan(7./12) 

radiusHCoil=0.136
angleHCoil=-0.8

RHCoil2=isttok_mag['RM']+ radiusHCoil*np.cos(angleHCoil)
ZHCoil2= radiusHCoil*np.sin(angleHCoil)

print("Rcoi %g, Zcoil %g" %(RHCoil2, ZHCoil2))

Vcl2=np.array([
       [ 0.58,  0.07,  0.0  ],   # Nominal Coil Position
       [ RHCoil2, ZHCoil2, -3.0 ]]) 
BpolEst2=buildIs2Bpol(Vcl2, Hcl, Pcl)


radiusCoil=0.139
angleCoil=- 120 * np.pi/180  # -105

RCoil_4=isttok_mag['RM'] + radiusCoil*np.cos(angleCoil)
ZCoil_4= radiusCoil*np.sin(angleCoil)

Vcl_4=np.array([
       [ RCoil_4, ZCoil_4,  3.0  ],   
       [ 0.35, -0.07, 0.0 ]]) # Nominal Coil Position

print("Rcoi-4  %g, Zcoil %g, Turns: %g" %(RCoil_4, ZCoil_4, 3))

BpolEst_4=buildIs2Bpol(Vcl_4, Hcl, Pcl)


radiusCoil=0.139
angleCoil= 125 * np.pi/180 

RCoil_8=isttok_mag['RM'] + radiusCoil*np.cos(angleCoil)
ZCoil_8= radiusCoil*np.sin(angleCoil)

Vcl_8=np.array([
       [ RCoil_8, ZCoil_8,  3.0  ],   
       [ 0.35, -0.07, 0.0 ]]) # Nominal Coil Position

print("Rcoi-8  %g, Zcoil %g, Turns: %g" %(RCoil_8, ZCoil_8, 3))

BpolEst_8=buildIs2Bpol(Vcl_8, Hcl, Pcl)


#Vcl11=np.array([
#       [ 0.58,  0.07,  0.0  ],   
#       [ 0.58, -0.07, 0.0 ]]) # Ideal Coil Position

radiusHCoil=0.13
angleHCoil= 1.035

RHCoil11=isttok_mag['RM'] + radiusHCoil*np.cos(angleHCoil)
ZHCoil11= radiusHCoil*np.sin(angleHCoil)

Vcl11=np.array([
       [ RHCoil11, ZHCoil11,  -3.0  ],   
       [ 0.58, -0.07, 0.0 ]]) # Nominal Coil Position

print("Rcoi-11  %g, Zcoil %g" %(RHCoil11, ZHCoil11))

BpolEst11=buildIs2Bpol(Vcl11, Hcl, Pcl)


prbNums = np.arange(1,13)

client = StartSdas()
#B2MirnFlux = FLux on Mirn probes (Turns * Area  ) in V.s
B2FluxMirn= 50 * 49e-6
scale=1e6 # values in uV.s

Nshot=44278 # Vartical Field
PfcVCurrent = -400.0 # 
flatSample = 5500 # sample with flat values

BpolEstTot = BpolEst2 + BpolEst_4 + BpolEst_8 + BpolEst11

times, dataV =getMirnovInt(client, Nshot, correctWO='Post');
dataVarr =np.array(dataV)
#plotAllPoloid(times, dataVarr*scale, show=True, title="Vertical PFC # " +str(Nshot),  ylim=10.0)

#fig, ax = plt.subplots()
#fig.suptitle("Mirnov Signal # " +str(Nshot))
#lines = ax.plot(times,dataVarr.T*scale) 
#ax.legend(lines, ['m1', 'm2', 'm3','m4', 'm5', 'm6','m7', \
#                             'm8', 'm9','m10', 'm11', 'm12'],loc='right')
#ax.set_ylabel('MirnFlux / uV.s')
#ax.set_xlabel('Time / us')
#plt.show()

fig, ax = plt.subplots()
fig.suptitle("Vertical PFC # " +str(Nshot) + " Sample#: "  +str(flatSample) )
linesV2 = ax.plot(prbNums, BpolEst2[:,0]*B2FluxMirn*PfcVCurrent *scale,label='Ver Pfc 2 Estimated ') #   
linesV4 = ax.plot(prbNums, BpolEst_4[:,0]*B2FluxMirn*PfcVCurrent *scale,label='Ver Pfc 4 Estimated ') #   
linesV8 = ax.plot(prbNums, BpolEst_8[:,0]*B2FluxMirn*PfcVCurrent *scale,label='Ver Pfc 8 Estimated ') #   
linesV11 = ax.plot(prbNums, BpolEst11[:,0]*B2FluxMirn*PfcVCurrent *scale,label='Ver Pfc 11 Estimated ') #   
linesOptim = ax.plot(prbNums, BpolEstOptim[:,0] * B2FluxMirn*PfcVCurrent *scale,label='Ver Pfc Optimized') #   
linesTot = ax.plot(prbNums,BpolEstTot[:,0]  * B2FluxMirn * PfcVCurrent *scale,label='Ver Pfc Total Estimated ') #   
linesMirnV = ax.plot(prbNums,dataVarr[:,flatSample]*scale, label='measured Field') #   
ax.set_xticks(prbNums)
ax.legend()
ax.set_ylabel('MirnFlux / uV.s')
ax.set_xlabel('Mirn Probe')
plt.show()

       
