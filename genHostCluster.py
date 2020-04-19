import numpy as np
import random
import sys
import time
from progressbar import ProgressBar, Bar, Percentage

def genHostCluster(numHost, hostUnit):
    host = np.zeros(numHost, dtype={
        'names':('rackIndx','hostType', 'CPU', 'Mem', 'DiskWrite', 'DiskRead', 'NetworkIn', 'NetworkOut'),
        'formats':('i4','U10', 'f4', 'f4','f4','f4','f4','f4')
    })
    
    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=numHost).start()
    print('Generating hosts:')

    #rack unit is 42; host unit should be better in 1, 2 or 4. The space between two hosts is 2U.
    #20 1U hosts/9 2U hosts/6 4U hosts in a rack.
    for i in range(0,numHost):
        if hostUnit == 1:
            host['rackIndx'][i] = int(i/20)            
        elif hostUnit == 2:
            host['rackIndx'][i] = int(i/9)
        elif hostUnit == 4:
            host['rackIndx'][i] = int(i/6)
        #tmp = random.randint(1,3)
        tmp = 3
        if tmp == 1:
            host['hostType'][i] = 'small'
            host['CPU'][i] = 2200*8
            host['Mem'][i] = 32*1024*1024
            host['DiskWrite'][i] = 1024*1024
            host['DiskRead'][i] = 1024*1024
            host['NetworkIn'][i] = 1024*1024
            host['NetworkOut'][i] = 1024*1024
        elif tmp == 2:
            host['hostType'][i] = 'medium'
            host['CPU'][i] = 2200*16
            host['Mem'][i] = 64*1024*1024
            host['DiskWrite'][i] = 1024*1024
            host['DiskRead'][i] = 1024*1024
            host['NetworkIn'][i] = 1024*1024
            host['NetworkOut'][i] = 1024*1024
        elif tmp == 3:   
            host['hostType'][i] = 'large'
            host['CPU'][i] = 2200*32
            host['Mem'][i] = 128*1024*1024
            host['DiskWrite'][i] = 1024*1024
            host['DiskRead'][i] = 1024*1024
            host['NetworkIn'][i] = 1024*1024
            host['NetworkOut'][i] = 1024*1024
        time.sleep(0.01)
        pbar.update(i+1)

    pbar.finish()
    return host

#hosts = genHostCluster(4,4)
#print(hosts)
#print(hosts['CPU'][1])

