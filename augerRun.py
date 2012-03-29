import pylab as pl
import numpy as np
from smooth import smooth

class AugerRun:
    def __init__(self, fileName, part=0):
        with open(fileName,'r') as f:
            self.fileName=fileName
            self.part=part
            self.name=f.next().strip('\n')
            info=[p for p in f.next().strip('\n\r').split(' ') if p]
            nbrOfSteps=int(round(float(info[5])))
            for p in range(part):
                for i in range(nbrOfSteps):
                    f.next()
                self.name=f.next().strip('\n')
                info=[p for p in f.next().strip('\n\r').split(' ') if p]
                nbrOfSteps=int(round(float(info[5])))
            self.startE=float(info[0]) #eV
            self.endE=float(info[1]) #eV
            self.step=float(info[2]) #eV
            self.nbrOfScans=float(info[3])
            self.stepTime=float(info[4]) #sec
            self.EPass=float(info[6])
            self.description=f.next().strip('\n')
            self.counts=[float(f.next()) for i in range(nbrOfSteps)]
            self.E=np.array([self.startE+self.step*i for i in
                range(nbrOfSteps)])
            self.countsPerSec=np.array(self.counts)/self.stepTime
    def plot(self,smoothing=0,derivative=False,normalize=False):
        y=smooth(self.countsPerSec,smoothing)
        x=self.E
        if derivative:
            y=(y[1:]-y[:-1])/self.step
            x=x[0:-1]+self.step
            if normalize:
                y/=np.sqrt(sum(y**2))
        elif normalize:
            y*=len(y)/sum(y)
        pl.plot(x,y,label=self.fileName+':'+str(self.part))
if __name__ == '__main__':
    r=AugerRun('augerData/bite2/120308BT.1')
    r.plot()
    pl.legend()
    pl.show()
