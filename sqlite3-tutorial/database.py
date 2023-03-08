import sqlite3

#connect to the tutorial.db database
con = sqlite3.connect("tutorial.db")
cur = con.cursor()

#Will return True if the table exists, False if it does not
def check_table_existence(table_name, creating=False):
    table_check = cur.execute(f"SELECT name FROM sqlite_master WHERE name='{table_name}'")
    table_exists = table_check.fetchone() != None

    if (not table_exists and creating == False):
        print("The movie table does not exist, please create it first!")

    if (table_exists and creating == True):
        print("Movie table already exists!")

    return table_exists

def create_table():
    if (check_table_existence('movie', True) == False):
        print("creating movie table")
        cur.execute("CREATE TABLE movie(title, year, score, watched)")

def show_all():
    if (check_table_existence('movie') == True):
        print('Showing all records')

        #iterate over results of the query
        for row in cur.execute("SELECT title, year, score, watched FROM movie ORDER BY year"):
            print(row)

def insert_row():
    if (check_table_existence('movie', False) == True):
        movie_name = input('What is the name of the movie? ')
        movie_year = input('What year was the movie released? ')
        movie_rating = input('What is the rating of the movie? ')
        movie_times = input('How many times have you watched the movie? ')

        cur.execute("""
            INSERT INTO movie VALUES
            (?, ?, ?, ?)
        """, 
        (movie_name, int(movie_year), float(movie_rating), int(movie_times)))
        con.commit()

def get_score():
    if (check_table_existence('movie', False) == True):
        movie_name = input('What movie would you like to get the score of? ')

        score = cur.execute("SELECT score FROM movie WHERE title = ?",
        (movie_name,),).fetchall()

        #returns a tuple inside a list, for this particular case we just want the value
        print(score[0][0])

def watched_helper(movie_name):
    watched = cur.execute("SELECT watched FROM movie WHERE title = ?",
    (movie_name,),).fetchall()

    #returns a tuple inside a list, for this particular case we just want the value
    return watched[0][0]

def increment_watched():
    if (check_table_existence('movie', False) == True):
        movie_name = input('What movie have you watched again? ')

        #get the previous number of times the movie was watched and increment
        watched = int(watched_helper(movie_name)) + 1

        #execute query to increment number of times watched
        cur.execute("UPDATE movie SET watched = ? WHERE title = ?",
        (watched, movie_name))

        #Recall: Must commit changes after making them!
        con.commit()
        print(f'Updated the number of times that you have watched {movie_name}!')



def database_operations():
    #this is taken directly from the python3 sql tutorial https://docs.python.org/3/library/sqlite3.html

    res = cur.execute("SELECT name FROM sqlite_master")
    res.fetchone()

    res = cur.execute("SELECT name FROM sqlite_master WHERE name='spam'")
    res.fetchone() is None

    cur.execute("""
        INSERT INTO movie VALUES
            ('Monty Python and the Holy Grail', 1975, 8.2),
            ('And Now for Something Completely Different', 1971, 7.5)
    """)

    con.commit()

    res = cur.execute("SELECT score FROM movie")
    res.fetchall()

    data = [
        ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
        ("Monty Python's The Meaning of Life", 1983, 7.5),
        ("Monty Python's Life of Brian", 1979, 8.0),
    ]
    cur.executemany("INSERT INTO movie VALUES(?, ?, ?)", data)
    con.commit()  # Remember to commit the transaction after executing INSERT

    #iterate over results of the query
    for row in cur.execute("SELECT year, title FROM movie ORDER BY year"):
        print(row)

    #do one more thing
    res = cur.execute("SELECT title, year FROM movie ORDER BY score DESC")
    title, year = res.fetchone()
    print(f'The highest scoring Monty Python movie is {title!r}, released in {year}')