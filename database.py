import sqlite3

#variables to store name of the tables we are using
user_context_parameter = "user_context_parameter"
message_counts = "message_counts"

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

#Will create the needed tables if they do not already exist
def create_tables():
    if (check_table_existence(user_context_parameter, True) == False):
        print(f'creating {user_context_parameter} table')
        cur.execute(f"CREATE TABLE {user_context_parameter}(user_id, all_messages_lang, conv_messages_lang, last_message_lang)")
        print(f'{user_context_parameter} table created')

    if (check_table_existence(message_counts, True) == False):
        print(f'creating {message_counts} table')
        #TODO: Add all of the languages as columns
        cur.execute(f"CREATE TABLE {message_counts}(conv_id, user_id, is_all_messages, en, fr)")
        print(f'{message_counts} table created')

#Will create a user, inserting a row in both tables to keep track of their parameters and their overall messages counts
def create_user():
    if (check_table_existence(user_context_parameter) == True):
        #automate this step at some point
        user_id = int(input('What numeric user id would you like to assign? '))

        #execute insertion of user and commit
        cur.execute(f"""
            INSERT INTO {user_context_parameter} VALUES
            (?, 0, 0, 0)
        """, 
        (user_id,))
        con.commit()

    #create row in message counts to store all messages history

    #as per schema, conversation id for all message history is user_id * -1
    conv_id = user_id * -1

    if (check_table_existence(message_counts) == True):
        #execute insertion of user and commit
        cur.execute(f"""
            INSERT INTO {message_counts} VALUES
            (?, ?, 0, 0, 0)
        """, 
        (conv_id, user_id))
        con.commit()

#def create_conversation():

#def increment_count(lang):