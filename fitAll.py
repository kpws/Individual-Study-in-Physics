from augerRun import *
from fitPeaks import *
import pylab as pl
import numpy as np
import ref

samples=["Te","BiTe","BiTe (Pd)"]
elements=["Te","Bi","Pd"]
refPeaks=[ref.TePeaks,ref.BiPeaks,ref.PdPeaks]
sources=[[('augerData/te/120319TE.1',0),
        ('augerData/te/120319TE.1',1),
        ('augerData/te/120319TE.1',1)],
       [('augerData/bite2/120308B4.1',0),
        ('augerData/bite2/120308B2.1',0),
        ('augerData/bite2/120308BT.1',0)],
       [('augerData/bitepd1/120314P1.1',1),
        ('augerData/bitepd1/120313P1.1',1),
        ('augerData/bitepd1/120314P1.1',0)]]
start=[452.0,-1,-1]
end=[523.0,float('inf'),float('inf')]
left=[[480.0,85.0,315.0]]*3
right=[[499.0,110.0,340.0]]*3

guessShift=1.5

colors=['red','green','blue']
for i in range(len(samples)):
    for j in range(len(elements)):
        r=AugerRun(sources[i][j][0],part=sources[i][j][1])
        guess=refPeaks[j]+guessShift
        print(str(i)+','+str(j))
        (params,fitE,fitCounts,EError)=fitPeaks(r,
                guess,left[i][j],right[i][j],
                start=start[j],end=end[j])
        shift=-guessShift-EError
        print('Results agree best when '+str(shift)+' eV are added to our AES peaks:')
        for p in range(len(guess)):
            print('Peak at: '+str(params[p*3]+shift)+
                    ' eV, ref: '+str(refPeaks[j][p])+' eV')
        pl.hold(True)
        pl.plot(r.E,r.countsPerSec,linewidth=2,color=colors[i])
        pl.plot(fitE,fitCounts,linewidth=2,color='black')

pl.show()
