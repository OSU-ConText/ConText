import database

not_quit = True

while (not_quit):
    print('\n')
    print('Enter a command')
    print('[C]reate a new table')
    print('show [A]ll records')
    print('insert [R]ow')
    print('[G]et rating')
    print('[I]ncrement times you have watched a movie')
    print('do [D]atabase operations (depreciated, use may result in crash / nonsensicalness)')
    print('[Q]uit the program')

    user_input = input()
    print("\n")

    if (user_input == 'C'):
        database.create_table()
    elif (user_input == 'A'):
        database.show_all()
    elif (user_input == 'D'):
        database.database_operations()
    elif (user_input == 'R'):
        database.insert_row()
    elif (user_input == 'G'):
        database.get_score()
    elif (user_input == 'I'):
        database.increment_watched()
    elif (user_input == 'Q'):
        print('Thanks for stopping by!')
        not_quit = False
    else:
        print('Invalid input, please try again')