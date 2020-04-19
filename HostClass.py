import numpy as np
import random

def genHostCluster(numHost):
    host = np.zeros(numHost, dtype={
        'names':('hostType', 'CPU', 'Mem', 'DiskWrite', 'DiskRead', 'NetworkIn', 'NetworkOut'),
        'formats':('U10', 'f4', 'f4','f4','f4','f4','f4')
    })
    for i in range(0,numHost):
        tmp = random.randint(1,3)
        if tmp == 1:
            host['hostType'][i] = 'small'
            host['CPU'][i] = 1024
            host['Mem'][i] = 1024
            host['DiskWrite'][i] = 1024
            host['DiskRead'][i] = 1024
            host['NetworkIn'][i] = 1024
            host['NetworkOut'][i] = 1024
        elif tmp == 2:
            host['hostType'][i] = 'medium'
            host['CPU'][i] = 2048
            host['Mem'][i] = 2048
            host['DiskWrite'][i] = 2048
            host['DiskRead'][i] = 2048
            host['NetworkIn'][i] = 2048
            host['NetworkOut'][i] = 2048
        elif tmp == 3:   
            host['hostType'][i] = 'large'
            host['CPU'][i] = 4096
            host['Mem'][i] = 4096
            host['DiskWrite'][i] = 4096
            host['DiskRead'][i] = 4096
            host['NetworkIn'][i] = 4096
            host['NetworkOut'][i] = 4096

    return host

host = genHostCluster(3)
print(host)