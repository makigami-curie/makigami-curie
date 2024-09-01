from flask import Flask, request, Response
import json
import sys
from feature_imp import compute_importance

from models import MODEL

import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

models = dict()
targets = dict()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/learn/', methods=['Post'])
def learn():
	global models
	f = request.get_json()
	model = MODEL()
#	model.MODEL_SELECTION = True#False
	try:
		model.PredWorker = f['predworker']=='True'
	except:
		model.PredWorker=True
	try:
		model.TARGET = f['target']
	except:
		model.TARGET = 'TIME'
	
	model.learn(f)
	models[f['id']] = model
	return success_response("LEARNED")

@app.route('/learnCL/', methods=['Post'])
def learnCL():
	global models
	f = request.get_json()
	print (f)
	model = MODEL()
#        model.MODEL_SELECTION = True#False
	try:
		model.TARGET = f['target']
	except:
		model.TARGET = 'KUPNO'
	model.learnCL(f)
	models[f['id']] = model
	return success_response("LEARNED")

@app.route('/feature_importances/', methods=['Post'])
def feature_importances():
        f = request.get_json()
        model = MODEL()
        try:
                model.PredWorker = f['predworker']=='True'
        except:
                model.PredWorker=True
        try:
                model.TARGET = f['target']
        except:
                model.TARGET = 'TIME'

        imp, imp_dict = compute_importance(model, f)
        imp_pd = pd.DataFrame.from_dict(imp_dict,orient="index")
        print(imp_dict)
        print(imp_pd)

        imp_pd.plot(kind='barh')
        plt.show()

        return success_response(str(imp))

@app.route('/predict/', methods=['Post'])
def predict():
	f = request.get_json()
	if f['id'] in models:
		workers_time, worker = models[f['id']].predict(f)
		print(worker, workers_time)
		if models[f['id']].PredWorker:
			return success_response( str(worker))
		else:
			return success_response( str(workers_time[worker]))
	else :
		message = {
			'message': 'Id Not Found: '+str(f['id'])
		}
		js = json.dumps(message)
		return Response(js, status=412)	
@app.route('/predictCL/', methods=['Post'])
def predictCL():
	f = request.get_json()
	if f['id'] in models:
		classCL = models[f['id']].predictCL(f)
		return success_response(str(classCL))
	else:
		message = {
			'message' : 'Id Not Founs: ' +str(f['id'])
		}
		js = json.dumps(message)
		return Response(js, status=412)


@app.route('/resetqueue/',methods=['PUT'])
def resetqueue():
	global models
	f = request.get_json()
	if f['id'] in models:
		models[f['id']].queue_reset()
		return success_response("ok")
	else:
		message = {
			'message': 'Id Not Found: '+str(f['id'])
		}
		js = json.dumps(message)
		return Response(js, status=412)

@app.route('/resetqueue/',methods=['POST'])
def resetqueueALL():
	global models
	for f in models:
		models[f].queue_reset()
	return success_response("ok")

@app.route('/set_target/', methods=['PUT'])
def set_target():
	global targets
	f = request.get_json()
	targets[f['id']] = f['target']
	return success_response("ok")

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Not Found: ' + request.url,
    }
    js = json.dumps(message)

    return Response(js, status=404)


def success_response(js=None):

    return Response(js, status=200, mimetype='application/json')


if __name__ == '__main__':
	app.run(threaded=True)
