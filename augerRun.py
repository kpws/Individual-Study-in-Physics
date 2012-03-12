import pylab as pl
import numpy as np
from smooth import smooth

class AugerRun:
    def __init__(self,fileName):
        with open(fileName,'r') as f:
            self.name=f.next().strip('\n')
            info=[p for p in f.next().strip('\n\r').split(' ') if p]
            self.startE=float(info[0]) #eV
            self.endE=float(info[1]) #eV
            self.step=float(info[2])
            self.nbrOfScans=float(info[3])
            self.stepTime=float(info[4])
            nbrOfSteps=float(info[5])
            self.EPass=float(info[6])
            self.description=f.next().strip('\n')
            self.counts=[int(i) for i in f]
            if len(self.counts)!=nbrOfSteps:
                raise Exception("Corrupt File")
            self.E=np.array([self.startE+self.step*i for i in
                range(len(self.counts))])
            self.countsPerSec=np.array(self.counts)/self.stepTime
    def plot(self,smoothing=0,derivative=False):
        y=smooth(self.countsPerSec,smoothing)
        x=self.E
        if derivative:
            y=(y[1:]-y[:-1])/self.step
            x=x[0:-1]+self.step
        pl.plot(x,y)
if __name__ == '__main__':
    r=AugerRun('augerData/bite2/120308BT.1')
    r.plot()
    pl.show()
