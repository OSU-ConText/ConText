import streamlit as st
import pandas as pd
import database as db
from googletrans import Translator
import sqlite3 
import database_helper as dbh
import data_generation.messageCreation as mc
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

 
def insert_user(name, id):
    with db.con:
        db.cur.execute(f'''INSERT INTO usernames (user_id, name) 
            VALUES ({id}, \'{name}\') ''')

def insert_conversation(sent_id, sender_id, sender_name, receiver_id, receiver_name):
    with db.con:
        db.cur.execute(f'''INSERT INTO conversations 
            (sent_id, sender_id, sender_name, receiver_id, receiver_name)
            
            VALUES ({sent_id}, {sender_id},\'{sender_name}\',{receiver_id},\'{receiver_name}\')''')

if(dbh.check_table_existence("usernames", True) == False):
    dbh.create_tables()
options = ['Create User', 'Create Conversation', 'Send Message']
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
    q = query_usernames()
    users = dict([(value, key) for key, value in q])
    st.markdown('All Users:')
    for user in users:
        st.markdown(f'- {user}') 

if selected == 'Create Conversation':
    st.markdown(f'### Create a Conversation') 
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
            q = query_conversations()   
            c = []
            receiver, sender = "", ""
            for item in q:
                if not (receiver == item[2] and sender == item[4]):
                    sender = item[2]
                    receiver = item[4]
                    c.append(f"{sender} & {receiver}")
            st.markdown('All Convos:')
            for item in c:
                st.markdown(f'- {item}') 
    

if selected == 'Send Message':
    st.markdown(f'### Send a Message')                      
    conversation = st.selectbox("Choose Conversation:",convos)
    message_creation = st.radio("How would you like the message to be created?", ["Generate message", "Type message"],
                                index=1)#,on_change=st.experimental_rerun)
    if (message_creation == "Type message"):
        text_message = st.text_input("Message (in English)")
    else:
        text_message = mc.generateMessage()
    lang = st.selectbox("What language would you like to send the message in",languages.LANGUAGES.values())
    # Every form must have a submit button.
    submitted = st.button("Submit")
    if submitted:
        translator = Translator()
        sent_message = translator.translate(text_message,dest=lang).text
        st.markdown(f'Your message: **{sent_message}**')
        str = re.split('=|,',conversation)
        sender = str[1].strip()
        receiver = str[3].strip()
        sent_id = get_sent_id(sender,receiver)[0]
        abbr = {i for i in languages.LANGUAGES if languages.LANGUAGES[i]==lang}.pop()

        db.update_history(sent_id,abbr)
        
        
        received_lang = db.get_recipient_lang(sent_id)
        received_message = translator.translate(sent_message,dest = received_lang).text
        st.markdown(f'{receiver} received the message in: **{received_lang}**' )
        st.markdown(f'The message {receiver} received is: **{received_message}**')
        st.markdown('### Why?')
        st.markdown(f'We used the data from the messages {receiver} has sent to decide!')

        recipient_history_id = db.get_all_sent_history_info(sent_id).get("recipient_history_id")
        params = db.get_params(recipient_history_id)
        all_messages_lang = params.get('all_messages_lang')
        conv_messages_lang = params.get('conv_messages_lang')
        last_message_lang = params.get('last_message_lang')
        st.markdown(f'Top language of the messages that {receiver} has sent in all conversations: **{all_messages_lang}**')
        st.markdown(f'Top language of the messages that {receiver} has sent in this conversation with {sender}: **{conv_messages_lang}**')
        st.markdown(f'Language of the last message that {receiver} has sent in this conversation with {sender}: **{last_message_lang}**')


