import sqlite3
import languages

#variables to store name of the tables we are using
user = "user"
sent_history = "sent_history"

#connect to the database
con = sqlite3.connect("context.db")
#enable foreign keys
con.execute("PRAGMA foreign_keys = ON")
cur = con.cursor()


#Will return True if the table exists, False if it does not
def check_table_existence(table_name, creating=False):
    table_check = cur.execute(f"SELECT name FROM sqlite_master WHERE name='{table_name}'")
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
        cur.execute(f'''CREATE TABLE {user}
            (user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            all_messages_lang TEXT DEFAULT NULL)''')
        print(f'{user} table created')

    if (check_table_existence(sent_history, True) == False):
        print(f'creating {sent_history} table')
        cur.execute(f'''CREATE TABLE {sent_history}
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

def delete_tables():
    if (check_table_existence(user, True) == True):
        cur.execute("DROP TABLE user")
    if (check_table_existence(sent_history, True) == True):
        cur.execute("DROP TABLE sent_history")
    print("Table dropped... ")
    con.commit()

#Will create a user, inserting a row in both tables to keep track of their parameters and their overall messages counts
def create_user():
    if (check_table_existence(user) == True):

        #execute insertion of user and commit
        cur.execute(f"""
            INSERT INTO {user} (user_id) VALUES 
            (NULL)
        """,)
        con.commit()

    #create row in message counts to store all messages history

    user_id = cur.lastrowid

    #as per schema, conversation id for all message history is user_id * -1
    sent_id = user_id * -1

    #create row in sent_history table to store all user sending history
    if (check_table_existence(sent_history) == True):
        #execute insertion of user and commit
        cur.execute(f"""
            INSERT INTO {sent_history} (sent_id, user_id, recipient_history_id, is_all_messages) VALUES
            (?, ?, ?, 1 )""", 
        (sent_id, user_id, sent_id))
        con.commit()

    print(f"added user", (user_id))
    return user_id

def create_sent_history(user_id_1, user_id_2):
    #verify integers are provided
    user_id_1 = int(user_id_1)
    user_id_2 = int(user_id_2)

    if (check_table_existence(sent_history) == True):

        #insert first row, user_id_1 history being recorded
        cur.execute(f"""
            INSERT INTO {sent_history} (user_id) VALUES
            ({user_id_1})
        """)
        con.commit()

        recipient_id1 = cur.lastrowid

        #insert second row, user_id_2 history being recorded
        cur.execute(f"""
            INSERT INTO {sent_history} (user_id, recipient_history_id) VALUES
            ({user_id_2}, {recipient_id1})
        """)
        con.commit()

        recipient_id2 = cur.lastrowid

        cur.execute(f"""
                UPDATE {sent_history} SET recipient_history_id = {recipient_id2}
                WHERE sent_id = {recipient_id1}
            """) 
        con.commit()       

#will return list of user ids associated with a sent id, first entry is user_id, second entry is recipient_history_id
def get_users_sent_history(sent_id):
    #verify integer is provided
    sent_id = int(sent_id)
    user_id = None
    recipient_history_id = None

    #Get the user ids from the sent_history table
    if (check_table_existence(sent_history) == True):
        user_id = cur.execute(f"SELECT user_id FROM {sent_history} WHERE sent_id = ?",
        (sent_id,),).fetchall()
        user_id = user_id[0][0]

        recipient_history_id = cur.execute(f"SELECT recipient_history_id FROM {sent_history} WHERE sent_id = ?",
        (sent_id,),).fetchall()
        recipient_history_id = recipient_history_id[0][0]

    return [user_id, recipient_history_id]

def get_preferred_lang(sent_id):
    #verify integer is provided
    sent_id = int(sent_id)

    #First we will check the sent_history table to get the recipients conv_messages_lang and last_message_lang, and also to get the recipients user_id 
    if (check_table_existence(sent_history) == True):
        print('table exists')

        #TODO: Get the most commonly used language by the recipient in this conversation

        #TODO: Get the language of the most recently sent message in the conversation

    if (check_table_existence(user) == True):
        print('table exists')

        #TODO Get the most commonly used language of all messages sent by the recipient of this message

    #TODO Taking the three parameters, find the most common, or apply tiebreaks to choose a preferred language, and return that language


def get_attr_from_sent_history(desiredAttr,sent_id):
    attr = cur.execute(f"SELECT {desiredAttr} FROM {sent_history} WHERE sent_id = {sent_id}").fetchall()
    return attr[0][0]

def test_get_attr_from_sent_history():
    uid = create_user()
    if get_attr_from_sent_history("user_id",-1 * uid) == uid :
        print("success")
    else:
        print("fail")

def update_history(sent_id, lang):
    #increment counts for desired language
    cur.execute(f"""
            UPDATE {sent_history} SET {lang} = {lang} + 1
            WHERE sent_id = {sent_id}
        """)
    user_id = cur.execute(f"SELECT user_id FROM {sent_history} WHERE sent_id = {sent_id}").fetchall()[0][0]
    all_convos_id = -1 * user_id
    cur.execute(f"""
            UPDATE {sent_history} SET {lang} = {lang} + 1
            WHERE sent_id = {all_convos_id}
        """)
    con.commit()
    
    #find max for this conversation
    row = cur.execute(f"""SELECT *
        FROM {sent_history} 
        WHERE sent_id = {sent_id}""").fetchone()
    #slice 6 columns at beginning of row to only get languages
    row_list = list(row)[6:]
    print(row_list)
    max_count = max(row_list)
    lang_index = row_list.index(max_count)
    print(lang_index)

    conv_lang = "\'" + list(languages.LANGUAGES.keys())[lang_index] + "\'"
    print(f"conv lang= {conv_lang}")
    print(f"""
            UPDATE {sent_history} SET conv_messages_lang = {conv_lang}
            WHERE sent_id = {sent_id}
        """)

    cur.execute(f"""
            UPDATE {sent_history} SET conv_messages_lang = {conv_lang}
            WHERE sent_id = {sent_id}
        """)
    
    #find max for all conversations
    row = cur.execute(f"""SELECT *
        FROM {sent_history} 
        WHERE sent_id = {all_convos_id}""").fetchone()
    row_list = list(row)[6:]
    print(row_list)
    max_count = max(row_list)
    lang_index = row_list.index(max_count)
    print(lang_index)

    conv_lang = "\'" + list(languages.LANGUAGES.keys())[lang_index] + "\'"

    cur.execute(f"""
            UPDATE {user} SET all_messages_lang = {conv_lang}
            WHERE user_id = {user_id}
        """)
    con.commit()


def get_sent_ids(user_id):
    sent_ids = cur.execute(f"SELECT sent_id FROM {sent_history} WHERE user_id = {user_id}").fetchall()
    return sent_ids[0]

