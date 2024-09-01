
import torch
from torch.autograd import Variable
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import pylab as pl
import torch.nn.init as init
import torch.nn as nn

import matplotlib.pyplot as plt

dtype = torch.FloatTensor
n_input, n_hidden, n_output = 1, 32, 1
epochs = 1000
seq_length = 20
lr = 0.001

class RNN(nn.Module):
        
	def __init__(self, n_input, n_hidden, n_output):
                
		super (RNN, self).__init__()

		self.n_hidden = n_hidden
		self.n_output = n_output

		self.hidden1 = nn.Linear(n_input+n_output, n_hidden)
		self.hidden2 = nn.Linear(n_hidden, n_hidden)
		self.hidden3 = nn.Linear(n_hidden, n_output)
        
	def forward(self, input, context):
#               print(input.size(), hidden.size())
#               combined = torch.cat((input, hidden),0)#torch.cat((input, hidden),0)
#		combined = torch.Tensor(np.append(input, co)).float()
                
#		combined = torch.cat(input, context)
		combined = torch.tensor([input, context])
#		print(combined.size(), hidden.size())
#               print(len(combined))
		tmp = F.relu(self.hidden1(combined))
		tmp = F.relu(self.hidden2(tmp))
		output = self.hidden3(tmp)

		return output, output

	def initHidden(self):
		return torch.zeros(1, self.n_output)

rnn = RNN(n_input=n_input, n_hidden=n_hidden, n_output=n_output)


data_time_steps = np.linspace(2, 10, seq_length + 1)
data = np.sin(data_time_steps)
data.resize((seq_length + 1, 1))

X = Variable(torch.Tensor(data[:-1]).type(dtype), requires_grad=False)
Y = Variable(torch.Tensor(data[1:]).type(dtype), requires_grad=False)
optimizer = optim.Adam(rnn.parameters(), lr=lr)
LOSS=nn.MSELoss()

plt.ion()

for step in range(epochs):
	total_loss = 0
	contex = Variable(torch.zeros(1, 1),1) 

	for j in range(X.size(0)):

		optimizer.zero_grad()

		input = X[j:(j+1)]
		target = Y[j:(j+1)]
		pred, contex = rnn(input, contex)
		loss = (pred - target).pow(2).sum()/2

		total_loss += loss
		loss.backward()
		
		optimizer.step()

		contex = Variable(contex.data)

	if step%10==0:
		print(step, total_loss.data[0])
		
		plt.cla()
		contex = Variable(torch.zeros(1,1),1)
		preds = []
		for i in range(X.size(0)):
			input = X[i:i+1]
			pred, contex = rnn(input, contex)
			preds.append(pred.data.numpy().ravel()[0])
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
