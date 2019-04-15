import numpy as np
import pandas as pd
from sklearn import datasets

print("Loading Iris Dataset")
iris = datasets.load_iris()
df = pd.DataFrame(data= np.c_[iris['data'], iris['target']], columns= iris['feature_names'] + ['target'])

print("Saving Iris Dataset")
df.to_pickle("./data/iris-data.pkl")
