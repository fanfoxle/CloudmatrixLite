import xlrd
import numpy as np
import os
import sys
import time
import random
from progressbar import ProgressBar, Bar, Percentage

#vmTrace(x,y,z)
#x:VM number index
#y:VM resource index
#z:time frame index

def loadTrace(filePath,numRes,timeFrame):
    x = 0
    filename = os.listdir(filePath)
    numVM = len(filename)
    vmTrace = np.zeros((numVM,numRes,timeFrame))
    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=numVM).start()
    print('There are '+str(numVM)+' VMs. Loading the traces:')
    for fileName in filename:
        #print('loading the trace of the ',x+1,'th VM. The file name is ',fileName,'.')
        data = xlrd.open_workbook(filePath+'\\'+fileName)    
        table = data.sheet_by_name('Sheet1')        
        if table.nrows>=timeFrame:
            #row = table.nrows
            row = timeFrame
            #col = table.ncols
            col = numRes
            vm = np.zeros((row, col))
            for i in range(row):
                rows = np.matrix(table.row_values(i))
                vm[i,:] = rows
                #print(vm[i,:])
            vmTrace[x,:,:] = vm.transpose()
        #else:
            #print('this trace is invalid!')
        time.sleep(0.01)
        pbar.update(x+1)
        x = x + 1
    pbar.finish()
    return (numVM,vmTrace)

def randomGen(numRes, timeFrame, startTime, endTime):
    vmTrace = np.zeros((numRes,timeFrame))
    starttimeframe = 1376314846
    cpuCores = np.array([1,2,4,8])
    cpuCore = cpuCores[random.randint(0,3)]
    cpuProvisioned = cpuCore*2599.999304
    memProvisioneds = np.array([8,16,32])
    memProvisioned = memProvisioneds[random.randint(0,2)]*1024*1024
    diskreadProvisioneds = np.array([1,2])
    diskreadProvisioned = diskreadProvisioneds[random.randint(0,1)]*100*1024
    diskwriteProvisioned = diskreadProvisioned
    for k in range(timeFrame):
        vmTrace[0,k] = starttimeframe + k*300        
        if k >= startTime and k <= endTime:
            vmTrace[1,k] = cpuCore
            vmTrace[2,k] = cpuProvisioned            
            vmTrace[3,k] = random.randint(0,cpuProvisioned*10000000)/10000000
            vmTrace[4,k] = vmTrace[3,k]/cpuProvisioned
            vmTrace[5,k] = memProvisioned
            vmTrace[6,k] = random.randint(0,memProvisioned)
            vmTrace[7,k] = random.randint(0,diskreadProvisioned)
            vmTrace[8,k] = random.randint(0,diskwriteProvisioned)
            vmTrace[9,k] = random.randint(0,10*1024*1024)
            vmTrace[10,k] = random.randint(0,10*1024*1024)
    return vmTrace




