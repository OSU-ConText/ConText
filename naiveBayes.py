#dictionary for each parameter
#counts how many times the parameter lang = decision lang
param_one_lang_is_decision = {}
param_two_lang_is_decision = {}
param_three_lang_is_decision = {}

#dictionary for each parameters
#counts how many times the parameter lang occurs
param_one_lang = {}
param_two_lang = {}
param_three_lang = {}

#conditional probabilities for each parameter
cp_param_one = {}
cp_param_two = {}
cp_param_three = {}

#list of all lang decisions
all_langs = []

#overall probability for each class
overall_prob_langs = {}

#posterior probability for each class
posterior_prob_langs = {}

# Split the dataset by class values, returns a dictionary
def separate_by_class(dataset):
    separated = {}
    for i in range(len(dataset)):
        list = dataset[i]
        class_value = list[-1]
        list.pop()
        if (class_value not in separated):
            separated[class_value] = []
        separated[class_value].append(list)
    return separated

#fill param = lang decision dictionaries
def find_freq_table(decision, param_list):
    #dictionary with first param matching translation decision
    if decision is param_list[0]:
        if param_one_lang_is_decision.get(decision) is not None:
            param_one_lang_is_decision[decision] += 1
        else:
            param_one_lang_is_decision[decision] = 1
    #dictionary with second param matching translation decision
    if decision is param_list[1]:
        if param_two_lang_is_decision.get(decision) is not None:
            param_two_lang_is_decision[decision] += 1
        else:
            param_two_lang_is_decision[decision] = 1
    #dictionary with third param matching translation decision
    if decision is param_list[2]:
        if param_three_lang_is_decision.get(decision) is not None:
            param_three_lang_is_decision[decision] += 1
        else:
            param_three_lang_is_decision[decision] = 1

#fill parameter lang count dictionaries
def find_total_lang_instance(param_list):
    if param_one_lang.get(param_list[0]) is not None:
        param_one_lang[param_list[0]] += 1
    else:
        param_one_lang[param_list[0]] = 1
    if param_two_lang.get(param_list[1]) is not None:
        param_two_lang[param_list[1]] += 1
    else:
        param_two_lang[param_list[1]] = 1
    if param_three_lang.get(param_list[2]) is not None:
        param_three_lang[param_list[2]] += 1
    else:
        param_three_lang[param_list[2]] = 1

#calculate probability of param = lang decision
def conditional_prob():
    total_param_one = sum(param_one_lang.values())
    total_param_two = sum(param_two_lang.values())
    total_param_three = sum(param_three_lang.values())
    #print(total_param_one)
    for lang in param_one_lang:
        if param_one_lang_is_decision.get(lang) is None:
            cp_param_one[lang] = 0
        else:
            cp_param_one[lang] = param_one_lang_is_decision[lang] / total_param_one
    for lang in param_two_lang:
        if param_two_lang_is_decision.get(lang) is None:
            cp_param_two[lang] = 0
        else:
            cp_param_two[lang] = param_two_lang_is_decision[lang] / total_param_two
    for lang in param_three_lang:
        if param_three_lang_is_decision.get(lang) is None:
            cp_param_three[lang] = 0
        else:
            cp_param_three[lang] = param_three_lang_is_decision[lang] / total_param_three

#calculate the probability of each class regardless of parameters
def overall_probability(total_rows, data):
    class_counts = {}
    for i in range(total_rows):
        list = data[i]
        all_langs.append(list[3])
    for i in all_langs:
        if class_counts.get(i) is None:
            class_counts[i] = 1
        else:
            class_counts[i] += 1
    for i in all_langs:
        overall_prob_langs[i] = class_counts.get(i) / total_rows
    #print(overall_prob_langs)

#calculate posterior probability to make decision
def posterior_probability(param_list):
    #posterior_prob_langs = {}
    #iterate through all possible classes/decisions (all languages from languages.py)
    #calculate probability by multiplying the conditional probability for each parameter given the
        #class/decision by the probability of the class/decision overall
        #whichever posterior probability is the greatest is the decision
        #Ex: P(af | af, en, af) = conditional probability of af param 1 given af decision * 
        #conditional probability of en param 2 given af decision *
        #conditional probability of af param 3 given af decision *
        #overall probability of af
        #repeat for each language
        #continuation = P(sq | af, en, af) = conditional probability of af param 1 given sq decision * 
        #conditional probability of en param 2 given sq decision *
        #conditional probability of af param 3 given sq decision *
        #overall probability of sq
        #...
        #sort to find max
    #for lang in all_langs:
    return

    


#test separating data by class (language decision)
data = [["da", "am","da","da"],
["af","af","sn","af"],
["am","am","am","am"],
["vi","vi","vi","vi"],
["ug","af","ug","ug"],
["af","af","af","af"]]
total_translations = len(data)
overall_probability(total_translations, data)
data_set = separate_by_class(data)
#print(data_set)
for key in data_set:
    for list in data_set[key]:
        find_freq_table(key, list)

for key in data_set:
    for list in data_set[key]:
        find_total_lang_instance(list)


conditional_prob()

print("counts of each language in each parameter")
print("Param 1 total counts")
print(param_one_lang)
print("Param 2 total counts")
print(param_two_lang)
print("Param 3 total counts")
print(param_three_lang)

print("Param 1 number of times param 1 lang = decision lang")
print(param_one_lang_is_decision)
print("Param 2 number of times param 2 lang = decision lang")
print(param_two_lang_is_decision)
print("Param 3 number of times param 3 lang = decision lang")
print(param_three_lang_is_decision)

print("Param 1 conditional probabilities")
print(cp_param_one)
print("Param 2 conditional probabilities")
print(cp_param_two)
print("Param 3 conditional probabilities")
print(cp_param_three)

print("Overall probability for each lang decision")
print(overall_prob_langs)


#TODO:
#calculate posterior probability