
import csv
import gnbValidation 
from joblib import dump, load

if __name__ == '__main__':
    KN_partial_langs = load('AI_model_pkl_files\kNearest_partial_langs_and_id.pkl')
    with open('csv_files/new_partial_langs_and_ids.csv', 'r') as f:
        reader = csv.reader(f)
        labels = next(reader)
        #first_column = reader.columns[0]
        data = list(reader)
    X = [[(float(row[i])) for i in range(1, len(row))] for row in data]
    y = [str(row[0]) for row in data]
    gnbValidation.create_confusion_matrix(KN_partial_langs, X, y)
    gnbValidation.print_proba(KN_partial_langs)