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

def submit_correct_lang():
    st.session_state.send_message_list.append('correct_lang_submitted')
    
db_created = dbh.check_table_existence("usernames", True)
while (not db_created):
    with st.spinner('Creating database...'):
        dbh.create_tables()
        time.sleep(2)
        db_created = dbh.check_table_existence("usernames", True)

     

options = ['Create User', 'Create Conversation', 'Send Message', 'View User']
selected = st.sidebar.radio('Choose Functionality:', options)

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
    # if "text_sent" not in st.session_state:
    #     st.session_state.text_sent = False
    # if "correct" not in st.session_state:
    #     st.session_state.correct = False
    # if "incorrect" not in st.session_state:
    #     st.session_state.incorrect = False
    # if "correct_lang_submitted" not in st.session_state:
    #     st.session_state.correct_lang_submitted = False
    if len(convos) > 0:  
        if 'text_sent' in st.session_state.send_message_list: 
            st.selectbox("Choose Conversation:",convos,disabled=True)
            st.radio("How would you like the message to be created?", ["Generate message", "Type message"],
                                        index=1,disabled=True)
            if (st.session_state.message_creation == "Type message"):
                st.session_state.text_message = st.text_input("Message (in English)",disabled=True)
            st.session_state.lang = st.selectbox("What language would you like to send the message in",languages.LANGUAGES.values(),disabled=True)
            # Every form must have a submit button.
            click = st.button("Submit",disabled=True)
        else:          
            st.session_state.conversation = st.selectbox("Choose Conversation:",convos)
            st.session_state.message_creation = st.radio("How would you like the message to be created?", ["Generate message", "Type message"],
                                        index=1)#,on_change=st.experimental_rerun)
            if (st.session_state.message_creation == "Type message"):
                st.session_state.text_message = st.text_input("Message (in English)")
            else:
                st.session_state.text_message = mc.generateMessage()
            st.session_state.lang = st.selectbox("What language would you like to send the message in",languages.LANGUAGES.values())
            # Every form must have a submit button.
            click = st.button("Submit", on_click=submit_text)



        if 'text_sent' in st.session_state.send_message_list:
            translator = Translator()
            sent_message = translator.translate(st.session_state.text_message,dest=st.session_state.lang).text
            st.markdown(f'Your message: **{sent_message}**')
            str = re.split('=|,',st.session_state.conversation)
            sender = str[1].strip()
            receiver = str[3].strip()
            sent_id = get_sent_id(sender,receiver)[0]
            abbr = {i for i in languages.LANGUAGES if languages.LANGUAGES[i]==(st.session_state.lang)}.pop()

            db.update_history(sent_id,abbr)
            
            received_lang = db.get_recipient_lang(sent_id)
            received_message = translator.translate(sent_message,dest = received_lang).text
            st.success(f"Sent {sender}'s message to {receiver}")
            st.markdown(f'{receiver} received the message in: **{languages.LANGUAGES.get(received_lang)}**' )
            st.markdown(f'The message {receiver} received is: **{received_message}**')
            st.markdown(f"Did we get that translation language right?")
            col1, col2 = st.columns(2)
            correct = 'correct_translation' in st.session_state.send_message_list
            incorrect = 'incorrect_translation' in st.session_state.send_message_list
            correct_lang_submitted = 'correct_lang_submitted' in st.session_state.send_message_list
            
            with col1:
                if not (correct or incorrect or correct_lang_submitted):
                    correct = st.button("Correct", on_click=correct_translation)
                    
                else:
                    st.button("Correct",disabled=True)
                    if correct:
                        st.success(f"Nice!")
                # if st.session_state.correct or st.session_state.incorrect or st.session_state.correct_lang_submitted:
                #     st.button("Correct",disabled=True)
                #     if st.session_state.correct:
                #         st.success(f"Nice!")
                # else:
                #     correct = st.button("Correct")
                #     if correct:
                #         st.session_state.correct = True


            with col2:
                if not (correct or incorrect or correct_lang_submitted):
                    incorrect = st.button("Incorrect", on_click=incorrect_translation)
                else:
                    st.button("Incorrect",disabled=True)
                    if incorrect:
                        with st.form("incorrect_form", clear_on_submit=False):

                            if correct_lang_submitted:
                                st.selectbox("What language should it have been?",languages.LANGUAGES.values(),disabled=True)
                                st.form_submit_button("OK",disabled=True)
                            else:
                                lang = st.selectbox("What language should it have been?",languages.LANGUAGES.values())
                                st.form_submit_button("OK",on_click=submit_correct_lang)
                # if st.session_state.correct or st.session_state.incorrect or st.session_state.correct_lang_submitted:
                #     st.button("Incorrect",disabled=True)

                #     if st.session_state.incorrect:
                #         with st.form("incorrect_form", clear_on_submit=False):

                #             if st.session_state.correct_lang_submitted:
                #                 st.selectbox("What language should it have been?",languages.LANGUAGES.values(),disabled=True)
                #                 st.form_submit_button("OK",disabled=True)
                #             else:
                #                 lang = st.selectbox("What language should it have been?",languages.LANGUAGES.values())
                #                 pressed = st.form_submit_button("OK")
                #                 if pressed:
                #                     st.session_state.correct_lang_submitted = True
                # else:
                #     incorrect = st.button("Incorrect")
                #     if incorrect:
                #         st.session_state.incorrect = True

            #NEED TO DO SOMETHING WITH THIS
            st.markdown('### How did we get the translation language?')
            st.markdown(f'We used the data from the messages {receiver} has sent to decide!')

            recipient_history_id = db.get_all_sent_history_info(sent_id).get("recipient_history_id")
            params = db.get_params(recipient_history_id)
            all_messages_lang = languages.LANGUAGES.get(params.get('all_messages_lang'))
            conv_messages_lang = languages.LANGUAGES.get(params.get('conv_messages_lang'))
            last_message_lang = languages.LANGUAGES.get(params.get('last_message_lang'))
            st.markdown(f'Top language of the messages that {receiver} has sent in all conversations: **{all_messages_lang}**')
            st.markdown(f'Top language of the messages that {receiver} has sent to {sender}: **{conv_messages_lang}**')
            st.markdown(f'Language of the last message that {receiver} has sent to {sender}: **{last_message_lang}**')

            try_again = st.button("Try again")
            if try_again:
                for key in st.session_state.keys():
                    del st.session_state[key]
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

            parameters.pop('is_all_messages')
            parameters.pop('user_id')
            parameters.pop('sent_id')
            parameters.pop('recipient_history_id')

            #will list relevant parameters given in get_all_sent_history_info
            st.markdown(f'### {user}\'s Message History Information')
            all_messages_lang = languages.LANGUAGES.get(parameters.pop('all_messages_lang'))
            conv_messages_lang = languages.LANGUAGES.get(parameters.pop('conv_messages_lang'))
            last_message_lang = languages.LANGUAGES.get(parameters.pop('last_message_lang'))
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


