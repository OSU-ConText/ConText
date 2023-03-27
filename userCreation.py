from googletrans import Translator
from wonderwords import RandomSentence
import random
import database_helper
import database
import languages

#global variable to store users and their personas (languages)
user_personas = {}

def createUserPersona(user_id):
    user_langs = []
    num_languages = random.randint(1, 5)
    for i in range(num_languages):
        user_langs.insert(i, random.choice(list(languages.LANGUAGES.keys())))
    user_personas[user_id] = user_langs


#creates a user and their list of languages
def createUser():
    user_id = database.create_user()
    createUserPersona(user_id)
    return user_id

#randomly chooses a language from the users list
def generateMessageLanguage(user_id):
    createUserPersona(user_id)
    persona = (user_personas[user_id])
    users_langs = user_personas[user_id]
    choosenLang = random.choice(users_langs)
    return choosenLang

#creates conversation between two users
def createConversation(user_one,user_two):
    database.create_sent_history(user_one, user_two)

#send a message, update history
def sendMessage(sent_id, lang):
    database.update_history(sent_id, lang)

#return all conversations for a user
def getConversations(user_id):
    user_convos = []
    user_convos = database.get_sent_ids(user_id)
    return user_convos

#return receivers preferred language
def receiverLang(sent_id):
    lang = database.get_recipient_lang(sent_id)
    return lang

#finds all of a given users conversations, chooses a random conversation to send a message in
#sends a message in a randomly generated language
def sendInConversation(convoId, user_generated_lang):
    sendMessage(convoId, user_generated_lang)

def checkLangForDashes(lang):
    if "-" in lang:
        newString = lang.replace("-", "_")
        return newString
    else:
        return lang

#Starts multiple conversations for each user
def generateConversations():

    #create 10 users (find a way to pass in a value so we can choose num users?)
    for i in range(10):
        createUser()

    #create conversations between users
    for i, user1 in enumerate(user_personas):
        for user2 in (list(user_personas.keys())[i+1:]):
            createConversation(user1, user2)
    
    #find all user ids
    user_ids = user_personas.keys()
    #iterate through all users
    for id in user_ids:
        #find one of their conversations
        convos = getConversations(id)
        pos_convos = [ele for ele in convos if ele > 0]
        #iterate through actual convos (with positive sent_ids in table)
        for i in range(len(pos_convos)):
            #send between 1 and 5 messages in the convo
            user_generated_lang = generateMessageLanguage(id)
            #remove dashes (if needed) for sqlite constraint
            user_generated_lang_no_dash = checkLangForDashes(user_generated_lang)
            rand = random.randint(5,10)
            for j in range(rand):
                sendInConversation(pos_convos[i], user_generated_lang_no_dash)

if __name__ == '__main__':
    database_helper.create_tables()
    generateConversations()

    
        



    

