import numpy as np
import random
import genHostCluster
import loadTrace
import placementAlgs
import countHostRes
import hostOverloadDetectAlg
import hostUnderloadDetectAlg
import vmSelectionAlg
import networkTopo as nt

#generate the hosts
#numHost = 4
numPod = 8
#hostUnit = 4
#hosts = genHostCluster.genHostCluster(numHost,hostUnit)
_,hosts = nt.fatTree(8)
numHost = len(hosts)

#load the VM trace
timeFrame = 3
numResinTrace = 11
numRes = 6
(numVM,vmTrace) = loadTrace.loadTrace('trace', numResinTrace, timeFrame)

#provion the VMs in to the CDC

#print(hosts)
hostList = hosts.copy()
deployment = placementAlgs.randomPlace(vmTrace, hostList)
#deployment = np.zeros(numVM,dtype=np.int32)
#print(hosts)

print(print('There are '+str(len(np.unique(deployment)))+' hosts are used.'))
#print(t.shape)

#recordhost state in every timeframe
hostState = np.zeros((timeFrame+1, numHost, numRes+2))
curTimeframe = 0
hostList = hosts.copy()
currentHost = countHostRes.count(vmTrace[:,:,0], hostList, deployment, numRes)
#hostState = np.zeros((timeFrame, numHost, numRes) , dtype=np.int32)
hostState[0,:,:] = currentHost
#print(hostState[0,:,:])
#[_,numHost,_] = hostState.shape

Deployment = np.zeros([timeFrame,numVM],dtype=np.int32)
for curTimeframe in range(timeFrame):
    print('this is the '+str(curTimeframe)+'th timeframe:')
    #host overloading detection
    HostState = hostState.copy()
    overloadingList = hostOverloadDetectAlg.staticTHR(curTimeframe, hostState, 0.85)
    #print(overloadingList)
    #host underloading detection
    #underloadingList = hostUnderloadDetectAlg.staticTHR(curTimeframe, hostState, 0.15)
    #print(underloadingList)
    #VM selection
    if curTimeframe == 0:
        D = deployment.copy()
        migratList = vmSelectionAlg.randomSelection(overloadingList, 0.85, D, vmTrace, hostState, 'staticTHR', curTimeframe)
    elif curTimeframe > 0:
        D = Deployment.copy()
        D_ = D[curTimeframe-1,:]
        migratList = vmSelectionAlg.randomSelection(overloadingList, 0.85, D_, vmTrace, hostState, 'staticTHR', curTimeframe)
    #migratList = np.ones(numVM, dtype=np.int32)
    
    print('there are '+str(len(np.argwhere(migratList==1)))+'VMs to be migrated from overloading hosts.')
    #VM placement
    HostState = hostState.copy()
    if curTimeframe == 0:
        Deployment[curTimeframe,:] = placementAlgs.CpuPacking(migratList, vmTrace, HostState, curTimeframe, 0.85, deployment)
    elif curTimeframe > 0:
        Deployment[curTimeframe,:] = placementAlgs.CpuPacking(migratList, vmTrace, HostState, curTimeframe, 0.85, Deployment[curTimeframe-1,:])
     
    print('There are '+str(len(np.unique(Deployment[curTimeframe,:])))+'hosts are used.')
    hostList = hosts.copy()
    currentHost = countHostRes.count(vmTrace[:,:,curTimeframe], hosts, Deployment[curTimeframe,:], numRes)
    #print(currentHost)
    hostState[curTimeframe+1,:,:] = currentHost
    print('----------------------------------------------------------------------------------')


