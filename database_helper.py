import languages
import database
import sqlite3



user = "user"
sent_history = "sent_history"
training_data = "training_data"

#connect to the database
con = sqlite3.connect("context.db", check_same_thread=False)
#enable foreign keys
con.execute("PRAGMA foreign_keys = ON")
cur = con.cursor()


#Will return True if the table exists, False if it does not
def check_table_existence(table_name, creating=False):
    with database.con:
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
    with database.con:
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

        if (check_table_existence('usernames', True) == False):
            database.cur.execute('''CREATE TABLE usernames
                (user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT DEFAULT NULL)''')
            
        if (check_table_existence('conversations', True) == False):
            database.cur.execute('''CREATE TABLE conversations
                (sent_id INTEGER, 
                sender_id INTEGER,
                sender_name TEXT,
                receiver_id INTEGER,
                receiver_name TEXT)''')



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
    #Taking the three parameters, find the most common, or apply tiebreaks to choose a preferred language, and return that language


    #due to being just three parameters, this is hard coded.  if you add more parameters, you'll need to come up with a better solution
    parameter_count = 3
    parameter_map = {}
    param_list = [conv_lang, last_lang, all_lang]
    
    for i in range(0, parameter_count):
        if param_list[i] in parameter_map:
            parameter_map[param_list[i]] += 1
        else:
            parameter_map[param_list[i]] = 1
        #print(parameter_map)
        
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
