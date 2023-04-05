from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import languages
import pandas as pd
import numpy as np
import csv
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    f1_score,
    classification_report,
)

# open the CSV file
with open('all_langs_and_id_data.csv', 'r') as f:
    reader = csv.reader(f)
    labels = next(reader)
    labels.pop(0)
    next(reader)  # skip the header row
    data = [row for row in reader]

# split data into features and labels
X = [[(float(row[i]) + 1) for i in range(2, len(row)-1)] for row in data]
y = [str(row[1]) for row in data]
# split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# train a Gaussian Naive Bayes model
gnb = GaussianNB()
gnb.fit(X_train, y_train)

# predict the labels for the test data
y_pred = gnb.predict(X_test)

# compute the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

print(f"Number of mislabeled points out of a total {np.asarray(X_test).shape[0]} points: {(y_test != y_pred).sum()}")
