import pickle
import argparse
import pandas as pd
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description="train", formatter_class=RawTextHelpFormatter)
parser.add_argument("-n", "--name")
parser.add_argument("-o", "--output")
args = parser.parse_args()

filename = "./models/{name}.pkl".format(name=args.name)
outfile  = "./scored/{output}.pkl".format(output=args.output)

print("Loading The Model ({})".format(filename))
model = pickle.load(open(filename, "rb" ) )

print("Scoring")
Xnew = [[0.79415228, 2.10495117, 0.79415228, 2.10495117]]
ynew = model.predict(Xnew)
results = "X={val}, Predicted={pred}\n".format(val=Xnew[0], pred=ynew[0])

print("Saving Results ({})".format(outfile))
text_file = open(outfile, "w")
text_file.write(results)
text_file.close()
