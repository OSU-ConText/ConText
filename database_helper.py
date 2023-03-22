import languages
import database

user = "user"
sent_history = "sent_history"
training_data = "training_data"

#Will return True if the table exists, False if it does not
def check_table_existence(table_name, creating=False):
    table_check = database.cur.execute(f"SELECT name FROM sqlite_master WHERE name='{table_name}'")
    table_exists = table_check.fetchone() != None

    if (not table_exists and creating == False):
        print(f"The {table_name} table does not exist, please create it first!")

    if (table_exists and creating == True):
        print(f"{table_name} table already exists!")

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
        print(f'creating {user} table')
        database.cur.execute(f'''CREATE TABLE {user}
            (user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            all_messages_lang TEXT DEFAULT NULL)''')
        print(f'{user} table created')

    if (check_table_existence(sent_history, True) == False):
        print(f'creating {sent_history} table')
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
        print(f'{sent_history} table created')

    if (check_table_existence(training_data, True) == False):
        print(f'creating {training_data} table')
        database.cur.execute(f'''CREATE TABLE {training_data}
            (all_messages_lang TEXT,
            conv_messages_lang TEXT, 
            last_message_lang TEXT,
            label TEXT)''')
        print(f'{training_data} table created')



def delete_tables():
    if (check_table_existence(user, True) == True):
        database.cur.execute("DROP TABLE user")
    if (check_table_existence(sent_history, True) == True):
        database.cur.execute("DROP TABLE sent_history")
    if (check_table_existence(training_data, True) == True):
        database.cur.execute("DROP TABLE training_data")
    print("Table dropped... ")
    database.con.commit()

def add_training_data(all_lang, conv_lang, last_lang, label):
    if (check_table_existence(training_data) == True):
        #execute insertion of user and commit
        database.cur.execute(f"""
            INSERT INTO {training_data} (all_messages_lang, conv_messages_lang, last_message_lang, label) VALUES
            (?, ?, ?, ? )""", 
        (all_lang, conv_lang, last_lang, label))
        database.con.commit()
    print('nice')
