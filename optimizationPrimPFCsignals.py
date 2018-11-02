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


Vcl=np.array([isttok_mag['RPfcVer'], isttok_mag['ZPfcVer'], isttok_mag['TurnsPfcVer']]).T
Hcl=np.array([isttok_mag['RPfcHor'], isttok_mag['ZPfcHor'], isttok_mag['TurnsPfcHor']]).T
Pcl=np.array([isttok_mag['RPfcPrim'], isttok_mag['ZPfcPrim'], isttok_mag['TurnsPfcPrim']]).T


#print("Rcoi-11  %g, Zcoil %g" %(RHCoil11, ZHCoil11))

BpolEst=buildIs2Bpol(Vcl, Hcl, Pcl)

prbNums = np.arange(1,13)

client = StartSdas()
#B2MirnFlux = FLux on Mirn probes (Turns * Area  ) in V.s
B2FluxMirn= 50 * 49e-6
scale=1e6 # values in uV.s

Nshot=44501 # Primary
PfcPrimCurrent = 157.0 # np.average(coilPrimData[4500:5500])=  156.86076

#Nshot=44499 # Primary com resistência externa
#PfcPrimCurrent = 157.0 # np.average(coilPrimData[4500:5500])=  156.52623

#Nshot=44503 # Primary  Prim -150A ferro saturado
#PfcPrimCurrent = -160.0 # np.average(coilPrimData[4500:5500])=  -159.57497

#44499 Prim com resistência externa
#44503 Prim -150A ferro saturado

flatSample = 5500 # sample with flat values

#BpolEstTot = BpolEst2 + BpolEst_4 + BpolEst_8 + BpolEst11

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
fig.suptitle("Primary PFC # " +str(Nshot) + ", Sample#: "  +str(flatSample) )
linesV2 = ax.plot(prbNums, BpolEst[:,2]*B2FluxMirn*PfcPrimCurrent *scale,label='Primary Pfc Field Estimated ') #   
#linesV4 = ax.plot(prbNums, BpolEst_4[:,0]*B2FluxMirn*PfcVCurrent *scale,label='Ver Pfc 4 Estimated ') #   
#linesV8 = ax.plot(prbNums, BpolEst_8[:,0]*B2FluxMirn*PfcVCurrent *scale,label='Ver Pfc 8 Estimated ') #   
#linesV11 = ax.plot(prbNums, BpolEst11[:,0]*B2FluxMirn*PfcVCurrent *scale,label='Ver Pfc 11 Estimated ') #   
#linesTot = ax.plot(prbNums,BpolEstTot[:,0]  * B2FluxMirn * PfcVCurrent *scale,label='Ver Pfc Total Estimated ') #   
linesMirnV = ax.plot(prbNums,dataVarr[:,flatSample]*scale, label='measured Field') #   
ax.set_xticks(prbNums)
ax.legend()
ax.set_ylabel('MirnFlux / uV.s')
ax.set_xlabel('Mirn Probe')
plt.show()

       
