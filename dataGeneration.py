import random
import database
import languages
import userCreation

#generates 10 users and their personas
def generateUsers():
    user_personas  = {}
    user_personas = userCreation.createUsers(10)
    return user_personas

#generate conversations between users ?? hard part
#pass in dictionary of user personas
def generateConvos(user_personas):
    #one possible method:
    #store user ids in an array
    #iterate thru and randomly assign each user to 2 other users and start 2 conversations:
    #e.g. assign user 1 to user 2 and 3, then have a convo between user 1 and user 2,
    #then user 1 and user 3, etc.
    #if convo already exists between two users, assign them a different user
    return

#send a message in a conversation
#pass in user_personas dictionary and conversation id
#determine message language from user persona
#send message in choosen language in a certain conversation
def sendInConvo(user_personas, sentId):
    lang = userCreation.generateMessageLanguage(user_personas)
    userCreation.sendMessage(sentId, lang)

