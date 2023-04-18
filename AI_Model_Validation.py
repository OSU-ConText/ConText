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
from sklearn import metrics

#runs a k-fold cross validation on a model
#pass in a saved AI model, parameters, and labels
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

#calculates the accuracy of a models predictions
#pass in a saved AI model, parameters, and labels
def accuracy(model, X, y):
    print("Accuracy: ")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    # predict the labels for the test data
    y_pred = model.predict(X_test)

    # compute the accuracy of the model
    accuracy = accuracy_score(y_test, y_pred)
    print(accuracy)

def compare_accuracy(model, X, y):
    print("Accuracy: ")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    # predict the labels for the test data
    y_pred_model = model.predict(X_test)

    y_pred_train = model.predict(X_train)

    # compute the accuracy of the model
    model_accuracy = accuracy_score(y_test, y_pred_model)
    train_accuracy = accuracy_score(y_train, y_pred_train)
    print("model accuracy: ", model_accuracy)
    print("training data accuracy: ", train_accuracy)


#creates a confusion matrix for the model
#pass in a saved AI model, parameters, and labels
def confusion_matrix(model, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    y_pred = model.predict(X_test)

    confusion_matrix = metrics.confusion_matrix(y_test, y_pred)

    cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = list(languages.LANGUAGES.keys()))

    cm_display.plot()
    plt.show() 

#calculates the f1 score of a models predictions
#pass in a saved AI model, parameters, and labels
def find_f1_score(model, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    y_pred = model.predict(X_test)
        
    score = f1_score(y_test, y_pred, average="macro")
    print("Macro F1-Score: ", score)

    score = f1_score(y_test, y_pred, average="micro")
    print("Micro F1-Score: ", score)

    score = f1_score(y_test, y_pred, average="weighted")
    print("Weighted F1-Score: ", score)
        
#runs all validations above on model using partial_langs_and_id_data.csv
#pass in a saved AI model
def validate_partial_langs_and_id(model):
    #partial_langs_and_id_validation
    # open the CSV file
    with open('csv_files/lang_subset_with_nones.csv', 'r') as f:
        reader = csv.reader(f)
        labels = next(reader)
        #first_column = reader.columns[0]
        data = list(reader)
    X = [[(float(row[i])) for i in range(1, len(row))] for row in data]
    y = [str(row[0]) for row in data]

    #run validations
    cross_validation(model, X, y)
    accuracy(model, X, y)
    confusion_matrix(model, X, y)
    find_f1_score(model, X, y)
    compare_accuracy(model, X, y)

#runs all validations above on model using all_langs_and_id_data.csv
#pass in a saved AI model
def validate_all_langs_and_id(model):
    #all_langs_and_id_validation
    # open the CSV file
    with open('csv_files/all_langs_and_id_data.csv', 'r') as f:
        reader = csv.reader(f)
        labels = next(reader)
        #first_column = reader.columns[0]
        data = list(reader)
    X = [[(float(row[i])) for i in range(1, len(row))] for row in data]
    y = [str(row[0]) for row in data]

    #run validations
    cross_validation(model, X, y)
    accuracy(model, X, y)
    confusion_matrix(model, X, y)
    find_f1_score(model, X, y)
    compare_accuracy(model, X, y)

#calls all validations on saved models
if __name__ == '__main__':
    #print("GNB model with partial langs and id data: ")
    #gnb_partial_langs = load('AI_model_pkl_files/gnb_partial_langs_and_id.pkl')
    #validate_partial_langs_and_id(gnb_partial_langs)

    #print("K Nearest model with partial langs and id data: ")
    #kNearest_partial_langs = load('AI_model_pkl_files/kNearest_partial_langs_and_id.pkl')
    #validate_partial_langs_and_id(kNearest_partial_langs)

    #print("Decision Tree model with partial langs and id data: ")
    #decision_tree_partial_langs = load('AI_model_pkl_files/decision_tree_partial_langs_and_id.pkl')
    #validate_partial_langs_and_id(decision_tree_partial_langs)

    #print("GNB model with all langs and id data: ")
    #gnb_all_langs = load('AI_model_pkl_files/gnb_all_langs_and_id.pkl')
    #validate_all_langs_and_id(gnb_all_langs)

    #print("K Nearest model with all langs and id data: ")
    #kNearest_all_langs = load('AI_model_pkl_files/kNearest_all_langs_and_id.pkl')
    #validate_all_langs_and_id(kNearest_all_langs)

    #print("Decision Tree model with all langs and id data: ")
    #decision_tree_all_langs = load('AI_model_pkl_files/decision_tree_all_langs_and_id.pkl')
    #validate_all_langs_and_id(decision_tree_all_langs)

    print("Random Forest model with partial langs and id data: ")
    random_forest_partial_langs = load('AI_model_pkl_files/random_forest_partial_langs_and_id.pkl')
    validate_partial_langs_and_id(random_forest_partial_langs)