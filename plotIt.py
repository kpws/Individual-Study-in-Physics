from augerRun import *
import pylab as pl

#runs=[AugerRun('augerData/bite2/120308B'+i+'.1') for i in 'T234']
runs=[AugerRun('augerData/bitepd1/120313P'+i+'.1') for i in '12']

for r in runs:
    r.plot(smoothing=15,derivative=False)
    pl.hold(True)

pl.show()
