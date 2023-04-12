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

#detects the language of a message using google translate
def detectLang(message):
    translator = Translator()
    return translator.detect(message).lang


