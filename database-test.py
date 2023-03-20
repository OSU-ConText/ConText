import database

not_quit = True

while (not_quit):
    print('\n')
    print('Enter a command')
    print('[C]reate tables')
    print('create [U]ser')
    print('create [S]ent history')
    print('[Q]uit the program')

    user_input = input()
    print("\n")

    if (user_input == 'C'):
        database.create_tables()
    elif (user_input == 'U'):
        database.create_user()
    elif (user_input == 'S'):
        user_id_1 = input('What is the first user_id? ')
        user_id_2 = input('What is the second user_id? ')
        database.create_sent_history(user_id_1, user_id_2)
    elif (user_input == 'Q'):
        print('Thanks for stopping by!')
        not_quit = False
    else:
        print('Invalid input, please try again')