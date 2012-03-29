from augerRun import *
import pylab as pl
import numpy as np
from scipy import optimize

#M. K. Bahl, R. L. Watson, and K. J. Irgolic, ChemPhys 68
refPeaks=np.array([481.6,483.9,485.3,491.8,493.9])
indWidth=0.0 #wether or not to use independent widths of the peaks
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
use=[i for i in range(len(r.counts)) if start<r.E[i]<end]
part1=[i for i in use if r.E[i]<left]
part2=[i for i in use if r.E[i]>right]
p1=np.polyfit(r.E[part1],r.countsPerSec[part1],1)
p2=np.polyfit(r.E[part2],r.countsPerSec[part2],1)
line1=r.E[use]*p1[0]+p1[1]
line2=r.E[use]*p2[0]+p2[1]
def base(c,w):
    sigmoid=1/(1+np.exp(-(r.E[use]-c)/(right-left)/w))
    return line1*(1-sigmoid)+line2*sigmoid
def base2(p):
    n=sum(p)
    sigmoid=np.array([sum(p[:i+1])/n for i in range(len(p))])
    return line1*(1-sigmoid)+line2*sigmoid
def peak(x,w,h):
    return np.exp(-((r.E[use]-x)/w)**2)*h #measurement noise
    #return 1/(1+((r.E[use]-x)/w)**2)*h #decay process uncertainty
def peaks(p):
    return sum(peak(p[3*i],p[3*i*indWidth+1],p[3*i+2]) for i in range(5))
guess=[483,1,1e5,485.5,1,1e5,487,1,1e5,493,1,1e5,496,1,1e5,0.1,(right+left)/2]
f=lambda p:r.countsPerSec[use]-base(p[-1],p[-2])-peaks(p[:-1])
#f=lambda p:r.countsPerSec[use]-base2(peaks(p[:-1]))-peaks(p[:-1])
params,optStatus=optimize.leastsq(f,guess)
EError,optStatus=optimize.leastsq(lambda x:np.array(params[:5*3:3])-refPeaks-x,0)
print('Residual: %(res)g'%{'res':sum(f(params)**2)})
print('Results agree best when '+str(-EError)+' eV are added to our AES peaks:')
for i in range(5):
    print('Peak at: '+str(params[i*3]-EError)+
            ' eV, ref: '+str(refPeaks[i])+' eV')
pl.hold(True)
pl.plot(r.E[use],r.countsPerSec[use],linewidth=2,color='red')
pl.plot(r.E[use],base(params[-1],params[-2])+peaks(params),linewidth=2,color='black')
#pl.plot(r.E[use],base2(peaks(params))+peaks(params),linewidth=2,color='black')
for i in range(5):
    pl.plot(r.E[use],base(params[-1],params[-2])+peak(params[3*i],params[3*i*indWidth+1],params[3*i+2]))
    #pl.plot(r.E[use],base2(peaks(params))+peak(params[3*i],params[3*i*indWidth+1],params[3*i+2]))
pl.show()
