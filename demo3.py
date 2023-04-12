
import streamlit as st
import pandas as pd
import database
import sqlite3

@st.cache_resource
def loadDatabase():
    return sqlite3.connect("demo3.db", check_same_thread=False)

@st.cache_data
def query():
    return pd.read_sql_query("SELECT * from users", connection)

options = ['Create User', 'Create Conversation', 'Send Message', 'Show Context Parameters']
selected = st.radio('Choose Functionality:', options)



st.session_state.users = {}
connection = loadDatabase()
if selected == 'Create User':
    st.text_input("Name", key='name')
    # #change with user's id
    clicked = st.button('Create')
    if clicked: 
        user = st.session_state.name
        st.text(f'Welcome {user}!')
        user_id = database.create_user()
        st.text(f'User id {user_id}!')
        st.session_state.users[user] = user_id
    st.session_state.users
    
if selected == 'Create Conversation':
    user_options = list(st.session_state.users.keys())
    st.text(user_options)
    user_1_selected = st.selectbox('User 1', user_options)
    clicked = st.button('OK')
    if clicked:
        user_options.remove(user_1_selected)
        user_2_selected = st.selectbox('User 2', st.session_state.users.keys())
        clicked_2 = st.button('OK')

if selected == 'Show Context Parameters':
    query()


