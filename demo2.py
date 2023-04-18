from googletrans import Translator
import messageCreation
import database

not_quit = True
translator = Translator()
while (not_quit):
    print('\n')
    print('Enter a command')
    print('[U] Create a new user')
    print('[C] Create a new conversation')
    print('[P] Print context parameters for a conversation')
    print('[F] Find the users in a conversation')
    print('[FC] Find all conversations a user is in')
    print('[T] Send a text in a conversation')
    print('[Q] End Demo')

    user_input = input()
    # create a user and print userid in the database
    if (user_input == 'U'):
        user = database.create_user()
        print("User " + str(user) + " has been created and added to the database")
    # create a conversation between two users
    elif (user_input == 'C'):
        user_id_1 = input('What is the first user_id? ')
        user_id_2 = input('What is the second user_id? ')
        database.create_sent_history(user_id_1, user_id_2)
        print("A conversation between user " + str(user_id_1) + " and user " + str(user_id_2) + " has been started and added to the database")
    #Fetch datas from an conversation
    elif (user_input == 'P'):
        sent_id = input('What conversation would you like to gather data from?\n')
        history = database.get_all_sent_history_info(sent_id)
        print(history)
    # get users involved in an conversation
    elif (user_input == 'F'):
        sent_id = input('What conversation would you like to get the details of? ')
        users = database.get_users_sent_history(sent_id)
        user1 = users[0]
        user2 = users[1]
        print("The sender in the conversation is: " , user1 ,", the receiver in the conversation is: ", user2 , "\n")
    # Get all conversation the user is in as a sender
    elif (user_input == 'FC'):
        user_id = input('What user would you like to view conversations for? ')
        sent_ids = database.get_sent_ids(user_id)
        pos_convos = [ele for ele in sent_ids if ele > 0]
        print("conversations user", user_id, " is in: ",pos_convos)
    
    #sent typed message in specified language with sent_id entered by user
    elif(user_input == 'T'):
        sent_id = input("\nWhat conversation would you like to send a message in?\n")
        user_input = input("Do you want to [G]enerate a random message or [T]ype a message?\n")
        if (user_input == "T"):
            text_message = input("Type the message you want to send in English\n")
        else:
            text_message = messageCreation.generateMessage()
        lang = input("What language would you like to send the message in\n")
        sent_message = translator.translate(text_message,dest=lang).text
        print("\nThe sentence you sent is:\n" + sent_message + "\n")
        database.update_history(sent_id,lang)
        received_lang = database.get_recipient_lang(sent_id)[0]
        received_message = translator.translate(sent_message,dest = received_lang).text
        print("\nThe translated sentence received by the other user in the conversation is:\n " + received_message + "\n")
        print("\nThe language of the sentence the user received is: " + received_lang)

    elif (user_input == 'Q'):
        print('Thanks for stopping by!')
        not_quit = False
    else:
        print('Invalid input, please try again')

        
