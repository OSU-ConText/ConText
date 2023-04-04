import languages
import database

user = "user"
sent_history = "sent_history"
training_data = "training_data"
class_tree_training_data = "class_tree_training_data"

#Will return True if the table exists, False if it does not
def check_table_existence(table_name, creating=False):
    table_check = database.cur.execute(f"SELECT name FROM sqlite_master WHERE name='{table_name}'")
    table_exists = table_check.fetchone() != None

    if (not table_exists and creating == False):
        print(f"The {table_name} table does not exist, please create it first!")

    #if (table_exists and creating == True):
        #print(f"{table_name} table already exists!")

    return table_exists

def get_language_columns():
    str = ' INTEGER DEFAULT 0, '.join(languages.LANGUAGES.keys())
    str += ' INTEGER DEFAULT 0, '

    #character - not allowed in sqlite column names
    str = str.replace('-', '_')
    return str


#Will create the needed tables if they do not already exist
def create_tables():
    if (check_table_existence(user, True) == False):
        #print(f'creating {user} table')
        database.cur.execute(f'''CREATE TABLE {user}
            (user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            all_messages_lang TEXT DEFAULT NULL)''')
        #print(f'{user} table created')

    if (check_table_existence(sent_history, True) == False):
        #print(f'creating {sent_history} table')
        database.cur.execute(f'''CREATE TABLE {sent_history}
            (sent_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER NOT NULL, 
            recipient_history_id INTEGER, 
            conv_messages_lang TEXT DEFAULT NULL, 
            last_message_lang TEXT DEFAULT NULL, 
            is_all_messages INTEGER DEFAULT 0,''' 
            + get_language_columns() + 
            f'''total INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES {user}(user_id),
            FOREIGN KEY(recipient_history_id) REFERENCES {sent_history}(sent_id))''')
        #print(f'{sent_history} table created')

    if (check_table_existence(training_data, True) == False):
        #print(f'creating {training_data} table')
        database.cur.execute(f'''CREATE TABLE {training_data}
            (all_messages_lang TEXT,
            conv_messages_lang TEXT, 
            last_message_lang TEXT,
            label TEXT)''')
        #print(f'{training_data} table created')



def delete_tables():
    if (check_table_existence(user, True) == True):
        database.cur.execute("DROP TABLE user")
    if (check_table_existence(sent_history, True) == True):
        database.cur.execute("DROP TABLE sent_history")
    if (check_table_existence(training_data, True) == True):
        database.cur.execute("DROP TABLE training_data")
    #("Table dropped... ")
    database.con.commit()

def add_training_data(all_lang, conv_lang, last_lang, label):
    if (check_table_existence(training_data) == True):
        #execute insertion of user and commit
        database.cur.execute(f"""
            INSERT INTO {training_data} (all_messages_lang, conv_messages_lang, last_message_lang, label) VALUES
            (?, ?, ?, ? )""", 
        (all_lang, conv_lang, last_lang, label))
        database.con.commit()
    #print('nice')

#gets recipient history id
def get_recipient_history_id(sent_id):
    #verify integer is provided
    sent_id = int(sent_id)
    recipient_history_id = None

    #Get the user ids from the sent_history table
    if (check_table_existence(sent_history) == True):
        recipient_history_id = database.cur.execute(f"SELECT recipient_history_id FROM {sent_history} WHERE sent_id = ?",
        (sent_id,),).fetchall()
        recipient_history_id = recipient_history_id[0][0]

    return recipient_history_id



#will make a decision based on the parameters
def make_lang_decision(all_lang, conv_lang, last_lang):
    #TODO Taking the three parameters, find the most common, or apply tiebreaks to choose a preferred language, and return that language
    #print('conv_lang: ' + str(conv_lang))
    #print('last_lang: ' + str(last_lang))
    #print('all_lang: ' + str(all_lang))

    #TODO stop hard coding this
    parameter_count = 3
    parameter_map = {}
    param_list = [conv_lang, last_lang, all_lang]
    
    for i in range(0, parameter_count):
        if param_list[i] in parameter_map:
            parameter_map[param_list[i]] += 1
        else:
            parameter_map[param_list[i]] = 1
        #print(parameter_map)

    #TODO: this hardcoding is particularly bad but i just want to get this done 
    lang = None

    #tiebreaker needed
    if len(parameter_map) == 3:
        #print("tiebreaker")
        #arbitarily choosing the all_lang parameter for now
        lang = all_lang
    else:
        lang = max(parameter_map, key=parameter_map.get)
    #print(lang)
    return lang

def get_attr_from_sent_history(desiredAttr,sent_id):
    attr = database.cur.execute(f"SELECT {desiredAttr} FROM {sent_history} WHERE sent_id = {sent_id}").fetchall()
    #if empty, the sent_id queried does not exist
    if len(attr) == 0:
        return None
    else:
        return attr[0][0]

def get_attr_from_user(desiredAttr,user_id):
    attr = database.cur.execute(f"SELECT {desiredAttr} FROM {user} WHERE user_id = {user_id}").fetchall()
    #if empty, the user_id queried does not exist
    if len(attr) == 0:
        return None
    else:
        return attr[0][0]

def check_conversation_exists(user_id_1, user_id_2):
    for sid in database.get_sent_ids(user_id_1):
        recipient = get_attr_from_sent_history("recipient_history_id", sid)
        if (user_id_2 == get_attr_from_sent_history("user_id", recipient)):
            return 1
    return 0

def create_class_tree_training_data():
    if (not check_table_existence(class_tree_training_data, True)):
    #print(f'creating {training_data} table')
        database.cur.execute(f'''CREATE TABLE {class_tree_training_data}
            (all_messages_lang_1 TEXT,
            all_messages_percent_1 REAL,
            all_messages_lang_2 TEXT,
            all_messages_percent_2 REAL,
            all_messages_lang_3 TEXT,
            all_messages_percent_3 REAL,
            conv_messages_lang_1 TEXT, 
            conv_messages_percent_1 REAL,
            conv_messages_lang_2 TEXT, 
            conv_messages_percent_2 REAL,
            conv_messages_lang_3 TEXT, 
            conv_messages_percent_3 REAL,
            last_message_lang TEXT,
            last_message_percent REAL,
            label TEXT)''')
    #print(f'{training_data} table created')

def record_class_tree_training_data(sent_id, decision_lang):
    conv_info = database.get_all_lang_info(sent_id)
    all_info = database.get_all_lang_info(int(conv_info.get("user_id")) * -1)
    print(conv_info)
    print(all_info)
    conv_info.pop("user_id")
    all_info.pop("user_id")
    create_class_tree_training_data()
    conv_total = int(conv_info.get("total"))
    all_total = int(all_info.get("total"))
    conv_info.pop("total")
    all_info.pop("total")
    last_message_lang = conv_info["last_message_lang"]
    last_message_percent = 1.0
    conv_info.pop("last_message_lang")
    all_info.pop("last_message_lang")
    label = decision_lang

    all_messages_lang_1 = None
    all_messages_percent_1 = None
    all_messages_lang_2 = None
    all_messages_percent_2 = None
    all_messages_lang_3 = None
    all_messages_percent_3 = None
    
    if len(all_info) > 0:
        all_messages_lang_1 = max(all_info, key=all_info.get)
        print(all_messages_lang_1)
        all_messages_percent_1 = all_info.get(all_messages_lang_1) / all_total
        print(all_messages_percent_1, "/", all_total)
        all_info.pop(all_messages_lang_1)
        
        if len(all_info) > 0:
            all_messages_lang_2 = max(all_info, key=all_info.get)
            print(all_messages_lang_2)
            all_messages_percent_2 = all_info.get(all_messages_lang_2) / all_total
            print(all_messages_percent_2, "/", all_total)
            all_info.pop(all_messages_lang_2)
            
            if len(all_info) > 0:
                all_messages_lang_3 = max(all_info, key=all_info.get)
                all_messages_percent_3 = all_info.get(all_messages_lang_3) / all_total

    conv_messages_lang_1 = None
    conv_messages_percent_1 = None
    conv_messages_lang_2 = None
    conv_messages_percent_2 = None
    conv_messages_lang_3 = None
    conv_messages_percent_3 = None
    
    if len(conv_info) > 0:
        conv_messages_lang_1 = max(conv_info, key=conv_info.get)
        #print(conv_info[conv_messages_lang_1])
        count = conv_info[conv_messages_lang_1] #conv_info.get(conv_messages_lang_1)
        conv_messages_percent_1 = int(count) / int(conv_total)
        conv_info.pop(conv_messages_lang_1)
        if len(conv_info) > 0:
            conv_messages_lang_2 = max(conv_info, key=conv_info.get)
            count = conv_info.get(conv_messages_lang_2)
            conv_messages_percent_2 =  int(count) / int(conv_total)
            conv_info.pop(conv_messages_lang_2)
            if len(conv_info) > 0:
                conv_messages_lang_3 = max(conv_info, key=conv_info.get)
                count = conv_info.get(conv_messages_lang_3)
                conv_messages_percent_3 = int(count) / int(conv_total)


    #execute insertion of user and commit
    database.cur.execute(f"""
        INSERT INTO {class_tree_training_data} (all_messages_lang_1, all_messages_percent_1, 
        all_messages_lang_2, all_messages_percent_2,
        all_messages_lang_3, all_messages_percent_3,
        conv_messages_lang_1, conv_messages_percent_1,
        conv_messages_lang_2, conv_messages_percent_2,
        conv_messages_lang_3, conv_messages_percent_3,
        last_message_lang, last_message_percent, label) VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?)""", 
    (all_messages_lang_1, all_messages_percent_1, 
     all_messages_lang_2, all_messages_percent_2,
     all_messages_lang_3, all_messages_percent_3,
     conv_messages_lang_1, conv_messages_percent_1,
     conv_messages_lang_2, conv_messages_percent_2,
     conv_messages_lang_3, conv_messages_percent_3,
     last_message_lang, last_message_percent, label))
    
    database.con.commit()


def create_class_data():
    if (check_table_existence("class_data", True) == False):
    #print(f'creating {sent_history} table')
        database.cur.execute(f'''CREATE TABLE {"class_data"}
        (label TEXT, ''' 
        + get_language_columns_for_test_data_creation())

def get_language_columns_for_test_data_creation():
    str = ' REAL DEFAULT 0, '.join(languages.LANGUAGES.keys())
    str += ' REAL DEFAULT 0)'

    #character - not allowed in sqlite column names
    str = str.replace('-', '_')
    return str

def get_language_columns_for_test_data_insertion():
    str = ', '.join(languages.LANGUAGES.keys())

    #character - not allowed in sqlite column names
    str = str.replace('-', '_')
    return str

def record_class_data(sent_id, decision_lang):

    conv_info = database.get_all_lang_info(sent_id)
    all_info = database.get_all_lang_info(int(conv_info.get("user_id")) * -1)
    # print(conv_info)
    # print(all_info)
    conv_info.pop("user_id")
    all_info.pop("user_id")
    create_class_data()
    conv_total = int(conv_info.get("total"))
    all_total = int(all_info.get("total"))
    conv_info.pop("total")
    all_info.pop("total")
    last_message_lang = conv_info["last_message_lang"]
    last_message_percent = .25
    conv_info.pop("last_message_lang")
    all_info.pop("last_message_lang")
    label = decision_lang
    mLanguages = {}

    for language in languages.LANGUAGES:
        language = language.replace('-', '_')
        added = False
        if language in conv_info:
            mLanguages[language] = conv_info[language] / conv_total
            added = True
        if language in all_info:
            if added:
                mLanguages[language] += all_info[language] / all_total
            else:
                mLanguages[language] = all_info[language] / all_total
        if not added:
            mLanguages[language] = 0

    mLanguages[last_message_lang] += last_message_percent
    #print(mLanguages.values())

    languagesString = "INSERT INTO class_data (label, "+get_language_columns_for_test_data_insertion()+") VALUES (""" 
    languagesString += "\'"+ label +"\', "
    #languagesString2 = ''.join(str(list(mLanguages.values())))
    languagesString += ', '.join([str(item) for item in mLanguages.values()])
    languagesString += ')'
    print(languagesString)
    database.cur.execute(languagesString)


    # database.cur.execute(f"""
    #     INSERT INTO {"class_data"} (label, ) VALUES
    #     (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?)""", 
    #     (all_messages_lang_1, all_messages_percent_1, 
    #     all_messages_lang_2, all_messages_percent_2,
    #     all_messages_lang_3, all_messages_percent_3,
    #     conv_messages_lang_1, conv_messages_percent_1,
    #     conv_messages_lang_2, conv_messages_percent_2,
    #     conv_messages_lang_3, conv_messages_percent_3,
    #     last_message_lang, last_message_percent, label))



    

    



