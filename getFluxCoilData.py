# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 14:23:33 2018

@author: bernardo
"""

import numpy as np
#from isttok_magnetics import isttok_mag, buildIs2Bpol

import matplotlib.pyplot as plt
from StartSdas import StartSdas
#from getMirnov import getSignal, getMirnovInt, plotAllPoloid, ch_vert, ch_hor, ch_prim

from getSdasSignal import getSignal

flux_int=['MARTE_NODE_IVO3.DataCollection.Channel_141',
'MARTE_NODE_IVO3.DataCollection.Channel_142',
'MARTE_NODE_IVO3.DataCollection.Channel_143',
'MARTE_NODE_IVO3.DataCollection.Channel_144']

flux_adc_raw=['MARTE_NODE_IVO3.DataCollection.Channel_157',
'MARTE_NODE_IVO3.DataCollection.Channel_158',
'MARTE_NODE_IVO3.DataCollection.Channel_159',
'MARTE_NODE_IVO3.DataCollection.Channel_160']

def getFluxCoilData(sdasClient, shot_, nodes=flux_int):
#    coilNr=0
    data=[]
    
    for coil in nodes:
  #      coilNr+=1
        times, coilData, tbs = getSignal(sdasClient, coil, shot_)
        data.append(coilData)
        
    dataArr = np.array(data)
    return times, dataArr

# Shot  Nov  6 17:40 44523
#    Nov  8 10:34 44534    
# 160913 Nov 12 11:34 44560    

def plotFluxCoilIntegrated(shot):
    VertScale =  1.7102e-4 / 2.0e6 # LSB to Volt * Sampling Period
    #uVscale=1e6 # Plot values in uV.s
    
    times, dataInt =getFluxCoilData(client, Nshot,  nodes=flux_int)
    fig, ax = plt.subplots()
    fig.suptitle("Flux Integrated data,  Shot# " +str(Nshot))
    lines = ax.plot(times,dataInt.T * VertScale) 
    ax.legend(lines, ['c1', 'c2', 'c3','c4'],loc='right')
    ax.set_ylabel('Flux / V.s')
    ax.set_xlabel('Time / us')
    plt.show()    

def plotFluxCoilData(shot):
    lsbVscale=1/2**14 # Raw Data must be shifted 14 bits to the right
    lsbVscale= lsbVscale *  1.7102e-4  # LSB to Volt
    times, dataRaw =getFluxCoilData(client, Nshot,  nodes=flux_adc_raw)
    fig, ax = plt.subplots()
    fig.suptitle("Flux Raw data,  Shot# " +str(Nshot))
    lines = ax.plot(times,dataRaw.T * lsbVscale) 
    ax.legend(lines, ['c1', 'c2', 'c3','c4'],loc='right')
    ax.set_ylabel('Data / V')
    ax.set_xlabel('Time / us')
    plt.show()  
    
if __name__ == "__main__":
    client = StartSdas()
    #Nshot=44776 # " Shot with HOrizontal field
    #Nshot=44700 # "Informatic Shot, no fields
    Nshot = 44804 # Shot with Plasma EO offset corrected 
    
    plotFluxCoilData(Nshot)
    plotFluxCoilIntegrated(Nshot)
    

#    eo=np.average(dataRaw,axis=1) * lsbVscale # Vlaues have to be 

    # Nshot=44775  eo [-614,  527, -212,   99]
    # Nshot=44778  eo [-612,  518, -215,   96]
    # Nshot = 44700 -615,  519, -212,   97
    # Nshot = 44701 -615,  517, -214,   95
    # Nshot=44600= -615,  519, -212,   97
    
    
