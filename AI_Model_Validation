from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import numpy as np
import csv
from sklearn.model_selection import cross_val_score, KFold
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
from joblib import dump, load
from sklearn.metrics import accuracy_score
import languages
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score


def cross_validation(model, X, y):
    print("Cross Validation: ")

    k_folds = 5
    # Define the cross-validation method
    cv_method = KFold(n_splits=k_folds, shuffle=True, random_state=42)
    # Perform k-fold cross-validation
    cv_scores = cross_val_score(model, X, y, cv=cv_method, scoring='accuracy')

    # Print the cross-validation scores
    print('Cross-validation scores:', cv_scores)
    print('Mean accuracy:', np.mean(cv_scores))

def accuracy(model, X, y):
    print("Accuracy: ")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    # predict the labels for the test data
    y_pred = model.predict(X_test)

    # compute the accuracy of the model
    accuracy = accuracy_score(y_test, y_pred)
    print(accuracy)

def confusion_matrix(model, X, y):
    #confustion matrix
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    y_pred = model.predict(X_test)
    mat = confusion_matrix(y_test, y_pred)
    labels = list(languages.LANGUAGES.keys())
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cm = ax.matshow(mat)
    # plot the title, use y to leave some space before the labels
    plt.title("Confusion matrix - langs and ids", y=1.2)
    ax.set_xticklabels([''] + labels)
    ax.set_yticklabels([''] + labels)
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right", rotation_mode="anchor")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    # Loop over data dimensions and create text annotations.
    for i in range(len(mat)):
        for j in range(len(mat)):
            text = ax.text(j, i, mat[i, j],
                        ha="center", va="center", color="w")
        # Create colorbar
    fig.colorbar(cm)
    plt.show()

def find_f1_score(model, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    y_pred = model.predict(X_test)
        
    score = f1_score(y_test, y_pred, average="macro")
    print("Macro F1-Score: ", score)

    score = f1_score(y_test, y_pred, average="micro")
    print("Micro F1-Score: ", score)

    score = f1_score(y_test, y_pred, average="weighted")
    print("Weighted F1-Score: ", score)
        

def validate_partial_langs_and_id(model):
    #partial_langs_and_id_validation
    # open the CSV file
    with open('csv_files/partial_langs_and_id_data.csv', 'r') as f:
        reader = csv.reader(f)
        labels = next(reader)
        #first_column = reader.columns[0]
        data = list(reader)
    X = [[(float(row[i])) for i in range(1, len(row)-1)] for row in data]
    y = [str(row[0]) for row in data]

    #run validations
    cross_validation(model, X, y)
    accuracy(model, X, y)
    #confusion_matrix(gnb_partial_langs, X, y)
    find_f1_score(model, X, y)

def validate_all_langs_and_id(model):
    #all_langs_and_id_validation
    # open the CSV file
    with open('csv_files/all_langs_and_id_data.csv', 'r') as f:
        reader = csv.reader(f)
        labels = next(reader)
        #first_column = reader.columns[0]
        data = list(reader)
    X = [[(float(row[i])) for i in range(1, len(row)-1)] for row in data]
    y = [str(row[0]) for row in data]

    #run validations
    cross_validation(model, X, y)
    accuracy(model, X, y)
    #confusion_matrix(gnb_partial_langs, X, y)
    find_f1_score(model, X, y)

if __name__ == '__main__':
    print("GNB model with partial langs and id data: ")
    gnb_partial_langs = load('AI_model_pkl_files/gnb_partial_langs_and_id.pkl')
    validate_partial_langs_and_id(gnb_partial_langs)

    print("K Nearest model with partial langs and id data: ")
    kNearest_partial_langs = load('AI_model_pkl_files/kNearest_partial_langs_and_id.pkl')
    validate_partial_langs_and_id(kNearest_partial_langs)

    print("Decision Tree model with partial langs and id data: ")
    decision_tree_partial_langs = load('AI_model_pkl_files/decision_tree_partial_langs_and_id.pkl')
    validate_partial_langs_and_id(decision_tree_partial_langs)

    print("GNB model with all langs and id data: ")
    gnb_all_langs = load('AI_model_pkl_files/gnb_all_langs_and_id.pkl')
    validate_all_langs_and_id(gnb_all_langs)

    print("K Nearest model with all langs and id data: ")
    kNearest_all_langs = load('AI_model_pkl_files/kNearest_all_langs_and_id.pkl')
    validate_all_langs_and_id(kNearest_all_langs)

    print("Decision Tree model with all langs and id data: ")
    decision_tree_all_langs = load('AI_model_pkl_files/decision_tree_all_langs_and_id.pkl')
    validate_all_langs_and_id(decision_tree_all_langs)