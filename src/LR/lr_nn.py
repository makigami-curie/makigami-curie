
import numpy as np
import pandas as pd
import re
from sklearn.metrics import mean_squared_error, r2_score

from sklearn.preprocessing import scale, LabelEncoder

import matplotlib.pyplot as plt

import torch
from torch.autograd import Variable
import torch.nn.functional as F

#liczba opuszczanych kolumn od przodu
skip_cols = 2
#Wczytanie danych
dataset = pd.read_csv('text',header=0, delimiter=" ")#, usecols=range(skip_cols,16))

#kolumny do opuszczenia
skip_columns = [x for x in range(0,skip_cols)]
#kolumny z datami
date_columns = []
for index, ww in enumerate(dataset.iloc[0]):
	if re.search(r'....-..-..', str(ww)) :
		date_columns.append(index)
skip_columns = skip_columns+date_columns
#wyrzuczanie kolumn
dataset = dataset.drop(dataset.columns[skip_columns],1)


#kolumny dla dummis variables
char_columns = dataset.dtypes.pipe(lambda x: x[x=='object']).index
bool_columns = dataset.dtypes.pipe(lambda x: x[x=='bool']).index
dummis_columns = list(char_columns)+list(bool_columns)
#sortowanie nie jest potrzebne
dummis_columns.sort()

#nazwy zmiennych
names = dataset.columns.values
Y_names = names[-1]

for col in names:
	if (dataset[col].dtype != 'object') and (dataset[col].dtype !='bool'):
		dataset[col] = scale(dataset[col])
#tworzenie zmienncy dummis
le = LabelEncoder()
for col in dummis_columns:
	le.fit(dataset[col])
	dataset[col] = le.transform(dataset[col])
dataset = pd.get_dummies(dataset, columns=dummis_columns) 


#liczba rekordow
N_data = len(dataset)

#print(dataset.corr()['TIME'])

train = dataset.sample(frac=.75, random_state=1)
test = dataset.loc[~dataset.index.isin(train.index)]

#nazwy kolumn po wyrzucaniu
names = dataset.columns.values
X_names = np.setdiff1d(names,Y_names)

X_train = train[X_names]
#.as_matrix().astype('float')
#X_train = X_train.reshape(-1,len(X_names))
X_train = torch.tensor(X_train.values).float()
Y_train = train[Y_names]
Y_train = torch.tensor(Y_train.values).float().view((-1,1))

X_test = torch.tensor(test[X_names].values).float()
Y_test = test[Y_names]

class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden = torch.nn.Linear(n_feature, n_hidden)   # hidden layer
        self.predict = torch.nn.Linear(n_hidden, n_output)   # output layer

    def forward(self, x):
        x = F.relu(self.hidden(x))      # activation function for hidden layer
        x = self.predict(x)             # linear output
        return x

net = Net(n_feature=len(X_names), n_hidden=100, n_output=1)     # define the network
print(net)  # net architecture

optimizer = torch.optim.Adam(net.parameters(), lr=0.2)
loss_func = torch.nn.MSELoss()  # this is for regression mean squared loss

plt.ion()   # something about plotting

for t in range(200):
    prediction = net(X_train)     # input x and predict based on x

    loss = loss_func(prediction, Y_train)     # must be (1. nn output, 2. target)

    optimizer.zero_grad()   # clear gradients for next train
    loss.backward()         # backpropagation, compute gradients
    optimizer.step()        # apply gradients

    if t % 5 == 0:
        # plot and show learning process
        plt.cla()
        plt.scatter(X_train[:,6].data.numpy(), Y_train.data.numpy())
        plt.scatter(X_train[:,6].data.numpy(), prediction.data.numpy(), c='r')
        plt.text(0.5, 0, 'Loss=%.4f' % loss.data[0], fontdict={'size': 20, 'color':  'red'})
        plt.pause(0.1)

    print(t, loss[0])
    if loss < 0.01: break
plt.ioff()
plt.show()

plt.ion()   # something about plotting

prediction = net(X_test)
#print(reg.coef_)
print(mean_squared_error(Y_test, prediction.detach()))
print(r2_score(Y_test, prediction.detach()))
'''
plt.scatter(X_test['LP'], Y_test, color='black')
plt.scatter(X_test['LP'], Y_pred, color='blue', linewidth=3)

#usuniecie skali na osich
#plt.xticks(())
#plt.yticks(())

plt.show()
'''
