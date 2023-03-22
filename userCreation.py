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

#creates two users, and a conversation
def createConversation():
    user_one = createUser()
    user_two = createUser()
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
    rand = random.randint(1, len(convos))
    user_generated_lang = generateMessageLanguage(user_id)
    sendMessage(rand, user_generated_lang)