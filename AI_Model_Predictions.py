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

def open_csv(csv_name):
    with open(csv_name, 'r') as f:
            reader = csv.reader(f)
            labels = next(reader)
            #first_column = reader.columns[0]
            data = list(reader)
    X = [[(float(row[i])) for i in range(1, len(row))] for row in data]
    y = [str(row[0]) for row in data]
    run_models(X, y)

def run_models(X, y):
    run_gnb(X, y)
    run_decisionTree(X, y)
    run_kNearest(X, y)

def run_gnb(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    gnb_partial_langs = load('AI_model_pkl_files/gnb_partial_langs_and_id.pkl')
    y_pred = gnb_partial_langs.predict(X_test)
    model_accuracy = accuracy_score(y_test, y_pred)
    print("model accuracy: ", model_accuracy)
     
def run_decisionTree(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    decision_tree_partial_langs = load('AI_model_pkl_files/decision_tree_partial_langs_and_id.pkl')
    y_pred = decision_tree_partial_langs.predict(X_test)
    y_pred_train = decision_tree_partial_langs.predict(X_train)
    model_accuracy = accuracy_score(y_test, y_pred)
    #train_accuracy = accuracy_score(y_train, y_pred_train)
    print("model accuracy: ", model_accuracy)
    #print("training data accuracy:: ", train_accuracy)
     
def run_kNearest(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    kNearest_partial_langs = load('AI_model_pkl_files/kNearest_partial_langs_and_id.pkl')
    y_pred = kNearest_partial_langs.predict(X_test)
    model_accuracy = accuracy_score(y_test, y_pred)
    print("model accuracy: ", model_accuracy)

def trim_index(csv_file, df):
    first_column = df.columns[0]
    df = df.drop([first_column], axis=1)
    df.to_csv(csv_file, index=False)
     
if __name__ == '__main__':
    csv_file = input("Enter name of csv file:\n")
    df = pd.read_csv(csv_file)
    trim_index(csv_file, df)
    #open_csv(csv_file)
