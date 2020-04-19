import numpy as np

def staticTHR(timeFrame, hostState, overTHR):    
    [_,numHost,_] = hostState.shape
    print('Detecting overloading hosts.')
    overloadingList = np.zeros(numHost, dtype=np.int32)
    for i in range(numHost):
        if hostState[timeFrame,i,0] == 1:
            if hostState[timeFrame,i,1]/(2200*8) > 2200*8*overTHR:
                overloadingList[i] = 1
        elif hostState[timeFrame,i,0] == 2:
            if hostState[timeFrame,i,1]/(2200*16) > 2200*16*overTHR:
                overloadingList[i] = 1
        elif hostState[timeFrame,i,0] == 3:
            if hostState[timeFrame,i,1]/(2200*32) > 2200*32*overTHR:
                overloadingList[i] = 1
    return overloadingList

def staticTHR_single(timeFrame, hostState, hostIndx, overTHR):
    if hostState[timeFrame,hostIndx,0] == 1:
        if hostState[timeFrame,hostIndx,1]/(2200*8) > 2200*8*overTHR:
            return True
    elif hostState[timeFrame,hostIndx,0] == 2:
        if hostState[timeFrame,hostIndx,1]/(2200*16) > 2200*16*overTHR:
            return True
    elif hostState[timeFrame,hostIndx,0] == 3:
        if hostState[timeFrame,hostIndx,1]/(2200*32) > 2200*32*overTHR:
            return True