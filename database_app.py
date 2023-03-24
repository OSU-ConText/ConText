import database
import database_helper

not_quit = True

while (not_quit):
    print('\n')
    print('Enter a command')
    print('[C]reate tables')
    print('create [U]ser')
    print('create [S]ent history')
    print('[G]et preferred language for a user')
    print('[GR] Get row information for a sent history')
    print('[SU] Get users for a particular sent_id')
    print('[SI] Get sent ids for a particular user_id')
    print('[UP]date the language count for a sent_id')
    print('[Q]uit the program')

    user_input = input()
    print("\n")

    if (user_input == 'C'):
        database_helper.create_tables()
    elif (user_input == 'U'):
        database.create_user()
    elif (user_input == 'S'):
        user_id_1 = input('What is the first user_id? ')
        user_id_2 = input('What is the second user_id? ')
        database.create_sent_history(user_id_1, user_id_2)
    elif (user_input == 'G'):
        sent_id = input('What sent_id would you like to get the preferred language for?  (Keep in mind this is based off the recipient_history_id) ')
        print(database.get_recipient_lang(sent_id))
    elif (user_input == 'GR'):
        sent_id = input('What sent_id would you like to get info for?')
        print(database.get_all_sent_history_info(sent_id))
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
    elif (user_input == "UP"):
        sent_id = input('What sent_id would you like to update?')
        lang = input('What language would you like to update?')
        database.update_history(sent_id, lang)
    elif (user_input == 'Q'):
        print('Thanks for stopping by!')
        not_quit = False
    else:
        print('Invalid input, please try again')