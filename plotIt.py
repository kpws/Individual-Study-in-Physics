from augerRun import *
import pylab as pl

runs=[AugerRun('augerData/bite2/120308B'+i+'.1') for i in 'T234']

for r in runs:
    r.plot(smoothing=15,derivative=False)
    pl.hold(True)

pl.show()
