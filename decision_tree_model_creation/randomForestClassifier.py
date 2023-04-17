from sklearn import tree
from sklearn.model_selection import train_test_split
import numpy as np
import csv
from sklearn.model_selection import cross_val_score, KFold
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
from joblib import dump, load
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification


# open the CSV file
with open('csv_files/new_partial_langs_and_ids.csv', 'r') as f:
    reader = csv.reader(f)
    labels = next(reader)
    data = list(reader)

# split data into features and labels
X = [[(float(row[i])) for i in range(1, len(row))] for row in data]

y = [str(row[0]) for row in data]

# split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#train a random forest model
X, y = make_classification(n_samples=1000, n_features=12,n_informative=2, n_redundant=0,random_state=0, shuffle=False)

rf = RandomForestClassifier()
rf.fit(X_train, y_train)

# save model to a file
dump(rf, 'AI_model_pkl_files/random_forest_partial_langs_and_id.pkl')