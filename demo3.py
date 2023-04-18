import time
import streamlit as st
import pandas as pd
import database as db
from googletrans import Translator
import sqlite3 
import database_helper as dbh
import messageCreation as mc
import languages
import re

def query_usernames():
    with db.con:
        return db.cur.execute("SELECT user_id, name from usernames").fetchall()

def query_sent_history():
    with db.con:
        return db.cur.execute("SELECT * from sent_history").fetchall()
    
def query_conversations():
    with db.con:
        return db.cur.execute("SELECT * from conversations").fetchall()
    
def get_sent_id(sender,receiver):
    with db.con:
        return db.cur.execute(f"SELECT sent_id from conversations WHERE sender_name LIKE \'{sender}\' and receiver_name LIKE \'{receiver}\'").fetchone()

def get_user_convos(user_id):
    #st.markdown(f'{user_id}')
    with db.con:
        return db.cur.execute(f"SELECT sent_id, receiver_name from conversations WHERE sender_id LIKE \'{user_id}\'").fetchall()
 
def insert_user(name, id):
    with db.con:
        db.cur.execute(f'''INSERT INTO usernames (user_id, name) 
            VALUES ({id}, \'{name}\') ''')

def insert_conversation(sent_id, sender_id, sender_name, receiver_id, receiver_name):
    with db.con:
        db.cur.execute(f'''INSERT INTO conversations 
            (sent_id, sender_id, sender_name, receiver_id, receiver_name)
            
            VALUES ({sent_id}, {sender_id},\'{sender_name}\',{receiver_id},\'{receiver_name}\')''')

def submit_text():
    st.session_state.send_message_list.append('text_sent')

def correct_translation():
    st.session_state.send_message_list.append('correct_translation')

def incorrect_translation():
    st.session_state.send_message_list.append('incorrect_translation')


def submit_correct_lang(lang):
    st.session_state.send_message_list.append('correct_lang_submitted')
    st.session_state.correct_lang = lang
    with db.con:
        db.cur.execute(f'''UPDATE table_with_all_langs_and_id 
            SET label = \'{lang}\'
            WHERE row_id = (SELECT MAX(row_id) FROM table_with_all_langs_and_id)''')
        
def clear_session_state():
    for key in st.session_state.keys():
        if key != "db_created":
            del st.session_state[key]
    
if "db_created" not in st.session_state:
    st.session_state.db_created = False
while (not st.session_state.db_created):
    with st.spinner('Creating database...'):
        dbh.create_tables()
        time.sleep(2)
        st.session_state.db_created = dbh.check_table_existence("usernames", True)

     

options = ['Create User', 'Create Conversation', 'Send Message', 'View User']
selected = st.sidebar.radio('Choose Functionality:', options, on_change=clear_session_state)

q = query_usernames()
users = dict([(value, key) for key, value in q])

q = query_conversations()    
convos = [f"Sender = {item[2]}, Receiver = {item[4]}" for item in q]

if selected == 'Create User':
    st.markdown(f'### Create a User') 
    st.text_input("Name", key='name')
    clicked = st.button('Create')
    if clicked:
        user_id = db.create_user()
        insert_user(st.session_state.name, user_id)
        st.success("Created user")
    q = query_usernames()
    users = dict([(value, key) for key, value in q])
    st.markdown('All Users:')
    for user in users:
        st.markdown(f'- {user}') 

if selected == 'Create Conversation':
    st.markdown(f'### Create a Conversation') 
    if len(users) >= 2:
        col1, col2 = st.columns(2)

        with col1:
            user1 = st.selectbox("User 1:",users.keys(),index=0)

        with col2:
            user2 = st.selectbox( "User 2:",users.keys(),index=1)
        
        clicked = st.button('OK', key='ok1')

        if clicked:
            if user1 == user2:
                st.error("Must choose two different users")
            else:
                ids = db.create_sent_history(users[user1], users[user2])
                if ids == None:
                    st.success("Users already in conversation")
                else:
                    insert_conversation(ids[0],users[user1],user1,users[user2],user2)
                    insert_conversation(ids[1],users[user2],user2,users[user1],user1)
                    st.success("Added users to conversations")
        
        st.markdown('All Convos:')
        q = query_conversations()   
        c = []
        receiver, sender = "", ""
        for item in q:
            if not (receiver == item[2] and sender == item[4]):
                sender = item[2]
                receiver = item[4]
                c.append(f"{sender} & {receiver}")
        for item in c:
            st.markdown(f'- {item}') 

    else:
        st.error('Must create at least two different users')
    

if selected == 'Send Message':
    st.markdown(f'### Send a Message')  
    if "send_message_list" not in st.session_state:
        st.session_state.send_message_list = []
    if len(convos) > 0:  
        if 'text_sent' in st.session_state.send_message_list: 
            st.selectbox("Choose Conversation:",convos,disabled=True)
            st.radio("How would you like the message to be created?", ["Type message","Generate message"],disabled=True)
            if (st.session_state.message_creation == "Type message"):
                st.session_state.text_message = st.text_input("Message (in English)",disabled=True)
            st.session_state.lang = st.selectbox("What language would you like to send the message in",languages.LANGUAGES.values(),disabled=True)
            click = st.button("Submit",disabled=True)
        else:          
            st.session_state.conversation = st.selectbox("Choose Conversation:",convos)
            st.session_state.message_creation = st.radio("How would you like the message to be created?", ["Type message","Generate message"])
            if (st.session_state.message_creation == "Type message"):
                st.session_state.text_message = st.text_input("Message (in English)")
            else:
                st.session_state.text_message = mc.generateMessage()
            st.session_state.lang = st.selectbox("What language would you like to send the message in",languages.LANGUAGES.values())
            click = st.button("Submit", on_click=submit_text)



        if 'text_sent' in st.session_state.send_message_list:

            correct = 'correct_translation' in st.session_state.send_message_list
            incorrect = 'incorrect_translation' in st.session_state.send_message_list
            correct_lang_submitted = 'correct_lang_submitted' in st.session_state.send_message_list
            
            #will rerun when next buttons pressed, so only set language and translation on the first run through
            if not (correct or incorrect or correct_lang_submitted):
                translator = Translator()
                st.session_state.sent_message = translator.translate(st.session_state.text_message,dest=st.session_state.lang).text
                str = re.split('=|,',st.session_state.conversation)
                st.session_state.sender = str[1].strip()
                st.session_state.receiver = str[3].strip()
                sent_id = get_sent_id(st.session_state.sender,st.session_state.receiver)[0]
                abbr = {i for i in languages.LANGUAGES if languages.LANGUAGES[i]==(st.session_state.lang)}.pop()

            #handle special case, cannot have '-' in SQLite
                if abbr == 'zh-cn':
                    abbr = 'zh_cn'

                db.update_history(sent_id,abbr)
                lang_list = db.get_recipient_lang(sent_id)
                st.session_state.label_lang_db = lang_list[0]
                st.session_state.ai_lang_db = lang_list[1]
                st.session_state.label_lang_google = st.session_state.label_lang_db.replace('_','-')
                st.session_state.ai_lang_google = st.session_state.ai_lang_db.replace('_','-')
                #ai_abbr = {i for i in languages.LANGUAGES if languages.LANGUAGES[i]==(st.session_state.ai_lang_db)}.pop()
                st.session_state.received_message = translator.translate(st.session_state.sent_message,dest = st.session_state.ai_lang_google).text
                recipient_history_id = db.get_all_sent_history_info(sent_id).get("recipient_history_id")
                params = db.get_params(recipient_history_id)
                st.session_state.all_messages_lang = languages.LANGUAGES.get(params.get('all_messages_lang'))
                st.session_state.conv_messages_lang = languages.LANGUAGES.get(params.get('conv_messages_lang'))
                st.session_state.last_message_lang = params.pop('last_message_lang')
            
                if st.session_state.last_message_lang != None:
                    st.session_state.last_message_lang = languages.LANGUAGES.get(st.session_state.last_message_lang.replace('_','-'))  

            st.markdown(f'Your message: **{st.session_state.sent_message}**')
            st.success(f"Sent {st.session_state.sender}'s message to {st.session_state.receiver}")
            st.markdown(f'The message {st.session_state.receiver} received is: **{st.session_state.received_message}**')
            st.info(f'Note: this was translated using our AI predicted language')
            st.markdown(f'Our AI predicted the desired language to be: **{languages.LANGUAGES.get(st.session_state.ai_lang_google)}**')
            st.markdown(f'The label for the language decision in this case was: **{languages.LANGUAGES.get(st.session_state.label_lang_google)}**')
            st.markdown(f"Did we get the translation language label right?")
            col1, col2 = st.columns(2)
            
            with col1:
                if not (correct or incorrect or correct_lang_submitted):
                    correct = st.button("Correct", on_click=correct_translation)
                    
                else:
                    st.button("Correct",disabled=True)
                    if correct:
                        st.success(f"Nice!")

            with col2:
                if not (correct or incorrect or correct_lang_submitted):
                    incorrect = st.button("Incorrect", on_click=incorrect_translation)
                else:
                    st.button("Incorrect",disabled=True)
                    if incorrect:

                            if correct_lang_submitted:
                                st.selectbox("What language should it have been?",languages.LANGUAGES.values(),disabled=True)
                                st.button("OK",disabled=True)
                            else:
                                lang = st.selectbox("What language should it have been?",languages.LANGUAGES.values())
                                abbr = {i for i in languages.LANGUAGES if languages.LANGUAGES[i]==(lang)}.pop()

                                st.button("OK",on_click=submit_correct_lang, args=(abbr,))

            if correct_lang_submitted:
                st.success(f"Changed training dataset to have **{st.session_state.correct_lang}** as the correct label")

            st.markdown('### How did we get the translation language label?')
            st.markdown(f'We used the data from the messages {st.session_state.receiver} has sent to decide!') 
            st.markdown(f'Top language of the messages that {st.session_state.receiver} has sent in all conversations: **{st.session_state.all_messages_lang}**')
            st.markdown(f'Top language of the messages that {st.session_state.receiver} has sent to {st.session_state.sender}: **{st.session_state.conv_messages_lang}**')
            st.markdown(f'Language of the last message that {st.session_state.receiver} has sent to {st.session_state.sender}: **{st.session_state.last_message_lang}**')

            try_again = st.button("Send another message", on_click=clear_session_state)

    else:
        st.error('Must create at least one conversation')

if selected == 'View User':
    st.markdown(f'### View User')

    if len(users) >= 1:
        #creates a select box for all of the users
        user = st.selectbox("User:", users.keys(), index=0)

        #will list all of the conversations the user participates in
        ids = db.get_sent_ids(users[user])
        #user will always have their overall sending history, we need to check if they are in more than one row then
        if len(ids) > 1:
            #will list the selected user's parameters
            user_convos = get_user_convos(users[user])
            recipients = dict([(i[1], i[0]) for i in user_convos])
            recipient = st.selectbox("Choose Conversation:", recipients.keys())

            parameters = db.get_all_sent_history_info(recipients.get(recipient))
            #st.write(parameters)

            parameters.pop('is_all_messages')
            parameters.pop('user_id')
            parameters.pop('sent_id')
            parameters.pop('recipient_history_id')

            #will list relevant parameters given in get_all_sent_history_info
            st.markdown(f'### {user}\'s Message History Information')
            all_messages_lang = languages.LANGUAGES.get(parameters.pop('all_messages_lang'))
            conv_messages_lang = languages.LANGUAGES.get(parameters.pop('conv_messages_lang'))
            last_message_lang = parameters.pop('last_message_lang')

            if last_message_lang != None:
                last_message_lang = languages.LANGUAGES.get(last_message_lang.replace('_','-'))              

            total = parameters.pop('total')
            st.markdown(f'Top language of the messages that {user} has sent in all conversations: **{all_messages_lang}**')
            st.markdown(f'Top language of the messages that {user} has sent to {recipient}: **{conv_messages_lang}**')
            st.markdown(f'Language of the last message that {user} has sent to {recipient}: **{last_message_lang}**')

            for item in parameters.items():
                st.markdown(f'Number of messages sent in {languages.LANGUAGES.get(item[0])}' + ': ' + f'{item[1]}')

            st.markdown(f'Total messages that {user} has sent to {recipient}: **{total}**')
        else:
            st.error(f'{user} is not in any conversations')

    else: 
        st.info('Must create at least one user')


