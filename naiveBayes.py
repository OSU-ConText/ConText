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
    print(total_param_one)
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

#test separating data by class (language decision)
data = [["da", "am","da","da"],
["af","af","sn","af"],
["am","am","am","am"],
["vi","vi","vi","vi"],
["ug","af","ug","ug"],
["af","af","af","af"]]
data_set = separate_by_class(data)
#print(data_set)
for key in data_set:
    for list in data_set[key]:
        find_freq_table(key, list)

for key in data_set:
    for list in data_set[key]:
        find_total_lang_instance(list)

conditional_prob()

#print(param_one_lang)
#print(param_two_lang)
#print(param_three_lang)

#print(param_one_lang_is_decision)
#print(param_two_lang_is_decision)
#print(param_three_lang_is_decision)

print(cp_param_one)
print(cp_param_two)
print(cp_param_three)