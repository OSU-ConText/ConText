import training_data_tables

not_quit = True

while (not_quit):
    print('\n')
    print('Enter a command')
    print('[C] Create Table')
    print('[P] Parse Data')
    print('[Q] Quit program')

    user_input = input()
    print("\n")

    if (user_input == 'C'):
        training_data_tables.create_table_mulitcolumn()
        print('tables created')
    elif (user_input == 'P'):
        recipient_history_id = int(input('recipient_history_id? '))
        decision_lang = input('decision_lang? ')
        training_data_tables.parse_data(recipient_history_id, decision_lang)
    elif (user_input == 'Q'):
        print('Thanks for stopping by!')
        not_quit = False
    else:
        print('Invalid input, please try again')