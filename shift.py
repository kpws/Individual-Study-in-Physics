from augerRun import *
import pylab as pl

te=AugerRun("augerData/te/120319TE.1",part=0)
bite=AugerRun("augerData/bite2/120308B3.1",part=0)
bitepd=AugerRun("augerData/bitepd1/120314P1.1",part=1)

te.plot(normalize=True,derivative=False,smoothing=10)
bite.plot(normalize=True,derivative=False,smoothing=10)
bitepd.plot(normalize=True,derivative=False,smoothing=10)
pl.legend()
pl.show()
