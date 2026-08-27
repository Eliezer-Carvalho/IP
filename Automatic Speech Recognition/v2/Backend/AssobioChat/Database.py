import sqlite3
import datetime

"""
CONECTOR = sqlite3.connect ("v2\Database\AssobioChat.db")

CURSOR = CONECTOR.cursor ()

CURSOR.execute (
    
    CREATE TABLE AssobioChats
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    modelo TEXT NOT NULL,
    chat TEXT NOT NULL
    )
    
)

CONECTOR.commit ()
"""


class SQL_FUNCT_ASSOBIOCHAT:

    def __init__ (self):

        self.PATH = ("v2\Database\AssobioChat.db")


    def ADD_CHAT_HISTORY (self, chat):

        CONECTOR = sqlite3.connect (self.PATH)

        CURSOR = CONECTOR.cursor ()

        data = datetime.datetime.now ()
        modelo = "Microsoft Phi 4 Q4.0"

        CURSOR.execute (
            """
            INSERT INTO AssobioChats (data, modelo, chat)
            VALUES (?, ?, ?)
            """,
            (data, modelo, str(chat))
        )

        CONECTOR.commit ()
        CONECTOR.close ()


    def CHAT_HISTORY (self)_

        CONECTOR = sqlite3.connect (self.PATH)

        CURSOR = CONECTOR.cursor ()

        CURSOR.execute (

            """
            SELECT 

            """
        )