import xlrd
import numpy as np
import os
# 打开文件
filePath = 'trace\\'
x = 0
filename = os.listdir(filePath)
numVM = len(filename)
vmTrace = np.zeros((numVM,11,288))
for fileName in filename:
    print('loading the trace of the ',x+1,'th VM. The file name is ',fileName,'.')
    data = xlrd.open_workbook('trace\\'+fileName)    
    table = data.sheet_by_name('Sheet1')
    if table.nrows>=288:
        #row = table.nrows
        row = 288
        #col = table.ncols
        col = 11
        vm = np.zeros((row, col))
        for i in range(row):
            rows = np.matrix(table.row_values(i))
            vm[i,:] = rows
            #print(vm[i,:])
        vmTrace[x,:,:] = vm.transpose()
    else:
        print('this trace is invalid!') 
    x = x+1
#print(vm1[1,:])

