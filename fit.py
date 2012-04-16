from augerRun import *
from fitPeaks import *
import pylab as pl
import numpy as np

#M. K. Bahl, R. L. Watson, and K. J. Irgolic, ChemPhys 68
refPeaks=np.array([481.6,483.9,485.3,491.8,493.9])

run=1
start=452.0;end=523.0
if run==1:
    name='augerData/bite2/120308B3.1'
    left=470.0
    right=510.0
elif run==2:
    name='augerData/bite2/120308B4.1'
    left=480.0
    right=500.0
r=AugerRun(name)
guess=refPeaks+1.5#[483,485.5,487,493,496]
(params,fitE,fitCounts,EError)=fitPeaks(r,guess,left,right,start=start,end=end)
print('Results agree best when '+str(-EError)+' eV are added to our AES peaks:')
for i in range(5):
    print('Peak at: '+str(params[i*3]-EError)+
            ' eV, ref: '+str(refPeaks[i])+' eV')
pl.hold(True)
pl.plot(r.E,r.countsPerSec,linewidth=2,color='red')
pl.plot(fitE,fitCounts,linewidth=2,color='black')
pl.show()
