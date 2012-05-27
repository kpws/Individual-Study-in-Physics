from augerRun import *
import pylab as pl
import numpy as np
from scipy import optimize

# r - AugerRun instance
# guess - initial guess of peakpositions
# indWidth - whether or not to have individual widths of the peaks
# left, right, where the peak area is, used to determine the asymptotes of the
# _background_, eV
# start, end can be used to limit area of optimization, eV
def fitPeaks(r,guess,left,right,start=-1,end=float('inf'),indWidth=True):
    ins=range(len(r.counts))
    use=[i for i in ins if left<r.E[i]<right]  #used for final optim
    part1=[i for i in ins if start<=r.E[i]<=left] #linefit 1 done on this part
    part2=[i for i in ins if end>=r.E[i]>=right]
    p1=np.polyfit(r.E[part1],r.countsPerSec[part1],1)
    p2=np.polyfit(r.E[part2],r.countsPerSec[part2],1)
    line1=r.E[use]*p1[0]+p1[1]
    line2=r.E[use]*p2[0]+p2[1]
    def sig(x):
        return 1/(1+np.exp(-x/(right-left)))
    def base(c,w):
        sigmoid=sig((r.E[use]-c)/w)
        return line1*(1-sigmoid)+line2*sigmoid
    #attemp at a model of why the background drops at peak, results not too
    #good, just crude model works better
    #def base2(p):
    #    n=sum(p)
    #    sigmoid=np.array([sum(p[:i+1])/n for i in range(len(p))])
    #    return line1*(1-sigmoid)+line2*sigmoid
    def peak(x,w,h):
        return np.exp(-((r.E[use]-x)/w)**2)*h #measurement noise
        #return 1/(1+((r.E[use]-x)/w)**2)*h #decay process uncertainty
    def peaks(p):
        return sum(peak(p[3*i],p[3*(i if indWidth else 0)+1],abs(p[3*i+2])) for i in range(len(guess)))
    fullGuess=[]
    for e in guess:
        fullGuess+=[e,0.5,1e5] #assumes width 1 eV and height 1e5 are reasonable
    fullGuess+=[0.1,(right+left)/2.0]
    f=lambda p:r.countsPerSec[use]-base(p[-1],p[-2])-peaks(p[:-1])
    #f=lambda p:r.countsPerSec[use]-base2(peaks(p[:-1]))-peaks(p[:-1])
    params,optStatus=optimize.leastsq(f,fullGuess)
    EError,optStatus=optimize.leastsq(lambda
            x:np.array(params[:-3:3])-np.array(guess)-x,0)
    relHeights=params[2:len(guess)*3+2:3]
    return (params,relHeights,r.E[use],base(params[-1],params[-2]),EError)
