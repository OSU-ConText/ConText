from googletrans import Translator
from wonderwords import RandomSentence
import random
import messageCreation
import database
import languages

#global variable to store users and their personas (languages)
user_personas = {}
#dictionary to store all of a user's messages (userid, list of messages)
all_user_messages = {}
#dictionary to store messages in a specific conversation (convoid, list of messages)
convo_messages = {}

#creates a user and their list of languages
def createUser():
    user_id = database.create_user()
    user_langs = []
    num_languages = random.randint(1, 5)
    for i in range(num_languages):
        user_langs.insert(i, random.choice(list(languages.LANGUAGES.keys())))
    user_personas[user_id] = user_langs
    print(user_personas)
    return user_id

#randomly chooses a language from the users list
def generateMessageLanguage(user_id):
    choosenLang = random.choice(user_personas[user_id])
    print(choosenLang)

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
    lang = database.get_preferred_lang(sent_id)
    return lang

#finds all of a given users conversations, chooses a random conversation to send a message in
#sends a message in a randomly generated language
def sendInConversation(user_id):
    convos = getConversations(user_id)
    # rand = random.randint(1, len(convos))
    conversation_id = convos[1]
    print("*****")
    print(user_id)
    print(conversation_id)
    print("*****")
    user_generated_lang = generateMessageLanguage(user_id)
    sendMessage(conversation_id, user_generated_lang)

#Starts multiple conversations for each user
def generateConversations():
    #one possible method:
    #store user ids in an dict with values being their languages
    #iterate thru and randomly assign each user to 2 other users and start 2 conversations:
    #e.g. assign user 1 to user 2 and 3, then have a convo between user 1 and user 2,
    #then user 1 and user 3, etc.
    #if convo already exists between two users, assign them a different user

    for i in range(10):
        createUser()

    for i, user1 in enumerate(user_personas):
        for user2 in (list(user_personas.keys())[i+1:]):
            createConversation(user1, user2)
            # sendInConversation(user1)

    # for user in user_personas:
    #     sendInConversation(user)

if __name__ == '__main__':
    generateConversations()

    
        



    

