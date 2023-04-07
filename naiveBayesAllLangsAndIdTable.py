from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import numpy as np
import csv
from sklearn.model_selection import cross_val_score, KFold
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# open the CSV file
with open('partial_langs_and_id_data.csv', 'r') as f:
    reader = csv.reader(f)
    labels = next(reader)
    labels.pop(0)
    next(reader)  # skip the header row
    data = [row for row in reader]

# split data into features and labels
X = [[(float(row[i])) for i in range(2, len(row)-1)] for row in data]

y = [str(row[1]) for row in data]
# split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# train a Gaussian Naive Bayes model
gnb = GaussianNB()

k_folds = 5

# Define the cross-validation method
cv_method = KFold(n_splits=k_folds, shuffle=True, random_state=42)

# Perform k-fold cross-validation
cv_scores = cross_val_score(gnb, X, y, cv=cv_method, scoring='accuracy')

# Print the cross-validation scores
print('Cross-validation scores:', cv_scores)
print('Mean accuracy:', np.mean(cv_scores))

#gnb.fit(X_train, y_train)

# predict the labels for the test data
#y_pred = gnb.predict(X_test)

# compute the accuracy of the model
#accuracy = accuracy_score(y_test, y_pred)
#print("Accuracy:", accuracy)

#confustion matrix
#mat = metrics.confusion_matrix(y_test, y_pred)
#labels = list(languages.LANGUAGES.keys())
#print(labels)
#fig = plt.figure()
#ax = fig.add_subplot(111)
#cm = ax.matshow(mat)
# plot the title, use y to leave some space before the labels
#plt.title("Confusion matrix - langs and ids", y=1.2)
#ax.set_xticklabels([''] + labels)
#ax.set_yticklabels([''] + labels)
#plt.setp(ax.get_xticklabels(), rotation=-30, ha="right", rotation_mode="anchor")
#plt.xlabel("Predicted")
#plt.ylabel("Actual")
# Loop over data dimensions and create text annotations.
#for i in range(len(mat)):
    #for j in range(len(mat)):
        #text = ax.text(j, i, mat[i, j],
                       #ha="center", va="center", color="w")
    # Create colorbar
#fig.colorbar(cm)
#plt.show()

#print(f"Number of mislabeled points out of a total {np.asarray(X_test).shape[0]} points: {(y_test != y_pred).sum()}")
