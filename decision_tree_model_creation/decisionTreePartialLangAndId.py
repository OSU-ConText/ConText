from sklearn import tree
from sklearn.model_selection import train_test_split
import numpy as np
import csv
from sklearn.model_selection import cross_val_score, KFold
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
from joblib import dump, load


# open the CSV file
with open('csv_files/lang_subset_with_nones.csv', 'r') as f:
    reader = csv.reader(f)
    labels = next(reader)
    data = list(reader)

# split data into features and labels
X = [[(float(row[i])) for i in range(1, len(row))] for row in data]

y = [str(row[0]) for row in data]

# split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# train a Decision Tree model
tree = tree.DecisionTreeClassifier()

tree.fit(X_train, y_train)

# save model to a file
dump(tree, 'AI_model_pkl_files/decision_tree_partial_langs_and_id.pkl')

