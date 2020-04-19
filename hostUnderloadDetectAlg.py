import numpy as np

def staticTHR(timeFrame, hostState, underTHR):    
    [_,numHost,_] = hostState.shape
    underloadingList = np.zeros(numHost, dtype=np.int32)
    print('Detecting underloading hosts.')
    for i in range(numHost):        
        if hostState[timeFrame,i,0] == 1:
            if hostState[timeFrame,i,1]/(2200*8) < 2200*8*underTHR:
                underloadingList[i] = 1
        elif hostState[timeFrame,i,0] == 2:
            if hostState[timeFrame,i,1]/(2200*16) < 2200*16*underTHR:
                underloadingList[i] = 1
        elif hostState[timeFrame,i,0] == 3:
            if hostState[timeFrame,i,1]/(2200*32) < 2200*32*underTHR:
                underloadingList[i] = 1
    return underloadingList