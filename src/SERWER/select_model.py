from train_models import *
from cross_models import *

def train(dataset, workers, X_names, Y_names, Bestmodel):
	models = {}
	for worker in workers:
		if Bestmodel[worker] == 'LR': 
			models[worker] = train_models_LR(dataset, worker, X_names, Y_names) #linear regresion
		if Bestmodel[worker] == 'RF': 
			models[worker] = train_models_RF(dataset, worker, X_names, Y_names) #random forest
		if Bestmodel[worker] == 'SVM2': 
			models[worker] = train_models_SVM2(dataset, worker, X_names, Y_names) #SVM poly 2
		if Bestmodel[worker] == 'SVMrbf': 
			models[worker] = train_models_SVMrbf(dataset, worker, X_names, Y_names) #SVM rbf
		if Bestmodel[worker] == 'AdaTree': 
			models[worker] = train_models_AdaTREE(dataset, worker, X_names, Y_names) #Adaboost with tree
		if Bestmodel[worker] == 'AdaLR': 
			models[worker] = train_models_AdaLR(dataset, worker, X_names, Y_names) #Adaboost with linear regresion
	return models

def scoreCV(dataset, workers, X_names, Y_names):
	scores = {}

	scores['LR'] = cross_models_LR(dataset, workers, X_names, Y_names) #linear regresion
	scores['RF'] = cross_models_RF(dataset, workers, X_names, Y_names) #random forest
	scores['SVM2'] = cross_models_SVM2(dataset, workers, X_names, Y_names) #SVM poly 2
	scores['SVMrbf'] = cross_models_SVMrbf(dataset, workers, X_names, Y_names) #SVM rbf
	scores['AdaTree'] = cross_models_AdaTREE(dataset, workers, X_names, Y_names) #Adaboost with tree
	scores['AdaLR'] = cross_models_AdaLR(dataset, workers, X_names, Y_names) #Adaboost with linear regresion

	out = {}
	for worker in workers:
		ll = {x:scores[x][worker] for x in scores.keys()}
		out[worker] = max(ll, key=ll.get)
	return out

def selectLR(workers):
	out = {worker : 'LR' for worker in workers}
	return out
