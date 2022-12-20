#!/usr/bin/env python3
# vim: sta:et:sw=4:ts=4:sts=4
"""
Plot 12 ISTTOK integrated Mirnovs
"""

import numpy as np
import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from StartSdas import StartSdas
#from getSdasSignal import getSignal, mirnv_int
from getMirnov import  getMirnovInt

if len(sys.argv) > 1:
    pulse = int(sys.argv[1])
else:
    pulse = 49639 # No fields, zero Wo coeffs


app = pg.mkQApp("ISTTOK Mag Probes Integrated, pulse {}".format(pulse))

sdasClient = StartSdas()

#print("pulse: {}".format(pulse))
win = pg.GraphicsLayoutWidget(show=True, title="ISTTOK Mag Probes Integrated, pulse {}".format(pulse))
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

times, coilData = getMirnovInt(sdasClient,  pulse)

p = [None] * 12
for i in range(0,4):
    p[i] = win.addPlot(title="Coil {}".format(i+1))
    p[i].plot(times, coilData[i], pen=({'color': (i, 12*1.3),
            'width': 1}), name="ch{}".format(i+1))
#p1 = win.addPlot(title="Basic array plotting", y=np.random.normal(size=100))
#p1 = win.addPlot(title="Coil 1, grid enabled")
#p1.plot(times, coilData[0])
#p1.showGrid(x=True, y=True)

#p2 = win.addPlot(title="Coil 2")
#p2.plot(times, coilData[1])
#p2.showGrid(x=True, y=True)
#p2 = win.addPlot(title="Multiple curves")
#p2.plot(np.random.normal(size=100), pen=(255,0,0), name="Red curve")
#p2.plot(np.random.normal(size=110)+5, pen=(0,255,0), name="Green curve")
#p2.plot(np.random.normal(size=120)+10, pen=(0,0,255), name="Blue curve")

#p3 = win.addPlot(title="Coil 3")
#p3.plot(times, coilData[2])
#p3.showGrid(x=True, y=True)
#p3 = win.addPlot(title="Drawing with points")
#p3.plot(np.random.normal(size=100), pen=(200,200,200), symbolBrush=(255,0,0), symbolPen='w')

#
win.nextRow()
for i in range(4,8):
    p[i] = win.addPlot(title="Coil {}".format(i+1))
    p[i].plot(times, coilData[i], pen=({'color': (i, 12*1.3),
            'width': 1}), name="ch{}".format(i+1))

win.nextRow()

for i in range(8,12):
    p[i] = win.addPlot(title="Coil {}".format(i+1))
    p[i].plot(times, coilData[i], pen=({'color': (i, 12*1.3),
            'width': 1}), name="ch{}".format(i+1))

if __name__ == '__main__':
    pg.exec()



