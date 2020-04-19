import torch
import numpy as np
import pandas as pd
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import matplotlib.pyplot as plt
from torch.autograd import Variable,function

from tensorboardX import SummaryWriter

##author:veritas xu
##time:2018/3/7
#设计深度学习P230页图10.3计算循环网络

#########################################
##      与自带RNN输入输出维度相同       ####
##    seq_len(T)  batch   feature   ####
#########################################
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

class computeRNN(nn.Module):
    def __init__(self,in_feature,hidden_size,n_class):
        super(computeRNN, self).__init__()
        self.in_feature=in_feature
        self.hidden_size=hidden_size
        self.n_class=n_class
        self.in2hidden=nn.Linear(in_feature+self.hidden_size,self.hidden_size)
        self.hidden2out=nn.Linear(self.hidden_size,self.n_class)
        self.tanh=nn.Tanh()
        self.softmax=nn.Softmax(dim=1)

    ##此处input的尺寸为[seq_len,batch,in_feature]
    def forward(self,input,pre_state):
        T=input.shape[0]
        batch=input.shape[1]
        # a=Variable(torch.zeros(T,batch,self.hidden_size))             #a-> [T,hidden_size]
        # o=Variable(torch.zeros(T,batch,self.n_class))                 #o ->[T,n_class]
        predict_y=Variable(torch.zeros(T,batch,self.n_class))
        # pre_state = Variable(torch.zeros(batch, self.hidden_size))  # pre_state=[batch,hidden_size]


        if pre_state is None:
            pre_state = Variable(torch.zeros(batch, self.hidden_size)).to(device)  # hidden ->[batch,hidden_size]

        for t in range(T):
            # input:[T,batch,in_feature]
            tmp = torch.cat((input[t], pre_state), 1)  #  [batch,in_feature]+[batch,hidden_size]-> [batch,hidden_size+in_featue]
            a = self.in2hidden(tmp)                      #  [batch,hidden_size+in_feature]*[hidden_size+in_feature,hidden_size] ->[batch,hidden_size]
            hidden = self.tanh(a)

            #这里不赋值的话就没有代表隐层向前传递
            pre_state = hidden

            o = self.hidden2out(hidden)  # [batch,hidden_size]*[hidden_size,n_class]->[batch,n_class]
            #由于此次是一个单分类问题，因此不用softmax函数
            if self.n_class == 1:
                predict_y[t] = F.sigmoid(o)
            else:
                predict_y[t] = self.softmax(o)


        return predict_y, hidden

def RNN(path, resIndx, timeframe):
#定义训练集
#data_csv = pd.read_csv('D:/Study/code/RNN-master/data.csv',usecols=[1])
    data = pd.read_csv(path,usecols=[resIndx])
    data_csv = data[0:timeframe]
    print(data_csv.shape)
    data_csv = data_csv.dropna()
    data_set = data_csv.values
    data_set = data_set.astype('float32')
    max_value = np.max(data_set)
    scalar = max_value
    data_set = list(map(lambda x: x / scalar, data_set))
# print(data_set)

#def create_dataset(dataset, look_back=2):

    dataX, dataY = [], []
    look_back=2
    for i in range(len(data_set) - look_back):
        a = data_set[i:(i + look_back)]
        dataX.append(a)
        dataY.append(data_set[i + look_back])
    #return np.array(dataX), np.array(dataY)
    data_X = np.array(dataX)
    data_Y = np.array(dataY)

# 创建好输入输出
#data_X, data_Y = create_dataset(data_set)
# print(data_X)
#print(data_X)
#print(data_Y)

# 划分训练集和测试集，70% 作为训练集
    train_size = int(len(data_X) * 0.9)
    test_size = len(data_X) - train_size
    train_X = data_X[:train_size]
    train_Y = data_Y[:train_size]
    test_X = data_X[train_size:]
    test_Y = data_Y[train_size:].astype('float32')
    print('train_x:'+str(train_X.shape))
    print('train_y:'+str(train_Y.shape))
    print('test_X:'+str(test_X.shape))
    train_X = train_X.reshape(-1, 4, 2)
    train_Y = train_Y.reshape(-1, 4, 1)
#train_X = train_X.reshape(-1,1,2)
#train_Y = train_Y.reshape(-1,1,1)
    test_X = test_X.reshape(-1, 1, 2)
    print('train_x:'+str(train_X.shape))
    print('train_y:'+str(train_Y.shape))
    print('test_X:'+str(test_X.shape))

    train_x = Variable(torch.from_numpy(train_X)).to(device)
    train_y = Variable(torch.from_numpy(train_Y)).to(device)
    test_x = Variable(torch.from_numpy(test_X)).to(device)
#print(train_x[0])
#print(train_y[0])

    input_size = 2       #一个序列的长度,也就是输入特征数
    n_hidden = 12      #隐层神经元数目
    target_size = 1     #输出的尺寸
    rnn = computeRNN(in_feature=input_size,hidden_size=n_hidden,n_class=target_size)
    rnn.to(device)
    optimizer = optim.Adam(rnn.parameters(),lr=0.016)
    loss_fun = nn.MSELoss()
    loss_fun.to(device)

    num_epoch = 1000
# print(len(train_x))
#
    for epoch in range(num_epoch):
        state = None
        out, state = rnn(train_x, state)
        out = out.to(device)
        loss = loss_fun(out,train_y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    #if (epoch + 1) % 100 == 0:  # 每 100 次输出结果
    #    print('Epoch: {}, Loss: {:.5f}'.format(epoch + 1, loss.data[0]))
    # state = None
# #
    rnn.eval()
    hidden1 = None
    out2,_=rnn(train_x,hidden1)
#print(out2.data.numpy().reshape(88,1)*scalar)
#print(train_Y.reshape(2,1)*scalar)
    plt.plot(out2.data.numpy().reshape(88,1))
    plt.plot(train_Y.reshape(88,1))
    plt.show()
    return out2.data.numpy().reshape(88,1)*scalar

path = 'D:/Study/code/RNN-master/data.csv'
resIndx = 1
timeframe = 100
out = RNN(path, resIndx, timeframe)
