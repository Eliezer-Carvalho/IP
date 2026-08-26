import sqlite3
import datetime


class SQL_FUNCTS:

    def __init__ (self):

        self.PATH = "v1\BackEnd\Assobio\db\BaseDadosAssobio.db"

        self.CONECTOR = sqlite3.connect (self.PATH)


    def ADD_DATA (self, audio, transcrição, auditoria, modelo):

        CURSOR = self.CONECTOR.cursor ()

        data = datetime.datetime.now ()

        CURSOR.execute (
            """
            INSERT INTO Assobio (data, audio, transcrição, auditoria, modelo)
            VALUES (?, ?, ?, ?, ?)
            """
            (data, audio, transcrição, auditoria, modelo)
        )

        self.CONECTOR.commit ()
        self.CONECTOR.close ()


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