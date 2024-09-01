
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor

def train_models_LR(dataset, workers, X_names, Y_names):
	models = {}
	for worker in workers:
		data = dataset[dataset['WORKER']==worker]
		models[worker] = linear_model.LinearRegression()

		models[worker].fit(data[X_names], data[Y_names])

	return models
	
def train_models_RF(dataset, workers, X_names, Y_names):
        models = {}
        for worker in workers:
                data = dataset[dataset['WORKER']==worker]
                models[worker] = RandomForestRegressor(max_depth=5, n_estimators=100)

                models[worker].fit(data[X_names], data[Y_names])

        return models

def train_models_SVM2(dataset, workers, X_names, Y_names):
	models = {}
	for worker in workers:
		data = dataset[dataset['WORKER']==worker]
		models[worker] = SVR(kernel='poly', C=1e3, degree=2)

		models[worker].fit(data[X_names],data[Y_names]) 
	return models

def train_models_SVMrbf(dataset, workers, X_names, Y_names):
        models = {}
        for worker in workers:
                data = dataset[dataset['WORKER']==worker]
                models[worker] = SVR(kernel='rbf', C=1e3)

                models[worker].fit(data[X_names],data[Y_names])
        return models

def train_models_AdaTREE(dataset, workers, X_names, Y_names):
	models = {}
	for worker in workers:
		data = dataset[dataset['WORKER']==worker]
		models[worker] = AdaBoostRegressor(base_estimator=DecisionTreeRegressor(max_depth=5), n_estimators=10)

		models[worker].fit(data[X_names],data[Y_names])

	return models

def train_models_AdaLR(dataset, workers, X_names, Y_names):
	models = {}
	for worker in workers:
		data = dataset[dataset['WORKER']==worker]
		models[worker] = AdaBoostRegressor(base_estimator=linear_model.LinearRegression(), n_estimators=100)
	
		models[worker].fit(dataset[X_names],dataset[Y_names])

	return models
