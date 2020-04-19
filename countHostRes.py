#according to the VM deployment, caculating the available resources of all hosts.
#input vmList as vmTrace at a certain timeframe
import numpy as np
def count(vmList, hostList, deployment, numRes):
    numHost = len(hostList)
    #print('testing!!!!'+str(numHost))
    curHoststate = np.zeros((numHost,numRes+2))
    for i in range(numHost):
        placeIndx = np.argwhere(deployment == i)
        numPlace = len(placeIndx)
        if hostList['hostType'][i] == 'small':
            curHoststate[i,0] = 1
        elif hostList['hostType'][i] == 'medium': 
            curHoststate[i,0] = 2
        elif hostList['hostType'][i] == 'large': 
            curHoststate[i,0] = 3
        if numPlace > 0:
            #print(hostList['CPU'][i])
            for j in range(numPlace):
                #print('host capacity is '+str(hostList['CPU'][i]))
                #print('VM demand is '+str(vmList[deployment[j],3]))                
                hostList['CPU'][i] = hostList['CPU'][i] - vmList[placeIndx[j],3]
                hostList['Mem'][i] = hostList['Mem'][i] - vmList[placeIndx[j],6]
                hostList['DiskWrite'][i] = hostList['DiskWrite'][i] - vmList[placeIndx[j],7]
                hostList['DiskRead'][i] = hostList['DiskRead'][i] - vmList[placeIndx[j],8]
                hostList['NetworkIn'][i] = hostList['NetworkIn'][i] - vmList[placeIndx[j],9]
                hostList['NetworkOut'][i] = hostList['NetworkOut'][i] - vmList[placeIndx[j],10]
        curHoststate[i,1] = hostList['CPU'][i]
        curHoststate[i,2] = hostList['Mem'][i]
        curHoststate[i,3] = hostList['DiskWrite'][i]
        curHoststate[i,4] = hostList['DiskRead'][i]
        curHoststate[i,5] = hostList['NetworkIn'][i]
        curHoststate[i,6] = hostList['NetworkOut'][i]
        curHoststate[i,7] = 1       
            

    return curHoststate