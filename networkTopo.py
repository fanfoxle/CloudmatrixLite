import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
import sys
import time
from progressbar import ProgressBar, Bar, Percentage

def fatTree(n):
    """Standard fat tree topology
    n: number of pods
    total n^3/4 hosts
    """
    topo = nx.Graph()
    num_of_hosts_per_edge_switch = n // 2
    num_of_edge_switches = n // 2
    numHost = n * (n // 2) * (n // 2)
    num_of_aggregation_switches = num_of_edge_switches
    num_of_core_switches = int((n / 2) * (n / 2))

    host = np.zeros(numHost, dtype={
        'names':('layer1Indx', 'layer0Indx', 'hostType', 'CPU', 'Mem', 'DiskWrite', 'DiskRead', 'NetworkIn', 'NetworkOut'),
        'formats':('i4','i4','U10', 'f4', 'f4','f4','f4','f4','f4')
    })

    # generate topo pod by pod
    x = 0
    for i in range(n):
        for j in range(num_of_edge_switches):
            topo.add_node("Pod {} edge switch {}".format(i, j))
            topo.add_node("Pod {} aggregation switch {}".format(i, j))
            for k in range(num_of_hosts_per_edge_switch):                
                #tmp = random.randint(1,3)
                tmp = 1
                if tmp == 1:
                    host['layer1Indx'][x] = i
                    host['layer0Indx'][x] = j
                    host['hostType'][x] = 'small'
                    host['CPU'][x] = 2200*8
                    host['Mem'][x] = 32*1024*1024
                    host['DiskWrite'][x] = 1024
                    host['DiskRead'][x] = 1024
                    host['NetworkIn'][x] = 1024
                    host['NetworkOut'][x] = 1024
                elif tmp == 2:
                    host['podIndx'][x] = i
                    host['aggregationswitchIndx'][x] = j
                    host['hostType'][x] = 'medium'
                    host['CPU'][x] = 2200*16
                    host['Mem'][x] = 64*1024*1024
                    host['DiskWrite'][x] = 2048
                    host['DiskRead'][x] = 2048
                    host['NetworkIn'][x] = 2048
                    host['NetworkOut'][x] = 2048
                elif tmp == 3:
                    host['podIndx'][x] = i
                    host['aggregationswitchIndx'][x] = j   
                    host['hostType'][x] = 'large'
                    host['CPU'][x] = 2200*32
                    host['Mem'][x] = 128*1024*1024
                    host['DiskWrite'][x] = 4096
                    host['DiskRead'][x] = 4096
                    host['NetworkIn'][x] = 4096
                    host['NetworkOut'][x] = 4096            
                topo.add_node("Pod {} edge switch {} host {}".format(
                    i, j, k))
                topo.add_edge(
                    "Pod {} edge switch {}".format(i, j),
                    "Pod {} edge switch {} host {}".format(i, j, k))
                x = x + 1
    print('there are '+str(numHost)+' hosts.')

    # add edge among edge and aggregation switch within pod
    for i in range(n):
        for j in range(num_of_aggregation_switches):
            for k in range(num_of_edge_switches):
                topo.add_edge("Pod {} aggregation switch {}".format(i, j),
                              "Pod {} edge switch {}".format(i, k))

    # add edge among core and aggregation switch
    num_of_core_switches_connected_to_same_aggregation_switch = num_of_core_switches // num_of_aggregation_switches
    for i in range(num_of_core_switches):
        topo.add_node("Core switch {}".format(i))
        aggregation_switch_index_in_pod = i // num_of_core_switches_connected_to_same_aggregation_switch
        for j in range(n):
            topo.add_edge(
                "Core switch {}".format(i),
                "Pod {} aggregation switch {}".format(
                    j, aggregation_switch_index_in_pod))

    topo.name = 'fattree'
    return topo, host



def bcube_topo(n):
    """Standard Bcube topology
    k: layers
    n: num of hosts
    total n ^ (k+1) hosts
    """
    k = 2 
    topo = nx.Graph()
    numHost = n**(k + 1)
    #print('there are '+str(numHost)+' hosts.')
    host = np.zeros(numHost, dtype={
        'names':('layer1Indx', 'layer0Indx', 'hostType', 'CPU', 'Mem', 'DiskWrite', 'DiskRead', 'NetworkIn', 'NetworkOut'),
        'formats':('i4','i4','U10', 'f4', 'f4','f4','f4','f4','f4')
    })
    # add host first
    for i in range(numHost):
        topo.add_node("host {}".format(i))

    # add switch by layer
    num_of_switches = int(numHost / n)
    for i in range(k + 1):
        index_interval = n**i
        num_of_one_group_switches = n**i
        for j in range(num_of_switches):
            topo.add_node("Layer {} Switch {}".format(i, j))
            start_index_host = j % num_of_one_group_switches + (
                j // num_of_one_group_switches) * num_of_one_group_switches * n
            for k in range(n):
                host_index = start_index_host + k * index_interval
                #tmp = random.randint(1,3)
                tmp = 1
                if tmp == 1:
                    host['layer1Indx'][host_index] = i
                    host['layer0Indx'][host_index] = j
                    host['hostType'][host_index] = 'small'
                    host['CPU'][host_index] = 2200*8
                    host['Mem'][host_index] = 32*1024*1024
                    host['DiskWrite'][host_index] = 1024
                    host['DiskRead'][host_index] = 1024
                    host['NetworkIn'][host_index] = 1024
                    host['NetworkOut'][host_index] = 1024
                elif tmp == 2:
                    host['podIndx'][host_index] = i
                    host['aggregationswitchIndx'][host_index] = j
                    host['hostType'][host_index] = 'medium'
                    host['CPU'][host_index] = 2200*16
                    host['Mem'][host_index] = 64*1024*1024
                    host['DiskWrite'][host_index] = 2048
                    host['DiskRead'][host_index] = 2048
                    host['NetworkIn'][host_index] = 2048
                    host['NetworkOut'][host_index] = 2048
                elif tmp == 3:
                    host['podIndx'][host_index] = i
                    host['aggregationswitchIndx'][host_index] = j   
                    host['hostType'][host_index] = 'large'
                    host['CPU'][host_index] = 2200*32
                    host['Mem'][host_index] = 128*1024*1024
                    host['DiskWrite'][host_index] = 4096
                    host['DiskRead'][host_index] = 4096
                    host['NetworkIn'][host_index] = 4096
                    host['NetworkOut'][host_index] = 4096
                topo.add_edge("host {}".format(host_index),
                              "Layer {} Switch {}".format(i, j))

    topo.name = 'Bcube'
    return topo, host



def vl2_topo(port_num_of_aggregation_switch=4, port_num_of_tor_for_host=3):
    """Standard vl2 topology
    total port_num_of_aggregation_switch^2 / 4 * port_num_of_tor_for_host hosts
    """
    topo = nx.Graph()
    num_of_aggregation_switches = port_num_of_aggregation_switch
    num_of_intermediate_switches = num_of_aggregation_switches // 2
    num_of_tor_switches = (port_num_of_aggregation_switch //
                           2) * (port_num_of_aggregation_switch // 2)

    # create intermediate switch
    for i in range(num_of_intermediate_switches):
        topo.add_node("Intermediate switch {}".format(i))

    # create aggregation switch
    for i in range(num_of_aggregation_switches):
        topo.add_node("Aggregation switch {}".format(i))
        for j in range(num_of_intermediate_switches):
            topo.add_edge("Aggregation switch {}".format(i),
                          "Intermediate switch {}".format(j))

    # create ToR switch
    num_of_tor_switches_per_aggregation_switch_can_connect = num_of_aggregation_switches // 2
    for i in range(num_of_tor_switches):
        topo.add_node("ToR switch {}".format(i))
        # every ToR only need to connect 2 aggregation switch
        aggregation_index = (
            i // num_of_tor_switches_per_aggregation_switch_can_connect) * 2
        topo.add_edge("ToR switch {}".format(i),
                      "Aggregation switch {}".format(aggregation_index))
        aggregation_index += 1  # The second aggregation switch
        topo.add_edge("ToR switch {}".format(i),
                      "Aggregation switch {}".format(aggregation_index))
        # add host to ToR
        for j in range(port_num_of_tor_for_host):
            #print('this is the '+str(j)+'th host of the '+str(i)+'th ToR.')
            host_index = i*port_num_of_tor_for_host + j
            tmp = 1
            if tmp == 1:
                host['layer1Indx'][host_index] = i
                host['layer0Indx'][host_index] = j
                host['hostType'][host_index] = 'small'
                host['CPU'][host_index] = 2200*8
                host['Mem'][host_index] = 32*1024*1024
                host['DiskWrite'][host_index] = 1024
                host['DiskRead'][host_index] = 1024
                host['NetworkIn'][host_index] = 1024
                host['NetworkOut'][host_index] = 1024
            elif tmp == 2:
                host['podIndx'][host_index] = i
                host['aggregationswitchIndx'][host_index] = j
                host['hostType'][host_index] = 'medium'
                host['CPU'][host_index] = 2200*16
                host['Mem'][host_index] = 64*1024*1024
                host['DiskWrite'][host_index] = 2048
                host['DiskRead'][host_index] = 2048
                host['NetworkIn'][host_index] = 2048
                host['NetworkOut'][host_index] = 2048
            elif tmp == 3:
                host['podIndx'][host_index] = i
                host['aggregationswitchIndx'][host_index] = j   
                host['hostType'][host_index] = 'large'
                host['CPU'][host_index] = 2200*32
                host['Mem'][host_index] = 128*1024*1024
                host['DiskWrite'][host_index] = 4096
                host['DiskRead'][host_index] = 4096
                host['NetworkIn'][host_index] = 4096
                host['NetworkOut'][host_index] = 4096
            topo.add_node("ToR switch {} host {}".format(i, j))
            topo.add_edge("ToR switch {} host {}".format(i, j),
                          "ToR switch {}".format(i))

    topo.name = 'VL2'
    return topo, host_index

topo,host = bcube_topo(3)

nx.draw(topo, with_labels=True, font_size=10, node_size=200)

plt.show()
#print(hosts)
#print(hosts['CPU'][1])
