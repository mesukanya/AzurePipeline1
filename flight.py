#import pickle
import csv
import pandas as pd
#import numpy as np
from sklearn.linear_model import LinearRegression
#from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Creating the dataframe
df = pd.read_csv("/home/admin1/Desktop/Flightdata/flights_dataset.csv")

# First grouping based on "Team"
# Within each team we are grouping based on "Position"


gkk = df.groupby(["searchTerms", "gl"])
print('gkk',gkk.first())



