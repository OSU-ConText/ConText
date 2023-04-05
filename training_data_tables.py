import database
import database_helper
import languages

table_with_3_percents = "table_with_3_percents"
table_with_all_langs = "table_with_all_langs"
table_with_all_langs_and_id = "table_with_all_langs_and_id"

def create_table_with_3_percents():
    if (not database_helper.check_table_existence(table_with_3_percents, True)):
        database.cur.execute(f'''CREATE TABLE {table_with_3_percents}
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

def record_training_data_3_percents(sent_id, decision_lang):
    conv_info = database.get_all_lang_info(sent_id)
    all_info = database.get_all_lang_info(int(conv_info.get("user_id")) * -1)
    print(conv_info)
    print(all_info)
    conv_info.pop("user_id")
    all_info.pop("user_id")
    create_table_with_3_percents()
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
        INSERT INTO {table_with_3_percents} (all_messages_lang_1, all_messages_percent_1, 
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


def create_table_with_all_langs():
    if (database_helper.check_table_existence(table_with_all_langs, True) == False):
    #print(f'creating {sent_history} table')
        database.cur.execute(f'''CREATE TABLE {table_with_all_langs}
        (label TEXT, ''' 
        + get_language_columns_for_test_data_creation())

def get_language_columns_for_test_data_creation():
    str = ' REAL DEFAULT 1, '.join(languages.LANGUAGES.keys())
    str += ' REAL DEFAULT 1)'

    #character - not allowed in sqlite column names
    str = str.replace('-', '_')
    return str

def get_language_columns_for_test_data_insertion():
    str = ', '.join(languages.LANGUAGES.keys())

    #character - not allowed in sqlite column names
    str = str.replace('-', '_')
    return str

def record_training_data_percents(sent_id, decision_lang):
    conv_info = database.get_all_lang_info(sent_id)
    all_info = database.get_all_lang_info(int(conv_info.get("user_id")) * -1)
    conv_info.pop("user_id")
    all_info.pop("user_id")
    create_table_with_all_langs()
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

    if(len(conv_info) > 0):
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
                mLanguages[language] = 1

        mLanguages[last_message_lang] += last_message_percent

        languagesString = f"INSERT INTO {table_with_all_langs} (label, "+get_language_columns_for_test_data_insertion()+") VALUES (""" 
        languagesString += "\'"+ label +"\', "
        languagesString += ', '.join([str(item) for item in mLanguages.values()])
        languagesString += ')'
        #print(languagesString)
        database.cur.execute(languagesString)

def create_table_with_all_langs_and_id():
    if (database_helper.check_table_existence(table_with_all_langs_and_id, True) == False):
    #print(f'creating {sent_history} table')
        database.cur.execute(f'''CREATE TABLE {table_with_all_langs_and_id}
        (row_id INTEGER PRIMARY KEY AUTOINCREMENT, label TEXT, ''' 
        + get_language_columns_for_test_data_creation())

def record_training_data_all_langs(sent_id, decision_lang):
    params = database.get_params(sent_id)
    if None not in list(params.values()):
        create_table_with_all_langs_and_id()
        insertion = f"""INSERT INTO {table_with_all_langs_and_id} (label) VALUES (\'{decision_lang}\')"""
        insertion = insertion.replace('-', '_')

        database.cur.execute(insertion)
        id = database.cur.lastrowid#database.cur.execute("SELECT SCOPE_IDENTITY()").fetchone()
        update = f"""UPDATE {table_with_all_langs_and_id} SET {params["all_messages_lang"]} = {params["all_messages_lang"]} + 1 WHERE row_id = {id}"""
        update = update.replace('-', '_')
        database.cur.execute(update)
        update2 = f"""UPDATE {table_with_all_langs_and_id} SET {params["conv_messages_lang"]} = {params["conv_messages_lang"]} + 1 WHERE row_id = {id}"""
        update2 = update.replace('-', '_')
        database.cur.execute(update2)
        update3 = f"""UPDATE {table_with_all_langs_and_id} SET {params["last_message_lang"]} = {params["last_message_lang"]} + 1 WHERE row_id = {id}"""
        update3 = update2.replace('-', '_')
        database.cur.execute(update3)
        print(insertion)
        print(update)
        print(update2)
        print(update3)




    

    



