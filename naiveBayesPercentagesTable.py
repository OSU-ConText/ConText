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
with open('percentages_data.csv', 'r') as f:
    reader = csv.reader(f)
    labels = next(reader)
    labels.pop(0)
    next(reader)  # skip the header row
    data = [row for row in reader]

# split data into features and labels
X = [[float(row[i]) for i in range(1, len(row)-1)] for row in data]
y = [str(row[0]) for row in data]

# split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


# train a Gaussian Naive Bayes model
gnb = GaussianNB()
gnb.fit(X_train, y_train)

# predict the labels for the test data
y_pred = gnb.predict(X_test)

# compute the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

#compute f1 score
#weighted average of the precision and recall
f1 = f1_score(y_pred, y_test, average="weighted")
print("F1 score: ", f1)

#there's a warning when you run this if you try to get f1 scores for cases where parameters in ytest don't appear in ypred
print(classification_report(y_test, y_pred))

#precision: accuracy of predictions, when we predict a language how often is the prediction correct
#recall/hit rate: fraction of correctly identified predictions (what fraction of translation lang decisions were the actual translation lang decision)
#f1: measures precision and recall at the same time by finding the harmonic mean of the two values
#accuracy: accuracy of all predictions
#support: the number of occurrences of each class in your y_test