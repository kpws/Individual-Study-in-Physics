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
end=[523.0,125.0,355.0]
left=[[478.0,85.0,315.0]]*4
right=[[499.0,110.0,340.0]]*4

guessShift=[1.6,1.6,1.0,0.5,0.0]
peaks=[]
colors=['red','green','blue','cyan','magenta','yellow','black']
fits=pl.figure().add_subplot(111)
fits.hold(True)
#for e in end+start+left[0]+right[0]:
#    pl.plot([e,e],[0,2e6],'gray')
for i in range(len(samples)):
    samplePeaks=[]
    for j in [0]:
        r=AugerRun(sources[i][j][0],part=sources[i][j][1])
        guess=refPeaks[j]+guessShift[i]
        print(j)
        (params,relHeights,fitE,base,EError)=fitPeaks(r,
                guess,left[i][j],right[i][j],
                start=start[j],end=end[j])
        samplePeaks.append([[params[t*3],relHeights[t]] for t in range(len(guess))])
        #shift=-guessShift-EError
        #print('Results agree best when '+str(shift)+' eV are added to our AES peaks:')
        #for p in range(len(guess)):
        #    print('Peak at: '+str(params[p*3]+shift)+
        #            ' eV, ref: '+str(refPeaks[j][p])+' eV')
        scale=1/base[0]
        shift=0.25*i
        fits.plot(r.E,shift+r.countsPerSec*scale,linewidth=2,color=colors[i],label=(samples[i]
            if j==0 else ''))
        tableString=""
        for p in range(len(guess)):
            fits.plot(fitE,shift+(base+abs(params[p*3+2])*np.exp(-((fitE-params[p*3])/params[p*3+1])**2))*scale,linewidth=1,color='black')
            tableString+=" & "+str(round((params[p*3]-2.4)*10)/10)
        print(tableString)
        print(params[3*3+1])
    peaks.append(samplePeaks)
#fits.legend(loc=2)
pl.xlabel('Energy [eV]')
pl.ylabel('Normalized count rate')
if False:
    ax2=pl.figure().add_subplot(111)
    width=0.25
    bottom=480
    for i in range(len(refPeaks[0])):
        ind=i+np.arange(len(samples))
        for j in range(len(samples)):
            ax2.bar(i+j*width,-bottom+peaks[j][0][i][0],width,bottom,color=colors[j],label=(samples[j]
                if i==0 else ''))
    ax2.legend(loc=2)
    pl.title('Te peak positions for the 3 different samples')
    pl.xlabel('Peak number')
    pl.ylabel('Peak energy [eV]')

    ax3=pl.figure().add_subplot(111)
    width=0.25
    for e in range(len(elements)):
        for i in range(len(refPeaks[e])):
            ind=i+np.arange(len(samples))
            for j in range(len(samples)):
                ax3.bar(e*5+i+j*width,peaks[j][e][i][1],width,bottom,color=colors[j],label=(samples[j]
                    if i==0 else ''))
    ax3.legend(loc=2)
    pl.title('Te peak positions for the 3 different samples')
    pl.xlabel('Peak number')
    pl.ylabel('Peak energy [eV]')

pl.show()
