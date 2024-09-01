from sklearn.model_selection import cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

classifiers = {
	'KN':KNeighborsClassifier(3),
	'SVM':SVC(kernel='linear',C=0.025),
	'SVMrbf':SVC(gamma=2,C=1),
	'RF':RandomForestClassifier(max_depth=5, n_estimators=10),
	'MLP':MLPClassifier(alpha=1),
	'Ada':AdaBoostClassifier()
	}
classifiers_name = classifiers.keys()

def trainCL(dataset, workers, X_names, Y_names, Bestmodel):
	models = {}
#	print (dataset)
	for worker in workers:
		data = dataset[dataset['WORKER']==worker]
		models[worker] = classifiers[Bestmodel[worker]].fit(data[X_names], data[Y_names])

	return models

def scoreCVCL(dataset, workers, X_names, Y_names):
	scores = {}
	for k, cls in classifiers.items():
		score = {} 
		for worker in workers:
			data = dataset[dataset['WORKER']==worker]
			score[worker] = cross_val_score(cls, data[X_names], data[Y_names], cv=5)
			score[worker] = score[worker].mean()
		scores[k] = score
#	print (scores)
	out = {}
	for worker in workers:
		ll = {x:scores[x][worker] for x in scores.keys()}
		out[worker] = max(ll, key=ll.get)
	return out

def selectRF(workers):
	out = {worker : 'RF' for worker in workers}
	return out
