
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
import matplotlib.pyplot as plt

LR = 0.0005

class RNN(nn.Module):
	def __init__(self, n_input, n_hidden1, n_output):
		super(RNN, self).__init__()
		self.lstm1 = nn.LSTM(n_input, n_hidden1)
		self.lstm2 = nn.LSTM(n_hidden1, n_hidden1)
		self.lstm3 = nn.LSTM(n_hidden1, n_output)
		self.p = 0.5

	def forward(self, seq, hc = None):
		out = []
		if hc == None:
			hc1, hc2, hc3 = None, None, None
		else:
			nc1, hc2, hc3 = hc
		x_in = torch.unsqueeze(seq[0],0)
		for x in seq.chunk(seq.size(0), dim=0):
			if np.random.rand()>self.p:
				x_in = x
			tmp, hc1 = self.lstm1(x_in, hc1)
			tmp, hc2 = self.lstm2(tmp, hc2)
			x_in, hc3 = self.lstm3(tmp, hc3)
			out.append(x_in)
		return torch.stack(out).squeeze(1), (hc1, hc2, hc3)

rnn = RNN(n_input=1, n_hidden1=64, n_output=1)
optimizer = optim.Adam(rnn.parameters(), lr=LR)
loss = nn.MSELoss()

plt.figure(1, figsize=(12,5))
plt.ion()

for step in range(1000):
	data = np.sin(np.linspace(0,10,4)+.2*np.pi*np.random.rand())
	xs = np.linspace(0,10,4)
	xs = data[:-1]
	ys = data[1:]

	X = Variable(torch.Tensor(xs).view(-1,1,1))
	Y = Variable(torch.Tensor(ys))
	if step%100==0:
		rnn.p = min(rnn.p+.01,0.85)

	optimizer.zero_grad()
	lstm_out,_ = rnn(X)
#	print(lstm_out[20:].squeeze(1).squeeze(1))
	ls = loss(lstm_out[:].view(-1),Y[:])
	ls.backward()

	optimizer.step()

	if step%10==0:
		print(step, ls.data.numpy()) 
		plt.cla()
		plt.plot(xs,ys, 'r-')
		plt.plot(xs, lstm_out.view(-1).data.numpy(),'b-')
		#plt.draw()
		plt.pause(0.05)

plt.ioff()
plt.show()
	
