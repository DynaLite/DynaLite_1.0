import numpy as np
import pandas as pd
import scipy as sp
import sklearn as sk
import sklearn.cross_validation as skcv
import sklearn.ensemble as skens
import sklearn.metrics as skmetric
import sklearn.naive_bayes as sknb
import sklearn.tree as sktree
import matplotlib.pyplot as plt
import pydot_ng as pydot
import sklearn.externals.six as sksix
import IPython.display as ipd
from sklearn.preprocessing import OneHotEncoder

def train(data_fn):
	df = pd.read_csv(data_fn)

	enc = OneHotEncoder()
	enc.fit(df.ix[:,0:5])
	df_transformed = enc.transform(df.ix[:,0:5]).toarray()

	dt_model = sktree.DecisionTreeClassifier( criterion='entropy')

	dt_model.fit(df_transformed, df.ix[:,6])
	return dt_model

def predict(model, x):
	enc = OneHotEncoder()
	enc.fit(x)
	x_transformed = enc.transform(x).toarray()

	return model.predict(x_transformed)
