from augerRun import *
from fitPeaks import *
import pylab as pl
import numpy as np
import ref

samples=["Metallic Te","$\mathrm{Bi}_2\mathrm{Te}_3$","$\mathrm{Bi}_2\mathrm{Te}_3$ (little Pd)","$\mathrm{Bi}_2\mathrm{Te}_3$ (much Pd)"]
elements=["Te","Bi","Pd"]
refPeaks=[ref.TePeaks,ref.BiPeaks,ref.PdPeaks]
sources=[[('augerData/te/120319TE.1',0),
        ('augerData/te/120319TE.1',1),
        ('augerData/te/120319TE.1',1)],
       [('augerData/bite2/120308B4.1',0),
        ('augerData/bite2/120308B2.1',0),
        ('augerData/bite2/120308BT.1',0)],
       [('augerData/bitepd2/170512PA.2',3),
        ('augerData/bitepd2/170512PA.2',2),
        ('augerData/bitepd2/170512PA.2',0)],
       [('augerData/bitepd1/120314P2.1',1),
        ('augerData/bitepd1/120314P2.1',0),
        ('augerData/bitepd1/120314P2.1',2)]]
start=[452.0,70.0,300]
end=[510.0,125.0,355.0]
left=[[478.0,85.0,315.0]]*4
right=[[499.0,110.0,340.0]]*4

guessShift=1.7
peaks=[]
colors=['red','green','blue','cyan','magenta','yellow','black']
fits=pl.figure().add_subplot(111)
fits.hold(True)

i=2
j=0
r=AugerRun(sources[i][j][0],part=sources[i][j][1])
guess=refPeaks[j]+guessShift

fits.plot(r.E,r.countsPerSec*1e-6,linewidth=2,color=colors[i],label=(samples[i] if j==0 else ''))

(params,relHeights,fitE,fitCounts,EError)=fitPeaks(r,
        guess,left[i][j],right[i][j],
        start=start[j],end=end[j])
left=left[i][j]
right=right[i][j]
start=start[j]
end=end[j]
ins=range(len(r.counts))
use=[i for i in ins if left<r.E[i]<right]  #used for final optim
part1=[i for i in ins if start<=r.E[i]<=left] #linefit 1 done on
part2=[i for i in ins if end>=r.E[i]>=right]
p1=np.polyfit(r.E[part1],r.countsPerSec[part1],1)
p2=np.polyfit(r.E[part2],r.countsPerSec[part2],1)
pl.plot([r.E[0],r.E[-1]],[(p1[1]+p1[0]*r.E[0])*1e-6,(p1[1]+p1[0]*r.E[-1])*1e-6],color='black',linewidth=1)
pl.plot([r.E[0],r.E[-1]],[(p2[1]+p2[0]*r.E[0])*1e-6,(p2[1]+p2[0]*r.E[-1])*1e-6],color='black',linewidth=1)

#fits.legend(loc=2)
pl.xlabel('Energy [eV]')
pl.ylabel('Count rate [$10^6s^{-1}$]')

pl.show()
