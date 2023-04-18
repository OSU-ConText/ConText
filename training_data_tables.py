import database
import database_helper
import languages

table_with_all_langs_and_id = "table_with_all_langs_and_id"

def get_language_columns_for_test_data_creation():
    str = ' REAL DEFAULT 1, '.join(languages.LANGUAGES.keys())
    str += ' REAL DEFAULT 1)'

    #character - not allowed in sqlite column names
    str = str.replace('-', '_')
    return str

def create_table_with_all_langs_and_id():
    if (database_helper.check_table_existence(table_with_all_langs_and_id, True) == False):
        database.cur.execute(f'''CREATE TABLE {table_with_all_langs_and_id}
        (row_id INTEGER PRIMARY KEY AUTOINCREMENT, label TEXT, ''' 
        + get_language_columns_for_test_data_creation())

def record_training_data_all_langs(sent_id, decision_lang):
    params = database.get_params(sent_id)        
    create_table_with_all_langs_and_id()

    insertion = f"""INSERT INTO {table_with_all_langs_and_id} (label) VALUES (\'{decision_lang}\')"""
    insertion = insertion.replace('-', '_')
    database.cur.execute(insertion)

    id = database.cur.lastrowid
    print(id)
    
    if params["all_messages_lang"] != None:
        update = f"""UPDATE {table_with_all_langs_and_id} SET {params["all_messages_lang"]} = {params["all_messages_lang"]} + 1 WHERE row_id = {id}"""
        update = update.replace('-', '_')
        database.cur.execute(update)

    if params["conv_messages_lang"] != None:
        update2 = f"""UPDATE {table_with_all_langs_and_id} SET {params["conv_messages_lang"]} = {params["conv_messages_lang"]} + 1 WHERE row_id = {id}"""
        update2 = update2.replace('-', '_')
        database.cur.execute(update2)
    
    if params["last_message_lang"] != None:
        update3 = f"""UPDATE {table_with_all_langs_and_id} SET {params["last_message_lang"]} = {params["last_message_lang"]} + 1 WHERE row_id = {id}"""
        update3 = update3.replace('-', '_')
        database.cur.execute(update3)






    

    



