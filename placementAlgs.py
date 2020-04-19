import random
import numpy as np
import hostUnderloadDetectAlg as hud
import countHostRes as CHR

def randomPlace( vmList, hostList ):
    numVM = len(vmList)
    numHost = len(hostList)
    deployment = np.zeros(numVM , dtype=np.int32)
    for i in range(numVM):
        for j in range(numHost):
            if vmList[i,2,0] <= hostList['CPU'][j] and vmList[i,5,0] <= hostList['Mem'][j]:
               deployment[i] = j
               print('VM '+str(i)+' is placed on host '+str(j)+'.')
               hostList['CPU'][j] = hostList['CPU'][j] - vmList[i,2,0]
               hostList['Mem'][j] = hostList['Mem'][j] - vmList[i,5,0]               
               break
    return deployment

def CpuPacking(migratList, vmList, HostState, timeFrame, overTHRPara, deployRec):
    #divide hosts into ACTIVE and EMPTY
    [_,numHost,_] = HostState.shape
    #print('numHost is '+str(numHost))
    
    activeHost = np.transpose(np.argwhere(HostState[timeFrame,:,7] == 1))[0]
    emptyHost = np.transpose(np.argwhere(HostState[timeFrame,:,7] == 0))
    
    #sort the activeHost in decreasing order by their capacities    
    numActiveHost = len(activeHost)
    activeHostCap = np.zeros(numActiveHost)
    for i in range(numActiveHost):
            activeHostCap[i] = (HostState[timeFrame,activeHost[i],1]/(2200*32)) + (HostState[timeFrame,activeHost[i],2]/(128*1024*1024)) \
            + (HostState[timeFrame,activeHost[i],3]/(1024*1024)) + (HostState[timeFrame,activeHost[i],4]/(1024*1024)) \
                + (HostState[timeFrame,activeHost[i],5]/(1024*1024)) + (HostState[timeFrame,activeHost[i],6]/(1024*1024))
    activeHostcapIndx = np.argsort(-activeHostCap)
    hostIndx = np.append(activeHost[activeHostcapIndx],emptyHost)
    
    #sort the VMs in decreasing order by their capacities
    numVM = len(migratList)
    vmCap = np.zeros(numVM)
    for i in range(numVM):
        if migratList[i] == 1:            
            vmCap[i] = (vmList[i,3,timeFrame]/(2200*32)) + (vmList[i,6,timeFrame]/(128*1024*1024))\
                + (vmList[i,7,timeFrame]/(1024*1024)) + (vmList[i,8,timeFrame]/(1024*1024))\
                    + (vmList[i,9,timeFrame]/(1024*1024)) + (vmList[i,10,timeFrame]/(1024*1024)) 

    
    deployment = np.zeros(numVM,dtype=np.int32)
    vmCapIndx = np.argsort(-vmCap)
    #place VMs from overloading hosts
    for i in range(numVM):
        if migratList[vmCapIndx[i]] == 1:
            for j in range(numActiveHost):
                if HostState[timeFrame,hostIndx[j],1]>=vmList[vmCapIndx[i],3,timeFrame] and HostState[timeFrame,hostIndx[j],2]>=vmList[vmCapIndx[i],6,timeFrame] and \
                    HostState[timeFrame,hostIndx[j],3]>=vmList[vmCapIndx[i],7,timeFrame] and HostState[timeFrame,hostIndx[j],4]>=vmList[vmCapIndx[i],8,timeFrame] and \
                        HostState[timeFrame,hostIndx[j],5]>=vmList[vmCapIndx[i],9,timeFrame] and HostState[timeFrame,hostIndx[j],6]>=vmList[vmCapIndx[i],10,timeFrame]:                        
                        deployment[vmCapIndx[i]] = hostIndx[j]
                        HostState[timeFrame,hostIndx[j],1] = HostState[timeFrame,hostIndx[j],1] - vmList[vmCapIndx[i],3,timeFrame]
                        HostState[timeFrame,hostIndx[j],2] = HostState[timeFrame,hostIndx[j],2] - vmList[vmCapIndx[i],6,timeFrame]
                        HostState[timeFrame,hostIndx[j],3] = HostState[timeFrame,hostIndx[j],3] - vmList[vmCapIndx[i],7,timeFrame]
                        HostState[timeFrame,hostIndx[j],4] = HostState[timeFrame,hostIndx[j],4] - vmList[vmCapIndx[i],8,timeFrame]
                        HostState[timeFrame,hostIndx[j],5] = HostState[timeFrame,hostIndx[j],5] - vmList[vmCapIndx[i],9,timeFrame]
                        HostState[timeFrame,hostIndx[j],6] = HostState[timeFrame,hostIndx[j],6] - vmList[vmCapIndx[i],10,timeFrame]
                        print('VM '+str(vmCapIndx[i])+' is placed to host '+str(hostIndx[j]))
                        break            
        elif migratList[vmCapIndx[i]] == 0:
            deployment[vmCapIndx[i]] = deployRec[vmCapIndx[i]]
        
    #packing VMs from underloading  hosts
    
    #detecting current underloading hosts
    underLoadingList = hud.staticTHR(timeFrame, HostState, 0.35)
    print('there are '+str(len(np.argwhere(underLoadingList==1)))+' underloading hosts.')

    #sorting the non-empty hosts in ascedning orders by their capacities
    #for an underloading host, moving all its VMs until there is no host before it can host its VMs.
    hostCPUIndx = np.argsort(-HostState[timeFrame,:,1])
    #print(hostCPUIndx)    

    print('Packing underloading hosts.')
    for i in range(numHost):
                
        if underLoadingList[hostCPUIndx[i]]==1 and len(np.argwhere(deployment==hostCPUIndx[i]))>0:
            #print('Handling host '+str(hostCPUIndx[i])+'. There are '+str(len(np.argwhere(deployment==hostCPUIndx[i])))+' VMs.')
            #ramdon select VMs to move
            vmOnHost = np.argwhere(deployment==hostCPUIndx[i])
            #print('there are '+str(len(vmOnHost))+' potential VMs could be migrated from host '+str(hostCPUIndx[i]))            
            for j in range(len(vmOnHost)):
                #print('Searching from host '+str(hostCPUIndx[numHost-1])+' to host '+str(hostCPUIndx[i]))
                #for k in range(hostCPUIndx[numHost-1],hostCPUIndx[i],-1):
                #for k in range(hostCPUIndx[numHost-1],hostCPUIndx[i],-1):
                for k in range(numHost-1,i,-1):
                    #print('Checking host '+str(hostCPUIndx[k]))
                    #if HostState[timeFrame,hostCPUIndx[k],1] < vmList[vmOnHost[j],3,timeFrame]:
                    #    print('not enough resource '+str(1)+' on host '+str(hostCPUIndx[k])+' for VM '+str(vmOnHost[j]))
                    #    print('the gap is '+str(HostState[timeFrame,hostCPUIndx[k],1])+' VS. '+str(vmList[vmOnHost[j],3,timeFrame]))
                    #else:
                    #    print('Check!') 
                    #if HostState[timeFrame,hostCPUIndx[k],2] < vmList[vmOnHost[j],6,timeFrame]:
                    #    print('not enough resource '+str(2)+' on host '+str(hostCPUIndx[k])+' for VM '+str(vmOnHost[j]))
                    #else:
                    #    print('Check!') 
                    #if HostState[timeFrame,hostCPUIndx[k],3] < vmList[vmOnHost[j],7,timeFrame]:
                    #    print('not enough resource '+str(3)+' on host '+str(hostCPUIndx[k])+' for VM '+str(vmOnHost[j]))
                    #else:
                    #    print('Check!') 
                    #if HostState[timeFrame,hostCPUIndx[k],4] < vmList[vmOnHost[j],8,timeFrame]:
                    #    print('not enough resource '+str(4)+' on host '+str(hostCPUIndx[k])+' for VM '+str(vmOnHost[j]))
                    #else:
                    #    print('Check!') 
                    #if HostState[timeFrame,hostCPUIndx[k],5] < vmList[vmOnHost[j],9,timeFrame]:
                    #    print('not enough resource '+str(5)+' on host '+str(hostCPUIndx[k])+' for VM '+str(vmOnHost[j]))
                    #else:
                    #    print('Check!') 
                    #if HostState[timeFrame,hostCPUIndx[k],6] < vmList[vmOnHost[j],10,timeFrame]:
                    #    print('not enough resource '+str(6)+' on host '+str(hostCPUIndx[k])+' for VM '+str(vmOnHost[j]))
                    #else:
                    #    print('Check!') 
                    #if deployment[vmOnHost[j]] == hostCPUIndx[k]:
                    #    print('VM '+str(vmOnHost[j])+' is already on host '+str(hostCPUIndx[k]))
                    #else:
                    #    print('Check!') 


                    if HostState[timeFrame,hostCPUIndx[k],1]>=vmList[vmOnHost[j],3,timeFrame] and \
                        HostState[timeFrame,hostCPUIndx[k],2]>=vmList[vmOnHost[j],6,timeFrame] and \
                        HostState[timeFrame,hostCPUIndx[k],3]>=vmList[vmOnHost[j],7,timeFrame] and \
                        HostState[timeFrame,hostCPUIndx[k],4]>=vmList[vmOnHost[j],8,timeFrame] and \
                        HostState[timeFrame,hostCPUIndx[k],5]>=vmList[vmOnHost[j],9,timeFrame] and \
                        HostState[timeFrame,hostCPUIndx[k],6]>=vmList[vmOnHost[j],10,timeFrame] and \
                        deployment[vmOnHost[j]] != hostCPUIndx[k]:
                            deployment[vmOnHost[j]] = hostCPUIndx[k]
                            HostState[timeFrame,hostCPUIndx[k],1] = HostState[timeFrame,hostCPUIndx[k],1] - vmList[vmOnHost[j],3,timeFrame]
                            HostState[timeFrame,hostCPUIndx[k],2] = HostState[timeFrame,hostCPUIndx[k],2] - vmList[vmOnHost[j],6,timeFrame]
                            HostState[timeFrame,hostCPUIndx[k],3] = HostState[timeFrame,hostCPUIndx[k],3] - vmList[vmOnHost[j],7,timeFrame]
                            HostState[timeFrame,hostCPUIndx[k],4] = HostState[timeFrame,hostCPUIndx[k],4] - vmList[vmOnHost[j],8,timeFrame]
                            HostState[timeFrame,hostCPUIndx[k],5] = HostState[timeFrame,hostCPUIndx[k],5] - vmList[vmOnHost[j],9,timeFrame]
                            HostState[timeFrame,hostCPUIndx[k],6] = HostState[timeFrame,hostCPUIndx[k],6] - vmList[vmOnHost[j],10,timeFrame]
                            print('VM '+str(vmOnHost[j])+' is placed to host '+str(hostCPUIndx[k]))
                            break
    return deployment
