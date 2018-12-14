# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 19:06:50 2018

@author: bernardo
"""

import matplotlib.pyplot as plt
from getSdasSignal import getSignal
from StartSdas import StartSdas
import numpy as np

mirnv_calib=['PCIE_ATCA_ADC_16.BOARD_2.CHANNEL_001',
'PCIE_ATCA_ADC_16.BOARD_2.CHANNEL_002',
'PCIE_ATCA_ADC_16.BOARD_2.CHANNEL_003',
'PCIE_ATCA_ADC_16.BOARD_2.CHANNEL_004',
'PCIE_ATCA_ADC_16.BOARD_2.CHANNEL_005',
'PCIE_ATCA_ADC_16.BOARD_2.CHANNEL_006',
'PCIE_ATCA_ADC_16.BOARD_2.CHANNEL_007',
'PCIE_ATCA_ADC_16.BOARD_2.CHANNEL_008',
'PCIE_ATCA_ADC_16.BOARD_2.CHANNEL_009',
'PCIE_ATCA_ADC_16.BOARD_2.CHANNEL_010',
'PCIE_ATCA_ADC_16.BOARD_2.CHANNEL_011',
'PCIE_ATCA_ADC_16.BOARD_2.CHANNEL_012']

def getMirnCalib(sdasClient, shot_):
    nodes=mirnv_calib
   # coilNr=0
    data=[]
  #  slopes=[]
    for coil in nodes:
        times, coilData, tbs = getSignal(sdasClient, coil, shot_)
        data.append(coilData)
        
    DataArr=np.array(data)
    return times, DataArr        
        
if __name__ == "__main__":
    client = StartSdas()
#Shot 40387 - hole 1
#Shot 40388 - hole 0
#Shot 40389 - hole 2
#Shot 40392 - hole 4
#Shot 40393 - hole 3
#Shot 40394 - hole 5
#Shot 40397 - hole 7
#Shot 40398 - hole 6
#Shot 40399 - hole 8    
    Nshot=40393 #
    times, MirnArr=  getMirnCalib(client, Nshot) # get Raw ADC data
    # Do the Sum (Time integration)
    MirnSum=np.cumsum(MirnArr,axis=1)
    #Allocate numpy array
    MirnSumDeTrend = np.zeros_like(MirnSum)
    for i in range(MirnSum.shape[0]):
        lastVal=MirnSum[i,-1]
        slope=np.linspace(i,lastVal,len(MirnSum[i]))
        MirnSumDeTrend[i] = MirnSum[i] - slope
    fig, ax = plt.subplots()
    lines=ax.plot(MirnSumDeTrend.transpose()) 
    ax.legend(lines, ['m1', 'm2', 'm3','m4', 'm5', 'm6','m7', \
                             'm8', 'm9','m10', 'm11', 'm12'],loc='right')

    ax.set_xlabel('Time / us')
    plt.show()  
    
    #FFT fo
    #coils
    fig, ax = plt.subplots()
    Ts=times[1]-times[0] # Sampling Time In us
    Fs=1e6/Ts # sampling rate
    signal=MirnSumDeTrend[1]
    N = signal.size # length of the signal 

    signalFFT=np.fft.rfft(MirnSumDeTrend)/ N # Compute  Normalized real FFT
    freq = np.fft.fftfreq(N, d=Ts*1e-6) # Frequency horizontal axys
    coilIdx = 3 # m4 ftt
    #Plot first few elements of FFT (must multiply by 2 for correct amplitudes)
    ax.stem(freq[range(20)], 2 * abs(signalFFT[coilIdx, range(20)]))
    fig.suptitle(f"Flux Raw data,  Shot {Nshot}, coil m{coilIdx +1} ")# +str(Nshot), coil {coilIdx +1})
    ax.set_xlabel('F / Hz')
    plt.show()  
    