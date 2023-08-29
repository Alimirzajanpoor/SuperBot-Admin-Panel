import sqlite3
from sqlite3 import Error


import sqlite3

connection = sqlite3.connect("pythonsqlite.db")
cursor = connection.cursor()


def creating_sessions_table(): # func for making our session table
    cursor.execute(
        """CREATE TABLE sessions (session_id char(128) UNIQUE NOT NULL ,atime timestamp NOT NULL default current_timestamp
         ,data text) """)
    print ('session table has created')


def creating_usersdata_table(): # func for making our userdata table
    cursor.execute("""CREATE TABLE user_ids(
    chat_id integer unique,username text ,firstname text)
    """)
    print ("usersdata table has created")


creating_usersdata_table()
