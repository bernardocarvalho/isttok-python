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

# Ideal Coil Position

Vcl=np.array([isttok_mag['RPfcVer'], isttok_mag['ZPfcVer'], isttok_mag['TurnsPfcVer']]).T
Hcl=np.array([isttok_mag['RPfcHor'], isttok_mag['ZPfcHor'], isttok_mag['TurnsPfcHor']]).T
Pcl=np.array([isttok_mag['RPfcPrim'], isttok_mag['ZPfcPrim'], isttok_mag['TurnsPfcPrim']]).T

BpolEst=buildIs2Bpol(Vcl, Hcl, Pcl)

prbNums = np.arange(1,13)

client = StartSdas()
#Nshot=44330 # Horizontal Field
#PfcHCurrent = -175.0 # in shot=44330

Nshot=43066 # Primary Field Current 157

PfcHCurrent = -157.0 # in shot=43066

times, dataH =getMirnovInt(client, Nshot, correctWO='Post');
dataHarr =np.array(dataH)

scale=1e6 # values in uV.s

plotAllPoloid(times, dataHarr*scale, show=True, title="Primary Field Coils # " +str(Nshot),  ylim=15.0)
              
#B2MirnFlux = FLux on Mirn probes (Turns * Area  ) in V.s
B2FluxMirn= 50 * 49e-6
scale=1e6 # values in uV.s

flatSample = 5500 # sample with flat values
#fig, ax = plt.subplots()
#fig.suptitle("Horizontal Field Coils # " +str(Nshot) + " Sample#: "  +str(flatSample) )
#ax.plot(prbNums, dataHarr[:,flatSample])
#ax.set_xlabel('Mirn Probe')
#plt.show()

fig, ax = plt.subplots()
fig.suptitle("Primary Field Coils # " +str(Nshot) + " Sample#: "  +str(flatSample) )
#fig.suptitle("Horizontal Field Coils # " +str(Nshot) + " Sample#: "  +str(flatSample) )
#plt.figure()


#Magic Factor
#Mgc=1.

#
#linesV = ax.plot(prbNums, BpolEst[:,0]*B2FluxMirn)
linesH = ax.plot(prbNums, BpolEst[:,2]*B2FluxMirn*PfcHCurrent *scale,label='Primary Estimated Field') #   
linesMirnH = ax.plot(prbNums,dataHarr[:,flatSample]*scale) #   
ax.legend()
ax.set_ylabel('MirnFlux / uV.s')

#"ax.legend(linesBpol, ['m0', 'm1', 'm2','m3', 'm4', 'm5','m6', \
#                         'm7', 'm8','m9', 'm10', 'm11'],loc='right')
ax.set_xlabel('Mirn Probe')
#ax.legend()
plt.show()

#Nshot=44330 # Horizontal Field
#PfcHCurrent = -175.0 # in shot=44330

#Nshot=42952 # Vartical Field
#PfcVCurrent = 340.0 # 
#flatSample = 5500 # sample with flat values

Nshot=44278 # Vartical Field
PfcVCurrent = -400.0 # 
flatSample = 5500 # sample with flat values

times, dataV =getMirnovInt(client, Nshot, correctWO='Post');
dataVarr =np.array(dataV)
plotAllPoloid(times, dataVarr*scale, show=True, title="Vertical Field Coils # " +str(Nshot),  ylim=20.0)

fig, ax = plt.subplots()
fig.suptitle("Vertical Field Coils # " +str(Nshot) + " Sample#: "  +str(flatSample) )
linesV = ax.plot(prbNums, BpolEst[:,0]*B2FluxMirn*PfcVCurrent *scale,label='Vertical Estimated Field') #   
linesMirnV = ax.plot(prbNums,dataVarr[:,flatSample]*scale) #   
ax.legend()
ax.set_ylabel('MirnFlux / uV.s')
ax.set_xlabel('Mirn Probe')
plt.show()



Nshot=44330 # Horizontal Field
PfcHCurrent = -175.0 
flatSample = 3700 # sample with flat values

#Nshot=42966 # Horizontal Field
#PfcHCurrent = 260.0 
#flatSample = 2000 # sample with flat values

times, dataH =getMirnovInt(client, Nshot, correctWO='Post');
dataHarr =np.array(dataH)
plotAllPoloid(times, dataHarr*scale, show=True, title="Horizontal Field Coils # " +str(Nshot),  ylim=10.0)

fig, ax = plt.subplots()
fig.suptitle("Horizontal Field Coils # " +str(Nshot))
lines = ax.plot(times,dataHarr.T*scale) 
ax.legend(lines, ['m1', 'm2', 'm3','m4', 'm5', 'm6','m7', \
                             'm8', 'm9','m10', 'm11', 'm12'],loc='right')
ax.set_ylabel('MirnFlux / uV.s')
ax.set_xlabel('Time / us')
plt.show()

fig, ax = plt.subplots()
fig.suptitle("Horizontal Field Coils # " +str(Nshot) + " Sample#: "  +str(flatSample) )
linesV = ax.plot(prbNums, BpolEst[:,1]*B2FluxMirn*PfcHCurrent *scale,label='Horizontal Estimated Field') #   
linesMirnV = ax.plot(prbNums,dataHarr[:,flatSample]*scale) #   
ax.legend()
ax.set_ylabel('MirnFlux / uV.s')
ax.set_xlabel('Mirn Probe')
plt.show()

#flatSample = 2000 # sample with flat values

Nshot=42966 # Horizontal Field
PfcHCurrent = 260.0 
flatSample = 2000 # sample with flat values

times, dataH =getMirnovInt(client, Nshot, correctWO='Post');
dataHarr =np.array(dataH)
fig, ax = plt.subplots()
fig.suptitle("Horizontal Field Coils # " +str(Nshot))
lines = ax.plot(times,dataHarr.T*scale) 
ax.legend(lines, ['m1', 'm2', 'm3','m4', 'm5', 'm6','m7', \
                             'm8', 'm9','m10', 'm11', 'm12'],loc='right')
ax.set_ylabel('MirnFlux / uV.s')
ax.set_xlabel('Time / us')
plt.show()
        
#plotAllPoloid(times, dataHarr*scale, show=True, title="Horizontal Field Coils # " +str(Nshot),  ylim=100.0)
