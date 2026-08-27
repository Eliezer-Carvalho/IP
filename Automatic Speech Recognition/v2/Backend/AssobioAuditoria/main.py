
from .SpeechToText import Speech_To_Text
from .AuditoriaSLM import AuditoriaSLM
from .Database import SQL_FUNCTS

import gc
import torch


STT = Speech_To_Text ()
AUDITORIA_SLM = AuditoriaSLM ()
DATABASE = SQL_FUNCTS ()


def RUN_ASSOBIO_AUDITORIA (path, contexto, prompt):

    STT.LOAD_ASR_MODEL ()

    for audio in path:

        yield "A começar Transcrição..."
        TRANSCRIÇÃO = STT.STT (audio)
        yield "Transcrição Terminada!"

        #print (len(TRANSCRIÇÃO)) # Número de Chars

        if len (TRANSCRIÇÃO) > 500:

            yield "A carregar modelo na GPU..."
            MODELO_SELECIONADO, TOKENIZER, MODELO = AUDITORIA_SLM.LOAD_MODELO_GPU () 
            yield "Modelo carregado na GPU com sucesso!"

            yield "A começar inferência..."
            AUDITORIA = AUDITORIA_SLM.INFER_GPU (contexto, prompt, TRANSCRIÇÃO)
            yield "Inferência Terminada!"

            DATABASE.ADD_DATA (audio, TRANSCRIÇÃO, AUDITORIA, MODELO_SELECIONADO)
            yield "Adicionado à Base de Dados!"

            del TOKENIZER, MODELO
            gc.collect ()
            torch.cuda.empty_cache ()

        else:

            yield "A carregar modelo na CPU..."
            MODELO, SERVER = AUDITORIA_SLM.LOAD_MODELO_CPU ()
            yield "Modelo carregado na CPU com sucesso!"

            yield "A começar inferência..."
            AUDITORIA = AUDITORIA_SLM.INFER_CPU (contexto, prompt, TRANSCRIÇÃO)
            yield "Inferência Terminada!"

            DATABASE.ADD_DATA (audio, TRANSCRIÇÃO, AUDITORIA, MODELO)
            yield "Adicionado à Base de Dados!"

            SERVER.terminate () # Termina a linha de comando o que faz limpeza da memória