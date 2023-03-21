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
        cur.execute(f"CREATE TABLE {sent_history}(sent_id, user_id, recipient_history_id, conv_messages_lang, last_message_lang, is_all_messages, en, fr, total)")
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
        sent_id = user_id * -1

        #create row in sent_history table to store all user sending history
        if (check_table_existence(sent_history) == True):
            #execute insertion of user and commit
            cur.execute(f"""
                INSERT INTO {sent_history} VALUES
                (?, ?, NULL, NULL, NULL, 1, 0, 0, 0)
            """, 
            (sent_id, user_id))
            con.commit()

        return user_id

def create_sent_history(user_id_1, user_id_2):
    #verify integers are provided
    user_id_1 = int(user_id_1)
    user_id_2 = int(user_id_2)

    if (check_table_existence(sent_history) == True):
        #TODO: automatically generate sent_id, make the other_sent_id that plus 1
        sent_id = 1
        other_sent_id = sent_id + 1

        #insert first row, user_id_1 history being recorded
        cur.execute(f"""
            INSERT INTO {sent_history} VALUES
            (?, ?, ?, NULL, NULL, 0, 0, 0, 0)
        """, 
        (sent_id, user_id_1, other_sent_id))
        con.commit()

        #insert second row, user_id_2 history being recorded
        cur.execute(f"""
            INSERT INTO {sent_history} VALUES
            (?, ?, ?, NULL, NULL, 0, 0, 0, 0)
        """, 
        (other_sent_id, user_id_2, sent_id))
        con.commit()

#will return recipient_history_id
def get_recipient_history_id(sent_id):
    #verify integer is provided
    sent_id = int(sent_id)
    recipient_history_id = None

    #Get the user ids from the sent_history table
    if (check_table_existence(sent_history) == True):
        recipient_history_id = cur.execute(f"SELECT recipient_history_id FROM {sent_history} WHERE sent_id = ?",
        (sent_id,),).fetchall()
        recipient_history_id = recipient_history_id[0][0]

    return recipient_history_id

#will make a decision based on the parameters
def make_lang_decision(all_lang, conv_lang, last_lang):
    #TODO Taking the three parameters, find the most common, or apply tiebreaks to choose a preferred language, and return that language
    print('conv_lang: ' + str(conv_lang))
    print('last_lang: ' + str(last_lang))
    print('all_lang: ' + str(all_lang))

def get_preferred_lang(sent_id):
    #verify integer is provided
    sent_id = int(sent_id)
    recipient_id = None

    #First we will check the sent_history table to get the recipients conv_messages_lang and last_message_lang, and also to get the recipients user_id 
    if (check_table_existence(sent_history) == True):
        print('table exists')

        #Get the recipient_history_id
        recipient_history_id = get_recipient_history_id(sent_id)
        print(recipient_history_id)

        #Get the most commonly used language by the recipient in this conversation
        conv_lang = cur.execute(f"SELECT conv_messages_lang FROM {sent_history} WHERE sent_id = ?",
        (recipient_history_id,),).fetchall()
        conv_lang = conv_lang[0][0]

        #Get the language of the most recently sent message in the conversation
        last_lang = cur.execute(f"SELECT last_message_lang FROM {sent_history} WHERE sent_id = ?",
        (recipient_history_id,),).fetchall()
        last_lang = last_lang[0][0]

        #Get the recipient's user_id
        recipient_id = cur.execute(f"SELECT user_id FROM {sent_history} WHERE sent_id = ?",
        (recipient_history_id,),).fetchall()
        recipient_id = recipient_id[0][0]

    if (check_table_existence(user) == True):
        print('table exists')

        #Get the most commonly used language of all messages sent by the recipient of this message
        all_lang = cur.execute(f"SELECT all_messages_lang FROM {user} WHERE user_id = ?",
        (recipient_id,),).fetchall()
        all_lang = all_lang[0][0]

    #TODO Taking the three parameters, find the most common, or apply tiebreaks to choose a preferred language, and return that language
    make_lang_decision(all_lang, conv_lang, last_lang)


def get_attr_from_sent_history(desiredAttr,sent_id):
    attr = cur.execute(f"SELECT {desiredAttr} FROM {sent_history} WHERE sent_id = {sent_id}").fetchall()
    return attr[0][0]

def test_get_attr_from_sent_history():
    uid = create_user()
    if get_attr_from_sent_history("user_id",-1 * uid) == uid :
        print("success")
    else:
        print("fail")

#def increment_count(lang, sent_id):
    #get user id of conversation
    #increment lang in conversation
    #increment lang in -user_id (all messages) for ALL conversations!