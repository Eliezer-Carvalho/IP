import sqlite3
import datetime

"""
Esta classe serve como ponte para contactar a base de dados SQL do sistema Assobio.
Tanto é possível extrair dados como adicionar dados.
"""

"""
################# Código Para Criar Database #########################################

CONECTOR = sqlite3.connect (r"C:\Users\Admin\Desktop\ip\Automatic Speech Recognition\v2\Backend\AssobioAuditoria\db\SQLDatabaseAssobio.db")

CURSOR = CONECTOR.cursor ()

CURSOR.execute (
    CREATE TABLE Assobio
    (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DATA TEXT NOT NULL,
    AUDIO_ORIGINAL TEXT NOT NULL,
    AUDIO_PRÉ_PROCESSADO TEXT NOT NULL,
    AUDIO_TIME FLOAT NOT NULL,
    TEMPO_PRÉ_PROCESSAMENTO FLOAT NOT NULL,
    TRANSCRIÇÃO TEXT NOT NULL,
    TEMPO_PROCESSAMENTO_MODELO_ASR FLOAT NOT NULL,
    TEMPO_INFERÊNCIA_MODELO_ASR FLOAT NOT NULL,
    LATÊNCIA FLOAT NOT NULL,
    TOKENS_PER_SECOND_DECODE FLOAT NOT NULL,
    HARDWARE_LLM TEXT NOT NULL,
    MODELO_LLM TEXT NOT NULL,
    AUDITORIA_LLM TEXT NOT NULL,
    NÚMERO_DE_TOKENS_PROCESSADOS INTEGER NOT NULL,
    TEMPO_PREFILL_LLM FLOAT NOT NULL,
    TOKENS_PER_SECOND_PREFILL_LLM FLOAT NOT NULL,
    TEMPO_DECODE_LLM FLOAT NOT NULL,
    TOKENS_PER_SECOND_DECODE_LLM FLOAT NOT NULL,
    LATÊNCIA_LLM FLOAT NOT NULL
    )
)

CONECTOR.commit ()
"""



class SQL_FUNCTS:

    def __init__ (self):

        """
        Método construtor, inicia variáveis importantes.
        """

        self.PATH = "v2\Backend\AssobioAuditoria\DatabaseAssobioAuditoria\SQLDatabaseAssobio.db"


    def ADD_DATA (self, AUDIO_ORIGINAL, AUDIO_PRÉ_PROCESSADO, AUDIO_TIME, TEMPO_PRÉ_PROCESSAMENTO, TRANSCRIÇÃO, TEMPO_PROCESSAMENTO_MODELO_ASR, TEMPO_INFERÊNCIA_MODELO_ASR, LATÊNCIA, TOKENS_PER_SECOND_DECODE, HARDWARE_LLM, MODELO_LLM, AUDITORIA_LLM, NÚMERO_DE_TOKENS_PROCESSADOS, TEMPO_PREFILL_LLM, TOKENS_PER_SECOND_PREFILL_LLM, TEMPO_DECODE_LLM, TOKENS_PER_SECOND_DECODE_LLM, LATÊNCIA_LLM):

        CONECTOR = sqlite3.connect (self.PATH)

        CURSOR = CONECTOR.cursor ()

        data = datetime.datetime.now ()

        ##### CONTINUAR AQUI

        CURSOR.execute ( 
            """
            INSERT INTO Assobio (data, audio, transcrição, auditoria, modelo)
            VALUES (?, ?, ?, ?, ?)
            """,
            (data, audio, transcrição, auditoria, modelo)
        )

        CONECTOR.commit ()
        CONECTOR.close ()


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
        #AVAL = LOG[6] # Nesta versão 2 fuck AVAL

        CONECTOR.close ()

        return DATA, AUDIO, TRANS, AUDITORIA, MODEL # Para retornar todos 