
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from torch.autograd import Variable
import matplotlib.pyplot as plt

LR = 0.0005
N_HIDDEN = 32

class RNN (nn.Module):
	def __init__(self, n_input, n_hidden, n_output):
		super (RNN, self).__init__()

		self.n_hidden = n_hidden
		self.n_output = n_output

		self.hidden1 = nn.Linear(n_input+n_output, n_hidden)
		self.hidden2 = nn.Linear(n_hidden, n_hidden)
		self.hidden3 = nn.Linear(n_hidden, n_output)

	def forward(self, input, hidden):
#		print(input.size(), hidden.size())
#		combined = torch.cat((input, hidden),0)#torch.cat((input, hidden),0)
		combined = torch.Tensor(np.append(input, hidden)).float()
		print(combined.size(), hidden.size())
#		print(len(combined))
		tmp = self.hidden1(combined)
		tmp = self.hidden2(tmp)
		output = self.hidden3(tmp)
		
		return output

	def initHidden(self):
		return torch.zeros(1, self.n_output)

rnn = RNN(n_input=1, n_hidden=N_HIDDEN, n_output=1)

optimizer = optim.Adam(rnn.parameters(), lr=LR)
loss = nn.MSELoss()


plt.figure(1, figsize=(12,5))
plt.ion()



X = np.array([np.pi*.01*i for i in range(100)])
Y =  np.sin(X) 
rnn_out = rnn.initHidden()
rnn_out = torch.zeros(1,100)

for step in range(1000):
	optimizer.zero_grad()
         
	for i in range(1,len(X)+1):
		rnn_out[0][i] = rnn(X[i-1], rnn_out[0][i-1])
   
	ls = loss(rnn_out,Y)
	ls.backward()
         
	optimizer.step()
	if step%10==0:
		print(step, ls.data.numpy())
#		plt.cla()
#		plt.plot(X,Y, 'r-')
#		plt.plot(X, rnn_out.view(-1).data.numpy(),'b-')
                #plt.draw()
#		plt.pause(0.05)

plt.ioff()
#plt.show()

