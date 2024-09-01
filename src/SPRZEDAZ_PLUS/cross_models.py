
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score

def cross_models_LR(dataset, workers, X_names, Y_names):
	models = {}
	scores = {}
	for worker in workers:
		data = dataset[dataset['WORKER']==worker]
		models[worker] = linear_model.LinearRegression()

		scores[worker] = cross_val_score(models[worker], data[X_names], data[Y_names], cv=5) 
		scores[worker] = scores[worker].mean()	

	return scores
	
def cross_models_RF(dataset, workers, X_names, Y_names):
        models = {}
        scores = {}
        for worker in workers:
                data = dataset[dataset['WORKER']==worker]
                models[worker] = RandomForestRegressor(max_depth=5, n_estimators=100)

                scores[worker] = cross_val_score(models[worker], data[X_names], data[Y_names], cv=5)
                scores[worker] = scores[worker].mean()

        return scores

def cross_models_SVM2(dataset, workers, X_names, Y_names):
	models = {}
	scores = {}
	for worker in workers:
		data = dataset[dataset['WORKER']==worker]
		models[worker] = SVR(kernel='poly', C=1e3, degree=2)

		scores[worker] = cross_val_score(models[worker], data[X_names], data[Y_names], cv=5)
		scores[worker] = scores[worker].mean()

	return scores

def cross_models_SVMrbf(dataset, workers, X_names, Y_names):
        models = {}
        scores = {}
        for worker in workers:
                data = dataset[dataset['WORKER']==worker]
                models[worker] = SVR(kernel='rbf', C=1e3)

                scores[worker] = cross_val_score(models[worker], data[X_names], data[Y_names], cv=5)
                scores[worker] = scores[worker].mean()

        return scores

def cross_models_AdaTREE(dataset, workers, X_names, Y_names):
	models = {}
	scores = {}
	for worker in workers:
		data = dataset[dataset['WORKER']==worker]
		models[worker] = AdaBoostRegressor(base_estimator=DecisionTreeRegressor(max_depth=5), n_estimators=10)

		scores[worker] = cross_val_score(models[worker], data[X_names], data[Y_names], cv=5)
		scores[worker] = scores[worker].mean()
	
	return scores

def cross_models_AdaLR(dataset, workers, X_names, Y_names):
	models = {}
	scores = {}
	for worker in workers:
		data = dataset[dataset['WORKER']==worker]
		models[worker] = AdaBoostRegressor(base_estimator=linear_model.LinearRegression(), n_estimators=100)
	
		scores[worker] = cross_val_score(models[worker], data[X_names], data[Y_names], cv=5)
		scores[worker] = scores[worker].mean()

	return scores
