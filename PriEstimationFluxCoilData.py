# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 14:23:33 2018

@author: bernardo
"""

import numpy as np
#from isttok_magnetics import isttok_mag, buildIs2Bpol

import matplotlib.pyplot as plt
from StartSdas import StartSdas
import magnetic_flux_fields as mf
#from getMirnov import getSignal, getMirnovInt, plotAllPoloid, ch_vert, ch_hor, ch_prim

from getSdasSignal import getSignal

from getFluxCoilData  import flux_int, getFluxCoilData, plotFluxCoilData, plotFluxCoilIntegrated

    
if __name__ == "__main__":
    client = StartSdas()

    #Nshot = 45083 #Primario +140A, 400ms
    Iprim = 140 
    Nshot = 45210# Primario +140A sem terminação 
    #Nshot = 45256 #Primario +140A com terminação 180ohm no canal 142 do marte    
    
    node= flux_int[0]
    signalStructArray=client.getData(node,'0x0000', Nshot)
    signalStruct=signalStructArray[0]
    Tstart=signalStruct.getTStart()
    Tstart.date  
    plotFluxCoilData(client,Nshot)
    plotFluxCoilIntegrated(client,Nshot)
#    Primary Coils 
    #PF1 ATorres
    PrimCoil=np.array([[0.615,  0.144, 14.], 
                   [0.615, -0.145, 14.]])
    
    RFluxPrb=np.array([0.714,  0.705, 0.714])
    ZFluxPrb=np.array([0.012,  0.0, -0.012])
    ATFluxPrb=np.array([0.012*0.154*10,  0.023*0.185*10, 0.012*0.154*10]) # Total Area * turns of probes
    #Is2Bpol=np.zeros((nPrb, ns))
    BrFluxPrb=np.zeros((3))
    BzFluxPrb=np.zeros((3))
    FluxPrbEstim=np.zeros((3))

    for k in range(PrimCoil.shape[0]):
        br,bz= mf.Bloop(PrimCoil[k,0], PrimCoil[k,1], RFluxPrb, ZFluxPrb)
        BrFluxPrb += br*PrimCoil[k,2]
        BzFluxPrb += bz*PrimCoil[k,2]
    
    
    FluxPrbEstim[0] = BrFluxPrb[0]*ATFluxPrb[0]
    FluxPrbEstim[1] = BzFluxPrb[1]*ATFluxPrb[1]  
    FluxPrbEstim[2] = BrFluxPrb[2]*ATFluxPrb[2]
    FluxPrbEstim= FluxPrbEstim*Iprim  
    

