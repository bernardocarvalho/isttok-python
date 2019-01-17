# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 19:06:50 2018

@author: bernardo
Calibration Setup made in 2016 by Domenica with AC wire current setput
"""

import matplotlib.pyplot as plt
import numpy as np
from magnetic_flux_fields import Bloop, BradBpol
from getSdasSignal import getSignal
from StartSdas import StartSdas

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

#samplingPeriod = 1./2e6
#Fsampling = 2e6

#Calibration Setup 2016 Domenica
# Probes insert on Port 4 mockup 
# Probes and Holes ar not correctl numbered on Domenica PDF
# Probes are numbered clockwise
RMajor = 0.46   # Vessel center Major radius
Rmirn = 0.0935  #Mirnov Coil radius 
Rhole = 0.05 # Hole circle position radius 

n_pbrs = 12
# Mirnov Proble Angle Posiiton in PORT 4 wood mock-up (+8.6 Angle offset)
angles_pbrOff = np.arange((360.-6.4),0,  -30) / 180.0 *np.pi 
#RprbOff =RMajor + Rmirn * np.cos(angles_pbrOff)
#ZprbOff =Rmirn * np.sin(angles_pbrOff)

# Mirnov Proble Angle Posiiton in wood mock-up (NO Angle offset)
angles_pbr = np.arange((360.0-15),0,  -30) / 180.0 *np.pi 

#Rprb =RMajor + Rmirn * np.cos(angles_pbr)
#Zprb =Rmirn * np.sin(angles_pbr)

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

def MirnIntegration(MirnArr,samplingPeriod):
    # Do the Sum (Time integration)
    MirnSum=np.cumsum(MirnArr,axis=1) * samplingPeriod
    #Allocate numpy array
    MirnSumDeTrend = np.zeros_like(MirnSum)
    for i in range(MirnSum.shape[0]):
        lastVal=MirnSum[i,-1]
        slope=np.linspace(0,lastVal,len(MirnSum[i]))
        MirnSumDeTrend[i] = MirnSum[i] - slope
    return MirnSumDeTrend

def HolePosition(angle):
    Rw=RMajor + Rhole*np.cos(angle)
    Zw= Rhole*np.sin(angle)
    return Rw, Zw

def MirnovPositions(RMirnCenter,ZMirnCenter):
    """
    Probe positions for a  Mirnov set of 12 probes
    RMirnCenter,ZMirnCenter are the center of the Mirnov set
    """
    Rprb =RMirnCenter + Rmirn * np.cos(angles_pbr)
    Zprb =ZMirnCenter + Rmirn * np.sin(angles_pbr)
    return Rprb, Zprb
 
def MirnovRotatedPositions(RMirnCenter,ZMirnCenter):
    """
    Probe positions for a  Mirnov rotated (+8.6 º) set of 12 probes
    DRcentral,DZcentral are the deviations of the Mirnov set from the "vessel"
    """
    Rprb =RMirnCenter + Rmirn * np.cos(angles_pbrOff)
    Zprb =ZMirnCenter + Rmirn * np.sin(angles_pbrOff)
    return Rprb, Zprb

def PlotMirnInt(times,MirnInt):
    fig, ax = plt.subplots()
    fig.suptitle(f"Calibration Raw data,  Shot {Nshot} ")# +str(Nshot), coil {coilIdx +1})
    lines=ax.plot(times*1e-3,MirnInt.transpose()) 
    ax.legend(lines, ['m1', 'm2', 'm3','m4', 'm5', 'm6','m7', \
                             'm8', 'm9','m10', 'm11', 'm12'],loc='right')

    ax.set_xlabel('Time / ms')
    plt.show()  

    
if __name__ == "__main__":
    client = StartSdas()
    Rwire = RMajor; Zwire =0.0
#Shot 40387 - hole 1   Rwire = 0.46; Zwire  = 0.05
#Shot 40388 - hole 0   Rwire = 0.46; Zwire  = 0.0
#Shot 40389 - hole 2   #  hole 4?
#Shot 40392 - hole 4   #  hole 2?
#Shot 40393 - hole 3   Rwire = 0.46; Zwire  = -0.05
#Shot 40394 - hole 5   Rwire = 0.46 +
#Shot 40397 - hole 7   Rwire = 0.46  -          #  hole 8 ?
#Shot 40398 - hole 6   Rwire = 0.46  -          #  hole 5 ?
#Shot 40399 - hole 8   Rwire = 0.46 +           #  hole 7?

# Probe # 11 was replaced after calibration
 
    Nshot=40388;   Hole=0 #      #Wire loop in the center of vessel
    RMirnCenter =RMajor; ZMirnCenter=0.0

#    Nshot=40387;   Hole=1 # 
#    RMirnCenter =RMajor; ZMirnCenter=-0.05
#
#    Nshot=40392;   Hole=2 # 
#    RMirnCenter =0.51; ZMirnCenter=0

#    Nshot=40393;   Hole=3 # 
#    RMirnCenter =RMajor; ZMirnCenter=0.05

#    Nshot=40399;   Hole=7 # 
#    RMirnCenter =0.4954; ZMirnCenter=0.035

    
#    Rwire, Zwire  =HolePosition(np.pi/2.)

#    Nshot=40394;   Hole=5 # 
#    Rwire, Zwire  =HolePosition(np.pi/4.)
#    Nshot=40389;   Hole=4 #
#    Rwire, Zwire  =HolePosition(0)

#    Nshot=40392;   Hole=2 # 
#    Rwire, Zwire  =HolePosition(np.pi)

#    Nshot=40399;   Hole=7 #
#    Rwire, Zwire  =HolePosition(-np.pi*3/4.0)
#
#    Nshot=40397;   Hole=8 #
#    Rwire, Zwire  =HolePosition(-np.pi*1/4.0)
    
#    Nshot=40398;   Hole=5 #
#    Rwire, Zwire  =HolePosition(np.pi/4.0)

#    print(f"Rwire :{Rwire:5.2f}, Zwire: {Zwire:5.2f} ")
    Rprb, Zprb = MirnovPositions(RMirnCenter,ZMirnCenter)
    RprbOff, ZprbOff = MirnovRotatedPositions(RMirnCenter,ZMirnCenter)
    print(f"RMirnCenter :{RMirnCenter:6.3f}, ZMirnCenter: {ZMirnCenter:6.3f} ")
    Iwire=-1.0
    
    times, MirnArr=  getMirnCalib(client, Nshot) # get Raw ADC data
    Ts=(times[1]-times[0]) * 1e-6 # Sampling Time In s
    Fs=1/Ts # sampling rate in Hertz

    MirnInt = MirnIntegration(MirnArr,Ts)
    PlotMirnInt(times,MirnInt)

    #FFT calculation
    #coils

    Nprobes, Nsamples = MirnInt.shape # signal.size # length of the signal 

    signalFFT=np.fft.rfft(MirnInt)/ Nsamples # Compute  Normalized real FFT
    freq = np.fft.fftfreq(Nsamples, d=Ts) # Frequency horizontal axys

    #coilIdx =3   # m4 ftt
    #Plot first few elements of FFT (must multiply by 2 for correct amplitudes)
#    fig, ax = plt.subplots()
#    ax.stem(freq[range(20)], 2 * abs(signalFFT[coilIdx, range(20)]))
#    fig.suptitle(f"FFT data,  Shot {Nshot}, coil m{coilIdx +1} ")# +str(Nshot), coil {coilIdx +1})
#    ax.set_xlabel('F / Hz')
#    plt.show() 

#    Estimated fields on the probes for Iwire = 1A
    BR,BZ =Bloop(Rwire, Zwire, Rprb, Zprb)
    bradEst, bpolEst  = BradBpol(BR,BZ, angles_pbr)
    #Offset angle position
    BROff,BZOff =Bloop(Rwire, Zwire, RprbOff, ZprbOff)
    bradEstOff, bpolEstOff  = BradBpol(BROff,BZOff, angles_pbrOff)
    
    Amplitude50Hz=np.zeros((Nprobes,1))
    f50Idx=int(50/(Fs/Nsamples))
    for i in range(Nprobes):
        Amplitude50Hz[i]=2 * abs(signalFFT[i, f50Idx])
        
    fig, ax1 = plt.subplots() 
    fig.suptitle(f" Calibration 50Hz Mirnov Amplitudes,  Shot {Nshot}, Hole {Hole}")
    ax1.stem(range(1,13),Amplitude50Hz)
    ax1.set_ylabel('Measured Flux (LSB*s)', color='b')
    ax1.set_xlabel('Probe #')
    ax2 = ax1.twinx()
    ax2.plot(range(1,13),bpolEst*Iwire*1e6, 'r.', label='Est. Probes')
    ax2.plot(range(1,13),bpolEstOff*Iwire*1e6, 'kx', label='Est. Offset Probes')
    ax2.legend()
    ax2.set_ylim(bottom=0)
    ax2.set_ylabel('Estimated Field (uT)', color='r')
    plt.show()

#Probe Offset +8.6º

    
    
    