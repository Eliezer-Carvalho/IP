import sqlite3
import datetime


"""
########### Criação da DataBase ###########

CONECTOR = sqlite3.connect ("v1\BackEnd\Assobio\db\BaseDadosAssobio.db")

CURSOR = CONECTOR.cursor ()

CURSOR.execute (
    CREATE TABLE Assobio 
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  
    data TEXT NOT NULL, 
    audio TEXT NOT NULL,
    transcrição TEXT NOT NULL,
    auditoria TEXT NOT NULL,
    modelo TEXT NOT NULL,
    score INTEGER
    )
    )

CONECTOR.commit ()
"""


class SQL_FUNCTS:

    def __init__ (self):
    
        self.PATH = "v1\BackEnd\Assobio\db\BaseDadosAssobio.db"


    def ADD_DATA (self, audio, transcrição, auditoria, modelo):

        CONECTOR = sqlite3.connect (self.PATH)

        CURSOR = CONECTOR.cursor ()

        data = datetime.datetime.now ()

        """
        ??? em SQL representa F-string
        """
        CURSOR.execute (
            """
            INSERT INTO Assobio (data, audio, transcrição, auditoria, modelo)
            VALUES (?, ?, ?, ?, ?)
            """,
            (data, audio, transcrição, auditoria, modelo)
            )
        
        CONECTOR.commit () #Commit
        CONECTOR.close () #Close Conector 


"""
CONECTOR = sqlite3.connect ("v1\BackEnd\Assobio\db\BaseDadosAssobio.db")


CURSOR = CONECTOR.cursor ()


x = CURSOR.execute ("SELECT * FROM Assobio")

for y in x:

    print (y)


CONECTOR.close ()
"""

"""
CONECTOR = sqlite3.connect ("v1\BackEnd\Assobio\db\BaseDadosAssobio.db")


CURSOR = CONECTOR.cursor()


CURSOR.execute ("DELETE * FROM UTILIZADORES")

CURSOR.execute ("CREATE TABLE UTILIZADORES (name TXT, age INTEGER)")
CURSOR.execute ("INSERT INTO UTILIZADORES VALUES ('Eliezer', 23)")
"""
#CONECTOR.commit () # Quando alteramos dados
#CONECTOR.close() # Para fechar, bom quando não alteramos nada