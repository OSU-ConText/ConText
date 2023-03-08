import sqlite3

#variables to store name of the tables we are using
user_context_parameter = "user_context_parameter"
message_counts = "message_counts"

#connect to the database
con = sqlite3.connect("context.db")
cur = con.cursor()

#language abbreviations for google translate
LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',}

#Will return True if the table exists, False if it does not
def check_table_existence(table_name, creating=False):
    table_check = cur.execute(f"SELECT name FROM sqlite_master WHERE name='{table_name}'")
    table_exists = table_check.fetchone() != None

    if (not table_exists and creating == False):
        print(f"The {table_name} table does not exist, please create it first!")

    if (table_exists and creating == True):
        print(f"{table_name} table already exists!")

    return table_exists

def get_language_columns():
    str = ', '.join(LANGUAGES.keys())
    return str


#Will create the needed tables if they do not already exist
def create_tables():
    if (check_table_existence(user_context_parameter, True) == False):
        print(f'creating {user_context_parameter} table')
        cur.execute(f"CREATE TABLE {user_context_parameter}(user_id, all_messages_lang, conv_messages_lang, last_message_lang)")
        print(f'{user_context_parameter} table created')

    if (check_table_existence(message_counts, True) == False):
        print(f'creating {message_counts} table')
        cur.execute(f"CREATE TABLE {message_counts}(conv_id, user_id, is_all_messages, " + get_language_columns() + ")")
        print(f'{message_counts} table created')

#Will create a user, inserting a row in both tables to keep track of their parameters and their overall messages counts
def create_user():
    if (check_table_existence(user_context_parameter) == True):
        #automate this step at some point
        user_id = int(input('What numeric user id would you like to assign? '))

        #execute insertion of user and commit
        cur.execute(f"""
            INSERT INTO {user_context_parameter} VALUES
            (?, 0, 0, 0)
        """, 
        (user_id,))
        con.commit()

    #create row in message counts to store all messages history

    #as per schema, conversation id for all message history is user_id * -1
    conv_id = user_id * -1

    if (check_table_existence(message_counts) == True):
        #execute insertion of user and commit
        cur.execute(f"""
            INSERT INTO {message_counts} VALUES
            (?, ?, 0, 0, 0)
        """, 
        (conv_id, user_id))
        con.commit()

#def create_conversation():

#def increment_count(lang):