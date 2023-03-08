import database

not_quit = True

while (not_quit):
    print('\n')
    print('Enter a command')
    print('[C]reate tables')
    print('create [U]ser')
    print('[Q]uit the program')

    user_input = input()
    print("\n")

    if (user_input == 'C'):
        database.create_tables()
    elif (user_input == 'U'):
        database.create_user()
    elif (user_input == 'Q'):
        print('Thanks for stopping by!')
        not_quit = False
    else:
        print('Invalid input, please try again')