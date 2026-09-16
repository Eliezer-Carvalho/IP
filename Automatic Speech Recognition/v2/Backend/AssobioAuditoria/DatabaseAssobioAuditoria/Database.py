import sqlite3
import datetime

"""
Esta classe serve como ponte para contactar a base de dados SQL do sistema Assobio.
Tanto é possível extrair dados como adicionar dados.
"""

"""
################# Código Para Criar Database #########################################

CONECTOR = sqlite3.connect (r"C:/Users/Admin/Desktop/ip/Automatic Speech Recognition/v2/Backend/AssobioAuditoria/db/SQLDatabaseAssobio.db")

CURSOR = CONECTOR.cursor ()

CURSOR.execute (
    CREATE TABLE Assobio
    (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DATA TEXT NOT NULL,
    CONTEXT TEXT NOT NULL,
    PROMPT TEXT NOT NULL,
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



class SQL_Functions:

    def __init__ (self):

        """
        Método construtor, inicia variáveis importantes.
        """

        self.PATH = "v2\Backend\AssobioAuditoria\DatabaseAssobioAuditoria\SQLDatabaseAssobio.db"


    def ADD_DATA (self, CONTEXT, PROMPT, AUDIO_ORIGINAL, AUDIO_PRÉ_PROCESSADO, AUDIO_TIME, TEMPO_PRÉ_PROCESSAMENTO, TRANSCRIÇÃO, TEMPO_PROCESSAMENTO_MODELO_ASR, TEMPO_INFERÊNCIA_MODELO_ASR, LATÊNCIA, TOKENS_PER_SECOND_DECODE, HARDWARE_LLM, MODELO_LLM, AUDITORIA_LLM, NÚMERO_DE_TOKENS_PROCESSADOS, TEMPO_PREFILL_LLM, TOKENS_PER_SECOND_PREFILL_LLM, TEMPO_DECODE_LLM, TOKENS_PER_SECOND_DECODE_LLM, LATÊNCIA_LLM):

        """
        Método que após correr a Auditoria, adiciona toda a informação à DataBase.
        Não é o código mais bonito but it does the job.
        """

        CONECTOR = sqlite3.connect (self.PATH)
        CURSOR = CONECTOR.cursor ()

        DATA = datetime.datetime.now ()

        CURSOR.execute ( 
            """
            INSERT INTO Assobio (DATA, CONTEXT, PROMPT, AUDIO_ORIGINAL, AUDIO_PRÉ_PROCESSADO, AUDIO_TIME, TEMPO_PRÉ_PROCESSAMENTO, TRANSCRIÇÃO, TEMPO_PROCESSAMENTO_MODELO_ASR, TEMPO_INFERÊNCIA_MODELO_ASR, LATÊNCIA, TOKENS_PER_SECOND_DECODE, HARDWARE_LLM, MODELO_LLM, AUDITORIA_LLM, NÚMERO_DE_TOKENS_PROCESSADOS, TEMPO_PREFILL_LLM, TOKENS_PER_SECOND_PREFILL_LLM, TEMPO_DECODE_LLM, TOKENS_PER_SECOND_DECODE_LLM, LATÊNCIA_LLM)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (DATA, CONTEXT, PROMPT, AUDIO_ORIGINAL, AUDIO_PRÉ_PROCESSADO, AUDIO_TIME, TEMPO_PRÉ_PROCESSAMENTO, TRANSCRIÇÃO, TEMPO_PROCESSAMENTO_MODELO_ASR, TEMPO_INFERÊNCIA_MODELO_ASR, LATÊNCIA, TOKENS_PER_SECOND_DECODE, HARDWARE_LLM, MODELO_LLM, AUDITORIA_LLM, NÚMERO_DE_TOKENS_PROCESSADOS, TEMPO_PREFILL_LLM, TOKENS_PER_SECOND_PREFILL_LLM, TEMPO_DECODE_LLM, TOKENS_PER_SECOND_DECODE_LLM, LATÊNCIA_LLM)
        )

        CONECTOR.commit ()
        CONECTOR.close ()


    def IDX_SQL (self):

        """
        Método para descobrir quantas linhas existem na DataBase.
        Importante para enviar a informação ao FrontEnd
        """

        CONECTOR = sqlite3.connect (self.PATH)
        CURSOR = CONECTOR.cursor ()

        IDX_MAX = CURSOR.execute (
            """
            SELECT ID FROM Assobio
            """
        )

        list = [idx[0] for idx in IDX_MAX.fetchall()] # Dropdown aceita um lista por isso temos de converter

        CONECTOR.close ()
        return list

   
    def VIEW_SQL (self, id):

        """
        Método para visualizar o SQL no FrontEnd.
        Recebe o id que corresponde ao idx selecionado pelo frontend e depois distribui a informação por variáveis
        """

        CONECTOR = sqlite3.connect (self.PATH)

        CURSOR = CONECTOR.cursor ()

        CURSOR.execute (
            """ 
            SELECT * 
            FROM Assobio
            WHERE ID = ?
            """,
            (id,)
            )

        LOG = CURSOR.fetchone() #fetchone | fetchall

        DATA = LOG[1]
        CONTEXT = LOG[2]
        PROMPT = LOG [3]
        AUDIO_ORIGINAL = LOG[4]
        AUDIO_PRÉ_PROCESSADO = LOG[5]
        AUDIO_TIME = LOG[6]
        TEMPO_PRÉ_PROCESSAMENTO = LOG[7]
        TRANSCRIÇÃO = LOG[8]
        TEMPO_PROCESSAMENTO_MODELO_ASR = LOG[9]
        TEMPO_INFERÊNCIA_MODELO_ASR = LOG[10]
        LATÊNCIA = LOG[11]
        TOKENS_PER_SECOND_DECODE = LOG[12]
        HARDWARE_LLM = LOG[13]
        MODELO_LLM = LOG[14]
        AUDITORIA_LLM = LOG[15]
        NÚMERO_DE_TOKENS_PROCESSADOS = LOG[16]
        TEMPO_PREFILL_LLM = LOG[17]
        TOKENS_PER_SECOND_PREFILL_LLM = LOG[18]
        TEMPO_DECODE_LLM = LOG[19]
        TOKENS_PER_SECOND_DECODE_LLM = LOG[20]
        LATÊNCIA_LLM = LOG[21]

        CONECTOR.close ()

        return DATA, CONTEXT, PROMPT, AUDIO_ORIGINAL, AUDIO_PRÉ_PROCESSADO, AUDIO_TIME, TEMPO_PRÉ_PROCESSAMENTO, TRANSCRIÇÃO, TEMPO_PROCESSAMENTO_MODELO_ASR, TEMPO_INFERÊNCIA_MODELO_ASR, LATÊNCIA, TOKENS_PER_SECOND_DECODE, HARDWARE_LLM, MODELO_LLM, AUDITORIA_LLM, NÚMERO_DE_TOKENS_PROCESSADOS, TEMPO_PREFILL_LLM, TOKENS_PER_SECOND_PREFILL_LLM, TEMPO_DECODE_LLM, TOKENS_PER_SECOND_DECODE_LLM, LATÊNCIA_LLM # Para retornar todos 