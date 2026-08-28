import sqlite3
import datetime

import json

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

        print (type(chat))

        CURSOR = CONECTOR.cursor ()

        data = datetime.datetime.now ()
        modelo = "Microsoft Phi 4 Q4.0"
        chat = json.dumps (chat, ensure_ascii = False) # Para conseguir armazenar JSON válido na base de dados SQLite
        
        CURSOR.execute (
            """
            INSERT INTO AssobioChats (data, modelo, chat)
            VALUES (?, ?, ?)
            """,
            (data, modelo, chat)
        )

        CONECTOR.commit ()
        CONECTOR.close ()


    def NUMBER_CHATS (self):

        CONECTOR = sqlite3.connect (self.PATH)

        CURSOR = CONECTOR.cursor ()

        CHAT = CURSOR.execute (

            """
            SELECT id, chat FROM AssobioChats
            """
        )

        CHAT = CURSOR.fetchall ()
        CONECTOR.close ()

        #print (CHAT)

        TITLE = []
        
        for idx, conversas in CHAT:

            hist = json.loads (conversas)

            USER_CONTENT = str(hist[0][0]["content"])
            ASSISTANT_CONTENT = str(hist[1][0]["content"])  

            TOTAL_CONTENT = "".join (USER_CONTENT + ASSISTANT_CONTENT)

            TITLE.append ((TOTAL_CONTENT[:30], idx))
            

        #print (TITLE)
            #print (hist) # Printa Tudo!
            #print (hist[0]) # Printa Prompt
            #print (hist[0][0]) # Printa Prompt em Dict
            #print (type(hist))
        
        #print (TITLE)
        return TITLE


    def GET_CHAT (self, idx):

        CONECTOR = sqlite3.connect (self.PATH)
        
        CURSOR = CONECTOR.cursor ()
        
        CHAT = CURSOR.execute (
        
            """
            SELECT chat FROM AssobioChats
            WHERE id = ?
            """,
            (idx,)
        )
        
        CHAT = CURSOR.fetchone ()
        CONECTOR.close ()

        teste = json.loads (CHAT[0])

        x = []

        for y in teste:
            for z in y:
                x.append (z)

        return (x)
        
        


TESTE = SQL_FUNCT_ASSOBIOCHAT ()


TESTE.NUMBER_CHATS ()


