from augerRun import *
import pylab as pl

bite1=AugerRun("augerData/bite2/120308BT.1")
bite3=AugerRun("augerData/bite2/120308B3.1")
bite4=AugerRun("augerData/bite2/120308B4.1")

bite1.plot(normalize=True,derivative=False,smoothing=0)
bite3.plot(normalize=True,derivative=False,smoothing=0)
bite4.plot(normalize=True,derivative=False,smoothing=0)

pl.legend()
pl.show()
