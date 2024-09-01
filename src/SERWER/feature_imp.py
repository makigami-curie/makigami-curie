from select_model import train
from select_modelCL import trainCL, selectRF
from load_json import load_json_all
from clean_data import clean_data

def feature_imp(self,dataset):
        Bestmodel = selectRF(self.workers)
        try:
            self.models = train(dataset, self.workers, self.X_names, self.Y_names, Bestmodel)
        except:
           self.models = trainCL(dataset, self.workers, self.X_names, self.Y_names, Bestmodel)
        imp = dict()
        for name in self.DUMMIS_names:
            imp[name]=[0,0]
        for name in self.X_names:
            name_NO = False
            for n in self.DUMMIS_names:
                if n in name:
                   name_NO = True
            if not name_NO:
                imp[name]=[0,0]
#               print (self.DUMMIS_names)
        for worker in self.workers:
            importances = self.models[worker].feature_importances_
        for feature in zip(imp.keys(), importances): 
            n = feature[0]
            for name in self.DUMMIS_names:
                if name in feature[0]: n = name
            imp [n][0] += feature[1]
            imp [n][1] += 1
#		print(feature)
		
        imp_ret = list()
        imp_dict = dict()
        for key, values in sorted(imp.items(), key=lambda x: x[1][0]/x[1][1] ,reverse=True ):
            imp_ret.append((key,values[0]/values[1]))
            imp_dict[key] = values[0]/values[1]

        return imp_ret, imp_dict
	
#	print (imp)

def compute_importance (model, f):
        dataset =  load_json_all(f)
        dataset, model.workers, model.X_names, model.Y_names, model.SKIP_names, model.DUMMIS_names, model.sc = clean_data(dataset, model.TARGET)
        imp, imp_dict = feature_imp(model, dataset)

        return imp, imp_dict

