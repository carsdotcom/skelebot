import pickle
import argparse
import numpy as np
import pandas as pd
from argparse import RawTextHelpFormatter
from sklearn.linear_model import LinearRegression

# READ ARGS and PARAMS
parser = argparse.ArgumentParser(description="train", formatter_class=RawTextHelpFormatter)
parser.add_argument("algorithm")
parser.add_argument("-n", "--name")
args = parser.parse_args()

filename = "./models/{name}.pkl".format(name=args.name)

print("Loading Iris Data")
df = pd.read_pickle("./data/iris-data.pkl")

if ("glm" == args.algorithm):
    print("Fitting GLM")
    model = LinearRegression(fit_intercept=False)
    model.fit(df[['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']], df['target'])

    print("Saving Model")
    pickle.dump(model, open(filename, 'wb'))
else:
    print("ALGORITHM NOT YET SUPPORTED")
