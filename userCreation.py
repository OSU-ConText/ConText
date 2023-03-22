from googletrans import Translator
from wonderwords import RandomSentence
import random
import messageCreation
import database
import languages

#global variable to store users and their personas (languages)
user_personas = {}

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



