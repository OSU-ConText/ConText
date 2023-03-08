from googletrans import Translator
from wonderwords import RandomSentence

#generates random sentence in English
def generateMessage():
    r = RandomSentence() #defining the random sentence
    sentence = r.simple_sentence()
    return sentence

#translates a message from a specificed srcLang to a specified destLang
def translateMessage(destLang, srcLang, message):
    translator = Translator() #defining the translator object
    #translator = Translator(service_urls=['translate.googleapis.com'])
    translated_sentence = translator.translate(message, dest=destLang, src=srcLang) 
    translated_wanted_sentence = translated_sentence.text 
    print(translated_wanted_sentence)
    return translated_wanted_sentence

#todo: implement language detection function
#todo: send/receive message functions that update db
#todo: function to pulls all of user's stats from db and prints them out
#above functions might need to be put in separate files

translateMessage("fr", "en", "Hello my name is mallory")