#create a dictionary of languages for each parameter and each languages count in the training data
param_one_lang_is_decision = {}
param_two_lang_is_decision = {}
param_three_lang_is_decision = {}
#dictionary for number of times a lang appears in all data
overall_langs = {}


def find_freq_table(data):
    for key in data:
        values = data[key]
        #dictionary with first param matching translation decision
        if key is values[0]:
            if param_one_lang_is_decision.get(values[0]) is not None:
                param_one_lang_is_decision[key] += 1
            else:
                param_one_lang_is_decision[key] = 1
        #dictionary with second param matching translation decision
        if key is values[1]:
            if param_two_lang_is_decision.get(values[1]) is not None:
                param_two_lang_is_decision[key] += 1
            else:
                param_two_lang_is_decision[key] = 1
        #dictionary with third param matching translation decision
        if key is values[2]:
            if param_three_lang_is_decision.get(values[2]) is not None:
                param_three_lang_is_decision[key] += 1
            else:
                param_three_lang_is_decision[key] = 1

    print(param_one_lang_is_decision)
    print(param_two_lang_is_decision)
    print(param_three_lang_is_decision)


#test separating data by class
data = {"da": ["am","da","da"],
        "am": ["am","am","am"],
        "af": ["af","sn","af"],
        "vi": ["vi","vi","vi"],
        "ug": ["af","ug","ug"],
        "af": ["af","af","af"]}
find_freq_table(data)

#need to have nested tuples for repeating af results.