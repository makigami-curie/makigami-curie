from load_json import load_json_all
from clean_data import clean_data
#from train_models import *
from load_job import load_job
from select_model import scoreCV, train, selectLR
from select_modelCL import scoreCVCL, trainCL, selectRF

#from feature_imp import feature_imp

class MODEL:
	def __init__ (self):
		self.models = dict()		#dict of models for workers
		self.setDF = dict()		
		self.workers = 0		#list of workers
		self.X_names = 0		#columns names of features
		self.Y_names = 0		#column name of value
		self.SKIP_names = 0		#columns names what was skiped
		self.DUMMIS_names = 0	#columns names of dummis variables
		self.sc = 0			
		self.queue = dict()		#cumulative time for worker

		self.MODEL_SELECTION = False
		self.TARGET = 'TIME'

	def learn(self, f):
		dataset =  load_json_all(f)
		dataset, self.workers, self.X_names, self.Y_names, self.SKIP_names, self.DUMMIS_names, self.sc = clean_data(dataset, self.TARGET)
		if self.MODEL_SELECTION:
			Bestmodel = scoreCV(dataset, self.workers, self.X_names, self.Y_names)
		else:
			Bestmodel = selectLR(self.workers) 	
	#		Bestmodel = selectRF(self.workers)
		self.models = train(dataset, self.workers, self.X_names, self.Y_names, Bestmodel)
		
#		feature_imp(self, dataset)
#		imp = dict()
#		for name in self.DUMMIS_names:
#			imp[name]=0
##		print (self.DUMMIS_names)
#		for worker in self.workers:
#			importances = self.models[worker].feature_importances_
#		for feature in zip(self.X_names, importances): 
#			for name in self.DUMMIS_names:
#				if name in feature[0]: n = name
#			imp [n] += feature[1]
#		for key, values in sorted(imp.items(), key=lambda x: x[1] ,reverse=True ):
#			print (key,":",values)
#		print (imp)

		self.setDF = dataset.head(1)
		self.setDF = self.setDF.drop(self.setDF.index)

		self.queue_reset()

        
	def learnCL(self, f):
		dataset =  load_json_all(f)
		dataset, self.workers, self.X_names, self.Y_names, self.SKIP_names, self.DUMMIS_names, self.sc = clean_data(dataset, self.TARGET)
		if self.MODEL_SELECTION:
			Bestmodel = scoreCVCL(dataset, self.workers, self.X_names, self.Y_names)
		else:
			Bestmodel = selectRF(self.workers)
                	
		self.models = trainCL(dataset, self.workers, self.X_names, self.Y_names, Bestmodel)
                
		self.setDF = dataset.head(1)
		self.setDF = self.setDF.drop(self.setDF.index)
                
		self.queue_reset()

	def predict(self, f):
		workers_time, _ = load_job (f, self.workers, self.TARGET, self.X_names, self.SKIP_names, self.DUMMIS_names, self.sc, self.setDF, self.models)
		return workers_time, self.check_queue(workers_time)
	def predictCL (self, f):
		workers_time, _ = load_job (f, self.workers, self.TARGET, self.X_names, self.SKIP_names, self.DUMMIS_names, self.sc, self.setDF, self.models)
		return workers_time[self.workers[0]]
#		return workers_time	

	def queue_reset(self):
		self.queue = {worker:0 for worker in self.workers}

	def check_queue(self, workers_time):
		times = {worker:self.queue[worker] + workers_time[worker] for worker in self.workers}

		BESTworker = min(times, key=times.get)
		self.queue[BESTworker] = times[BESTworker]
		
		return BESTworker


