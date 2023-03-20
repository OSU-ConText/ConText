import sqlite3
import languages

#variables to store name of the tables we are using
user = "user"
sent_history = "sent_history"

#connect to the database
con = sqlite3.connect("context.db")
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
    str = ', '.join(languages.LANGUAGES.keys())
    return str


#Will create the needed tables if they do not already exist
def create_tables():
    if (check_table_existence(user, True) == False):
        print(f'creating {user} table')
        cur.execute(f"CREATE TABLE {user}(user_id, all_messages_lang)")
        print(f'{user} table created')

    if (check_table_existence(sent_history, True) == False):
        print(f'creating {sent_history} table')
        cur.execute(f"CREATE TABLE {sent_history}(conv_id, user_id, recipient_history_id, conv_messages_lang, last_message_lang, is_all_messages, en, fr, total)")
        print(f'{sent_history} table created')

#Will create a user, inserting a row in both tables to keep track of their parameters and their overall messages counts
def create_user():
    #create row in user table to store the user
    if (check_table_existence(user) == True):
        #TODO: automate this step at some point
        user_id = int(input('What numeric user id would you like to assign? '))

        #execute insertion of user and commit
        cur.execute(f"""
            INSERT INTO {user} VALUES
            (?, NULL)
        """, 
        (user_id,))
        con.commit()

    #create row in message counts to store all messages history

    #as per schema, conversation id for all message history is user_id * -1
    conv_id = user_id * -1

    #create row in sent_history table to store all user sending history
    if (check_table_existence(sent_history) == True):
        #execute insertion of user and commit
        cur.execute(f"""
            INSERT INTO {sent_history} VALUES
            (?, ?, NULL, NULL, NULL, 1, 0, 0, 0)
        """, 
        (conv_id, user_id))
        con.commit()

    return user_id

#def create_conversation():

def get_attr_from_sent_history(desiredAttr,conv_id):
    attr = cur.execute(f"SELECT {desiredAttr} FROM {sent_history} WHERE conv_id = {conv_id}").fetchall()
    return attr[0][0]

def test_get_attr_from_sent_history():
    uid = create_user()
    if get_attr_from_sent_history("user_id",-1 * uid) == uid :
        print("success")
    else:
        print("fail")

#def increment_count(lang, conv_id):
    #get user id of conversation
    #increment lang in conversation
    #increment lang in -user_id (all messages) for ALL conversations!