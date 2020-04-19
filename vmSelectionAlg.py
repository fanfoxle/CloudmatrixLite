import numpy as np
import random

def randomSelection(overloadingList, overTHRPara, deployment, vmList, hostState, overLoadDetectMeth, timeFrame): 
#def randomSelection(underloadingList, overloadingList, overTHRPara, deployment, vmList, hostState, overLoadDetectMeth, timeFrame):   
    migratList = np.zeros(len(vmList), dtype=np.int32)
    #selecting VMs from overloading host
    for i in range(len(overloadingList)):        
        if overloadingList[i] == 1:
            if overLoadDetectMeth == 'staticTHR':
                hostLoad = hostState(timeFrame, i, 1)
                if hostState(timeFrame, i, 0) == 1:
                    loadTHR = 2200*8*overTHRPara
                elif hostState(timeFrame, i, 0) == 2:
                    loadTHR = 2200*16*overTHRPara
                elif hostState(timeFrame, i, 0) == 3:
                    loadTHR = 2200*32*overTHRPara            
                while hostLoad > loadTHR:
                    vm = np.argwhere(deployment==i)
                    #print('there are '+str(len(vm))+'VMs to be migrated on host '+str(i))
                    t = random.randint(0,len(vm))
                    selectVM = vm[t]
                    migratList[selectVM] = 1
                    deployment[selectVM] = 0
                    hostLoad = hostLoad - vmList[timeFrame,selectVM,3]
            if overLoadDetectMeth == 'others':
                print('Developing...plz input staticTHR as overLoadDetectMeth')
    #selecting VMs from underloading host
    #for i in range(len(underloadingList)):
    #    if underloadingList[i] == 1:
    #        vm = np.argwhere(deployment==i)
    #        #print('there are '+str(len(vm))+'VMs to be migrated on host '+str(i))
    #        migratList[vm] = 1
    return migratList
