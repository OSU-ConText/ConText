from googletrans import Translator
from wonderwords import RandomSentence
import msgGeneration
import database

#need database functions that can: 
# query for a specific user, 
# query for a specific conversation, 
# show all conversations for a specific user

def messageSimulation():
    sendMessage()
    return

def printStats(user):
    #read from database for a certain user
    #format and print stats to console
    return

def sendMessage(userLanguage):
    #have user input the language they want to send a message in
    #create a new user
    database.create_user()
    #display user row in database
    user = findUser()
    printStats(user)
    #create a conversation for the user
    database.create_conversation()
    #display user conversations in database
    findUserConversations()
    #select a certain conversation we want to update/send a message in
    selectUserConversation()
    #send a message in messageTranslation function
    sendMessageInConvo(userLanguage)
    #print out database row to show update worked (lang parameters were successfully updated)
    database.get_language_columns()
    return

#function that calls database backend function to return all conversations for a specific user
def findUserConversations():
    return

#function that selects the conversation we are going to send a message in
def selectUserConversation():
    return

#function that calls database backend functions to return the row for a specific user
def findUser():
    return

#funtion that simulates sending a message
def sendMessageInConvo(userLanguage):
    #"send" one message
    message = msgGeneration.generateMessage
    print(message)
    lang = msgGeneration.detectLang
    print(lang)
    msgGeneration.translateMessage(userLanguage, lang, message)
    lang = msgGeneration.detectLang
    print(lang)
    database.increment_count(lang)