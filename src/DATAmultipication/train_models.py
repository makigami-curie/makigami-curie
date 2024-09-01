
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor


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

