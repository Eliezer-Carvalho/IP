import sqlite3
import datetime

"""
v1 BackEnd Assobio db SQL.md
"""
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


"""
Esta classe tem dentro de si alguns métodos (funções) que permitem Adicionar e Visualizar a DataBase

"""

class SQL_FUNCTS:

    def __init__ (self): 

        """
        Método Construtor
        """
        self.PATH = "v1\BackEnd\Assobio\db\BaseDadosAssobio.db" # Caminho para a DB

###############################################################################################################

    """
    Método para adicionar dados, quando o modelo de Linguagem realizar a Auditoria.
    """
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

###############################################################################################################

    """
    Método para descobrir quantas linhas existem na DataBase.
    Importante para enviar a informação ao FrontEnd
    """
    def IDX_SQL (self):

        CONECTOR = sqlite3.connect (self.PATH)

        CURSOR = CONECTOR.cursor ()

        IDX_MAX = CURSOR.execute (
            """
            SELECT id FROM Assobio
            """
        )


        list = [idx[0] for idx in IDX_MAX.fetchall()] # Dropdown aceita um lista por isso temos de converter

        CONECTOR.close ()

        return list

###############################################################################################################

    """
    Método para visualizar o SQL no FrontEnd.
    Recebe o id que corresponde ao idx selecionado pelo frontend e depois distribui a informação por variáveis
    """
    def VIEW_SQL (self, id):

        CONECTOR = sqlite3.connect (self.PATH)

        CURSOR = CONECTOR.cursor ()

        CURSOR.execute (
            """ 
            SELECT * 
            FROM Assobio
            WHERE id = ?
            """,
            (id,)
            )

        LOG = CURSOR.fetchone() #fetchone | fetchall

        DATA = LOG[1]
        AUDIO = LOG[2]
        TRANS = LOG[3]
        AUDITORIA = LOG[4]
        MODEL = LOG[5]
        AVAL = LOG[6]

        CONECTOR.close ()

        return DATA, AUDIO, TRANS, AUDITORIA, MODEL, AVAL # Para retornar todos 

###############################################################################################################

    """
    Método que permite ao utilizar alterar o valor de avaliação da base de dados.
    """
    def UPDATE_AVAL_SQL (self, aval, id):

        CONECTOR = sqlite3.connect (self.PATH)

        CURSOR = CONECTOR.cursor ()

        CURSOR.execute (
            """
            UPDATE Assobio
            SET score = ?
            WHERE id = ?
            """,
            (aval, id,)
        )

        CONECTOR.commit ()
        CONECTOR.close ()

###############################################################################################################


"""
###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################
########################################### Código Solto ###################################################### 
"""

"""
CONECTOR = sqlite3.connect ("v1\BackEnd\Assobio\db\BaseDadosAssobio.db")

CURSOR = CONECTOR.cursor ()

CURSOR.execute (
    
    SELECT * 
    FROM Assobio
    WHERE id = ?
    (1,)
)

print (CURSOR.fetchone()[5])
""",

"""
CONECTOR = sqlite3.connect ("v1\BackEnd\Assobio\db\BaseDadosAssobio.db")

CURSOR = CONECTOR.cursor ()

IDX_MAX = CURSOR.execute (

    SELECT id FROM Assobio

)


print (IDX_MAX.fetchall())

"""
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