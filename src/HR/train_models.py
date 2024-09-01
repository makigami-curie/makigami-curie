
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor

def train_models_LR(dataset, worker, X_names, Y_names):
	data = dataset[dataset['WORKER']==worker]
	model = linear_model.LinearRegression()

	model.fit(data[X_names], data[Y_names])

	return model
	
def train_models_RF(dataset, worker, X_names, Y_names):
        data = dataset[dataset['WORKER']==worker]
        model = RandomForestRegressor(max_depth=5, n_estimators=100)

        model.fit(data[X_names], data[Y_names])
        return model

def train_models_SVM2(dataset, worker, X_names, Y_names):
	data = dataset[dataset['WORKER']==worker]
	model = SVR(kernel='poly', C=1e3, degree=2)

	model.fit(data[X_names],data[Y_names]) 
	return model

def train_models_SVMrbf(dataset, worker, X_names, Y_names):
        data = dataset[dataset['WORKER']==worker]
        model = SVR(kernel='rbf', C=1e3)

        model.fit(data[X_names],data[Y_names])
        return model

def train_models_AdaTREE(dataset, worker, X_names, Y_names):
	data = dataset[dataset['WORKER']==worker]
	model = AdaBoostRegressor(base_estimator=DecisionTreeRegressor(max_depth=5), n_estimators=10)

	model.fit(data[X_names],data[Y_names])

	return model

def train_models_AdaLR(dataset, worker, X_names, Y_names):
	data = dataset[dataset['WORKER']==worker]
	model = AdaBoostRegressor(base_estimator=linear_model.LinearRegression(), n_estimators=100)
	
	model.fit(dataset[X_names],dataset[Y_names])

	return model
