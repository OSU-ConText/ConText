import sqlite3
import languages
import database_helper


#variables to store name of the tables we are using
user = "user"
sent_history = "sent_history"
training_data = "training_data"

#connect to the database
con = sqlite3.connect("context.db")
#enable foreign keys
con.execute("PRAGMA foreign_keys = ON")
cur = con.cursor()

#Will create a user, inserting a row in both tables to keep track of their parameters and their overall messages counts
def create_user():
    if (database_helper.check_table_existence(user) == True):

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
    if (database_helper.check_table_existence(sent_history) == True):
        #execute insertion of user and commit
        cur.execute(f"""
            INSERT INTO {sent_history} (sent_id, user_id, recipient_history_id, is_all_messages) VALUES
            (?, ?, ?, 1 )""", 
        (sent_id, user_id, sent_id))
        con.commit()

    #print(f"added user", (user_id))
    return user_id

def create_sent_history(user_id_1, user_id_2):
    #verify integers are provided
    user_id_1 = int(user_id_1)
    user_id_2 = int(user_id_2)

    if (database_helper.check_table_existence(sent_history) == True 
        and not database_helper.check_conversation_exists(user_id_1, user_id_2)):

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

        #print('send history for user with id ' + str(user_id_1) + ' is in row with send_id ' + str(recipient_id1))  
        #print('send history for user with id ' + str(user_id_2) + ' is in row with send_id ' + str(recipient_id2))  
        ids = [recipient_id1, recipient_id2]
        #print(ids[0], ids[1])
        return ids
    else:
        print("conversation already exists")
        return None


#this is done with the recipient's id so that on the front-end only one send_id has to be used
#get the language your recipient needs
def get_recipient_lang(sent_id):
    #verify integer is provided
    sent_id = int(sent_id)
    recipient_id = None

    #First we will check the sent_history table to get the recipients conv_messages_lang and last_message_lang, and also to get the recipients user_id 
    if (database_helper.check_table_existence(sent_history) == True):
        #print('table exists')

        #Get the recipient_history_id
        recipient_history_id = database_helper.get_recipient_history_id(sent_id)
        #print(recipient_history_id)

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

    if (database_helper.check_table_existence(user) == True):
        #print('table exists')

        #Get the most commonly used language of all messages sent by the recipient of this message
        all_lang = cur.execute(f"SELECT all_messages_lang FROM {user} WHERE user_id = ?",
        (recipient_id,),).fetchall()
        all_lang = all_lang[0][0]

    #Taking the three parameters, find the most common, or apply tiebreaks to choose a preferred language, and return that language
    decision_lang = database_helper.make_lang_decision(all_lang, conv_lang, last_lang)

    if (decision_lang == None):
        decision_lang = cur.execute(f"SELECT last_message_lang FROM {sent_history} WHERE sent_id = {sent_id}").fetchall()[0][0]
  
    if(all_lang is not None and last_lang is not None and conv_lang is not None):
        database_helper.add_training_data(all_lang, conv_lang, last_lang, decision_lang)
    return decision_lang

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
    
    #increment counts for totals
    cur.execute(f"""
            UPDATE {sent_history} SET total = total + 1
            WHERE sent_id = {sent_id}
        """)
    cur.execute(f"""
            UPDATE {sent_history} SET total = total + 1
            WHERE sent_id = {all_convos_id}
        """)

    #set most recent language sent
    cur.execute(f"""
            UPDATE {sent_history} SET last_message_lang = \'{lang}\'
            WHERE sent_id = {sent_id}
        """)
    
    #commit all above changes
    con.commit()

    
    #find max for this conversation
    row = cur.execute(f"""SELECT *
        FROM {sent_history} 
        WHERE sent_id = {sent_id}""").fetchone()
    #slice 6 columns at beginning of row to only get languages, don't include total
    row_list = list(row)[6:111]
    max_count = max(row_list)
    lang_index = row_list.index(max_count)

    conv_lang = "\'" + list(languages.LANGUAGES.keys())[lang_index] + "\'"

    cur.execute(f"""
            UPDATE {sent_history} SET conv_messages_lang = {conv_lang}
            WHERE sent_id = {sent_id}
        """)
    
    #find max for all conversations
    row = cur.execute(f"""SELECT *
        FROM {sent_history} 
        WHERE sent_id = {all_convos_id}""").fetchone()
    
    row_list = list(row)[6:111]
    max_count = max(row_list)
    lang_index = row_list.index(max_count)

    conv_lang = "\'" + list(languages.LANGUAGES.keys())[lang_index] + "\'"

    cur.execute(f"""
            UPDATE {user} SET all_messages_lang = {conv_lang}
            WHERE user_id = {user_id}
        """)
    con.commit()



def get_sent_ids(user_id):
    sent_ids = cur.execute(f"SELECT sent_id FROM {sent_history} WHERE user_id = {user_id}").fetchall()
    l = list(sent_ids)
    result = []
    for item in l:
        result.append(item[0])
    return result

#get the 2 users in a conversation
def get_users_sent_history(sent_id):
    users = []
    users.append(cur.execute(f"SELECT user_id FROM {sent_history} WHERE sent_id = {sent_id}").fetchall()[0][0])
    user2_sent_id = cur.execute(f"SELECT recipient_history_id FROM {sent_history} WHERE sent_id = {sent_id}").fetchall()[0][0]
    users.append(cur.execute(f"SELECT user_id FROM {sent_history} WHERE sent_id = {user2_sent_id}").fetchall()[0][0])
    return users

def get_all_sent_history_info(sent_id):
    result = {}
    result.update({"sent_id": str(sent_id)})
    user_id = database_helper.get_attr_from_sent_history("user_id",sent_id)
    result.update({"user_id": str(user_id)})
    result.update({"recipient_history_id": str(database_helper.get_attr_from_sent_history("recipient_history_id",sent_id))})
    result.update({"all_messages_lang": database_helper.get_attr_from_user("all_messages_lang",user_id)})
    result.update({"conv_messages_lang": database_helper.get_attr_from_sent_history("conv_messages_lang",sent_id)})
    result.update({"last_message_lang": database_helper.get_attr_from_sent_history("last_message_lang",sent_id)})
    result.update({"is_all_messages": str(bool(database_helper.get_attr_from_sent_history("is_all_messages",sent_id)))})
    result.update({"total": str(database_helper.get_attr_from_sent_history("total",str(sent_id)))})
    row = cur.execute(f"SELECT * FROM {sent_history} WHERE sent_id = {sent_id}").fetchone()
    language_counts = list(row)[6:111]
    language_names = list(languages.LANGUAGES.keys())
    for x in range(len(language_counts)):
        if language_counts[x] != 0:
            result.update({language_names[x]: str(language_counts[x])})

    return result


