from googletrans import Translator
import messageCreation
import random
import database
import languages


#create user 1
#create user 2
#create user 3
#create conversation 1 between user 1 and user 2
#print conversation parameters
#type out a message to send
#translate it into a chosen language
#update database and get receiver preferred language
#translate message to preferred language
#print out updated sender data

#do it again with user 1 and user 3, show different decision because user 3 has different params

#user 1 (POV: person 1) speaks english, spanish
#user 2 (grandma) speaks vietnamese
#user 3 (friend) speaks spanish



#Create Hannah(who talks to grandma in English and friends in spanish)

not_quit = True
translator = Translator()
while (not_quit):
    print('\n')
    print('Enter a command')
    print('create [U]ser')
    print('create [S]ent history')
    print('[P]rint a sent history parameters')
    print('[SU] Get users for a particular sent_id')
    print('[SI] Get sent ids for a particular user_id')
    print('[T]ext a message for a sent_id')
    print('[Q]uit the program')

    user_input = input()
    if (user_input == 'U'):
        database.create_user()
    elif (user_input == 'S'):
        user_id_1 = input('What is the first user_id? ')
        user_id_2 = input('What is the second user_id? ')
        database.create_sent_history(user_id_1, user_id_2)
    elif (user_input == 'P'):
        sent_id = input('what sent_id would you like to gather data from\n')
        history = database.get_all_sent_history_info(sent_id)
        print(history)
    elif (user_input == 'SU'):
        sent_id = input('What sent_id would you like to get the users for? ')
        users = database.get_users_sent_history(sent_id)
        user1 = users[0]
        user2 = users[1]
        print("Users in this conversation: ", user1, ",", user2)
    elif (user_input == 'SI'):
        user_id = input('What user_id would you like to get the sent_ids for? ')
        sent_ids = database.get_sent_ids(user_id)
        print("sent_ids for user", user_id, ":",sent_ids)
    
    #sent typed message in specified language with sent_id entered by user
    elif(user_input == 'T'):
        sent_id = input("\nwhat sent_id would you like to sent the message to\n")
        user_input = input("Do you want to [G]enerate a random message or [T]ype a message\n")
        if (user_input == "T"):
            text_message = input("Type the message you want to send in English\n")
        else:
            text_message = messageCreation.generateMessage()
        lang = input("What language would you like to send the message in\n")
        sent_message = translator.translate(text_message,dest=lang).text
        print("\nThe sentence you sent is:\n" + sent_message + "\n")
        database.update_history(sent_id,lang)
        received_lang = database.get_recipient_lang(sent_id)
        received_message = translator.translate(sent_message,dest = received_lang).text
        print("\nThe sentence received is:\n " + received_message + "\n")

    elif (user_input == 'Q'):
        print('Thanks for stopping by!')
        not_quit = False
    else:
        print('Invalid input, please try again')

        
