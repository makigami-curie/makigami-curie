
import torch
from torch.autograd import Variable
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import pylab as pl
import torch.nn.init as init
import torch.nn as nn

import random

import matplotlib.pyplot as plt

dtype = torch.FloatTensor
n_input, n_hidden, n_output, n_history = 1, 64, 1, 4
n_param = 1
epochs = 7000
seq_length = 20
lr = 0.0001
err = 0.01

class RNN(nn.Module):
        
	def __init__(self, n_input, n_hidden, n_output, n_history, n_param):
                
		super (RNN, self).__init__()

		self.n_hidden = n_hidden
		self.n_output = n_output
		self.n_history= n_history
		self.n_param  = n_param

		self.hidden1 = nn.Linear(n_input+n_history+n_param, n_hidden)
		self.hidden2 = nn.Linear(n_hidden, n_hidden)
	#	self.hidden2a= nn.Linear(n_hidden, n_hidden)
		self.hidden3 = nn.Linear(n_hidden, n_output)
        
	def forward(self, input, context, param):
		combined2 = input
		b = list(param)
		b.extend(list(context.view(-1)))
		b.append(input)
		combined2 = torch.tensor(b)
		tmp = F.relu(self.hidden1(combined2))
		tmp = F.relu(self.hidden2(tmp))
	#	tmp = F.relu(self.hidden2a(tmp))
		output = self.hidden3(tmp)

		return output, output

	def initHidden(self):
		return torch.zeros(1, self.n_history)

def learn_rnn( n_input, n_hidden, n_output, n_history, n_param):
#PRZEKAZAC INPUT DO UCZENIA, PARAMETRY
rnn = RNN(n_input=n_input, n_hidden=n_hidden, n_output=n_output, n_history=n_history, n_param=n_param)


data_time_steps = np.linspace(2, 10, seq_length + 1)
data = np.sin(data_time_steps)
data.resize((seq_length + 1, 1))

param = list(range(n_param))
#X = Variable(torch.Tensor(data[:-1]).type(dtype), requires_grad=False)
X = Variable(torch.Tensor(data_time_steps[1:]).type(dtype), requires_grad=False)
Y = Variable(torch.Tensor(data[1:]).type(dtype), requires_grad=False)
#print(len(X))
#print(len(Y))
optimizer = optim.Adam(rnn.parameters(), lr=lr)
LOSS=nn.MSELoss()

plt.ion()

for step in range(epochs):
	total_loss = 0
	contex = Variable(torch.zeros(n_history, 1),1) 
	con = 0
	
	if step%4 == 0:
		data = np.sin(data_time_steps)
		param[0]=0
	if step%4 == 1:
		data = np.power(data_time_steps, 2)
		param[0]=1
	if step%4 == 2:
		data = np.cos(data_time_steps)
		param[0]=2
	if step%4 == 3:
		data = - np.power(data_time_steps, 3)
		param[0]=3
	
	data.resize((seq_length + 1, 1))
	Y = Variable(torch.Tensor(data[1:]).type(dtype), requires_grad=False)
	for i in range(X.size(0)):
		Y[i] = Y[i] + (random.random()*2. -1.)*err

	for j in range(X.size(0)):

		optimizer.zero_grad()

		input = X[j:(j+1)] 
		target = Y[j:(j+1)]
		pred, con = rnn(input, contex, param)
		#print(contex)
		#print (pred, con)
		try:
			contex[0:n_history-1] = contex[1:n_history]
		except:
			pass
		contex[n_history-1,0] = con
		

		loss = (pred - target).pow(2).sum()/2
#		print('aa',loss, pred, target)

		total_loss += loss
		loss.backward()
		
		optimizer.step()

		contex = Variable(contex.data)

	if step%21==0:
		print(step, total_loss.data[0])
		
		plt.cla()
		contex = Variable(torch.zeros(n_history,1),1)
		preds = []
		for i in range(X.size(0)):
			input = X[i:i+1]
			pred, con = rnn(input, contex, param)
			preds.append(pred.data.numpy().ravel()[0])
			try:
				contex[0:n_history-1] = contex[1:n_history]
			except:
				pass
			contex[n_history-1,0] = con
		plt.plot(X.view(-1).numpy(), Y.view(-1).numpy(), 'b-')
		plt.plot(X.view(-1).numpy(), preds, 'r-')
		plt.pause(0.05)

"""
contex = Variable(torch.zeros(1,1),1)
preds = []
for i in range(X.size(0)):
	input = X[i:i+1]
	pred, contex = rnn(input, contex)
	preds.append(pred.data.numpy().ravel()[0])

print(preds,Y.view(-1).numpy())

plt.plot(X.view(-1).numpy(), Y.view(-1).numpy(), 'b-')
plt.plot(X.view(-1).numpy(), preds, 'r-')
"""
plt.show()
