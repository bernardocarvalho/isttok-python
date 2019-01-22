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

flux_int=['MARTE_NODE_IVO3.DataCollection.Channel_141', # Upper radial saddle coil
'MARTE_NODE_IVO3.DataCollection.Channel_142',  # Vertical saddle coil
'MARTE_NODE_IVO3.DataCollection.Channel_143',  # Lower radial saddle coil
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

def plotFluxCoilIntegrated(client, shot):
    VertScale =  1.7102e-4/10.0 / 2.0e6 *1e6 # Convertion from ADC raw to Flux (in uV.s)
    # LSB to Volt * Sampling Period * 1e6
    
    times, dataInt =getFluxCoilData(client, shot,  nodes=flux_int)
    fig, ax = plt.subplots()
    fig.suptitle("Flux Integrated data,  Shot# " +str(shot))
    lines = ax.plot(times,dataInt.T * VertScale) 
    ax.legend(lines, ['Rad Up', 'Vert', 'Rad Down','c4'],loc='right')
    ax.set_ylabel('Flux / uV.s')
    ax.set_xlabel('Time / us')
    plt.show()    

def plotFluxCoilData(client, shot):
    lsbVscale=1/2**14 # Raw Data must be shifted 14 bits to the right
    #lsbVscale= lsbVscale *  1.7102e-4  # LSB to Volt
    times, dataRaw =getFluxCoilData(client, shot,  nodes=flux_adc_raw)
    fig, ax = plt.subplots()
    fig.suptitle("Flux Raw data,  Shot# " +str(shot))
    lines = ax.plot(times,dataRaw.T * lsbVscale) 
    ax.legend(lines, ['Rad Up', 'Vert', 'Rad Down','c4'],loc='right')
    ax.set_ylabel('Data / LSB')
    ax.set_xlabel('Time / us')
    plt.show()  
    
if __name__ == "__main__":
    client = StartSdas()
    #Nshot=44776 # " Shot with Horizontal field
    #Nshot=44700 # "Informatic Shot, no fields
#    Nshot = 44819 # Shot with Plasma EO offset corrected in FPGA first shot 44804
#    Nshot = 44830
#    Nshot = 44836
#    Nshot = 45076 #Horizontal -+200A, 400ms
#    Nshot = 45206
    
#    Nshot = 45208 # Rogoswky installed
#    Nshot = 45210 # Ramp Primary
    # Nshot = 45078 #Vertical -+400A, 400ms
    Nshot =   45083; IHPfc=175 # Primary Coil +140A, 400ms

    #Nshot =45123 #    Pilha de 1.5V com 1.311V
    #45085 Primario -140A, 400ms
    #Nshot = 44804
    
    node= flux_int[0]
    signalStructArray=client.getData(node,'0x0000', Nshot)
    signalStruct=signalStructArray[0]
    Tstart=signalStruct.getTStart()
    print(Tstart.date) # Print the date
    
    plotFluxCoilData(client,Nshot)
    plotFluxCoilIntegrated(client,Nshot)

#    Horizontal PFC Coils 
    #Measured  positions obtained by HF + BBC  10 Jan  2019
#    HPfcCoil=np.array([[0.560,  0.10, 4.], 
#                   [0.566, -0.10, -4.]])
#    
##   Estimation of the Flux on the saddle coils created by a current IHPfc on the Horizontal PFC
#    RFluxPrb=np.array([0.714,  0.705, 0.714])
#    ZFluxPrb=np.array([0.012,  0.0, -0.012])
#    ATFluxPrb=np.array([0.012*0.154*10,  0.023*0.185*10, 0.012*0.154*10]) # Total Area * turns of probes
#    #Is2Bpol=np.zeros((nPrb, ns))
#    BrFluxPrb=np.zeros((3))
#    BzFluxPrb=np.zeros((3))
#    FluxPrbEstim=np.zeros((3))
#
#    for k in range(HPfcCoil.shape[0]):
#        br,bz= mf.Bloop(HPfcCoil[k,0], HPfcCoil[k,1], RFluxPrb, ZFluxPrb)
#        BrFluxPrb += br*HPfcCoil[k,2]
#        BzFluxPrb += bz*HPfcCoil[k,2]
#    
#    
#    FluxPrbEstim[0] = BrFluxPrb[0]*ATFluxPrb[0]*IHPfc  
#    FluxPrbEstim[1] = BzFluxPrb[1]*ATFluxPrb[1]*IHPfc    
#    FluxPrbEstim[2] = BrFluxPrb[2]*ATFluxPrb[2]*IHPfc  
    


    
        

#    eo=np.average(dataRaw,axis=1) * lsbVscale # Vlaues have to be 

    # Nshot=44775  eo [-614,  527, -212,   99]
    # Nshot=44778  eo [-612,  518, -215,   96]
    # Nshot = 44700 -615,  519, -212,   97
    # Nshot = 44701 -615,  517, -214,   95
    # Nshot=44600= -615,  519, -212,   97
    
    
