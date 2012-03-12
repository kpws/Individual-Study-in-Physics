import numpy as np

def smooth(data,amount):
    smoothedData=np.zeros(len(data))
    kernel=np.ndarray(amount*2+1)
    if amount==0:
        kernel[0]=1.0
    else:
        for i in range(amount*2+1):
            kernel[i]=np.exp(-((2.0*float(i-amount)/float(amount))**2.0))
    for i in range(len(data)):
        tot=0.0
        for j in range(amount*2+1):
            if i+j-amount>0 and i+j-amount<len(data):
                smoothedData[i]+=kernel[j]*data[i+j-amount]
                tot+=kernel[j]
        smoothedData[i]/=tot
    return smoothedData
