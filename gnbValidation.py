import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd
import languages
from sklearn.model_selection import cross_val_score, KFold
from sklearn.decomposition import PCA
from joblib import dump, load
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn import metrics

#creates a confusion matrix for the model
#pass in a saved AI model, parameters, and labels
def create_confusion_matrix(model, X, y):
    #confustion matrix
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    y_pred = model.predict(X_test)

    confusion_matrix = metrics.confusion_matrix(y_test, y_pred)

    cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = list(languages.LANGUAGES.keys()))

    cm_display.plot()
    plt.show()  

def print_proba(model, X_test):
    for test in X_test:
        print("params ")
        print(test)
        print("predictions")
        probas = model.predict_log_proba([test])
        print(probas)
        print(model.predict([test]))
        print("max num")
        print(probas.max())
    #prediction_lang = model.predict(params)
    #print(predictions)
    #print(prediction_lang)

if __name__ == '__main__':
    gnb_partial_langs = load('AI_model_pkl_files/gnb_partial_langs_and_id.pkl')
    knearest_partial_langs = load('AI_model_pkl_files/kNearest_partial_langs_and_id.pkl')
    with open('csv_files/new_partial_langs_and_ids.csv', 'r') as f:
        reader = csv.reader(f)
        labels = next(reader)
        #first_column = reader.columns[0]
        data = list(reader)
    X = [[(float(row[i])) for i in range(1, len(row))] for row in data]
    y = [str(row[0]) for row in data]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    #create_confusion_matrix(gnb_partial_langs, X, y)
    print_proba(gnb_partial_langs, X_test)