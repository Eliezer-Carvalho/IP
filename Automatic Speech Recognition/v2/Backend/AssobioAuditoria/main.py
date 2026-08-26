
from .SpeechToText import Speech_To_Text
from .AuditoriaSLM import AuditoriaSLM
from .Database import SQL_FUNCTS


STT = Speech_To_Text ()
AUDITORIA_SLM = AuditoriaSLM ()
DATABASE = SQL_FUNCTS ()


def RUN_ASSOBIO_AUDITORIA (path, contexto, prompt):

    STT.LOAD_ASR_MODEL ()

    for audio in path:

        TRANSCRIÇÃO = STT.STT (audio)

        if len (TRANSCRIÇÃO) > 100:

            MODELO = AUDITORIA_SLM.LOAD_MODELO_GPU () 

            AUDITORIA = AUDITORIA_SLM.INFER_GPU (contexto, prompt, TRANSCRIÇÃO)

            DATABASE.ADD_DATA (audio, TRANSCRIÇÃO, AUDITORIA, MODELO)


        else:

            MODELO, SERVER = AUDITORIA_SLM.LOAD_MODELO_CPU ()

            AUDITORIA = AUDITORIA_SLM.INFER_CPU (contexto, prompt, TRANSCRIÇÃO)

            DATABASE.ADD_DATA (audio, TRANSCRIÇÃO, AUDITORIA, MODELO)

            SERVER.terminate ()