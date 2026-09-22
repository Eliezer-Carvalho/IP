
import gradio as gr
import time

from .SpeechToText import Speech_To_Text #ip\Automatic Speech Recognition\v2\Backend\AssobioAuditoria\SpeechToText.py
from .Model_Routing import System_One_Model_Routing #C:\Users\Admin\Desktop\ip\Automatic Speech Recognition\v2\Backend\AssobioAuditoria\Model_Routing.py
from .AuditoriaLLM import Auditoria_LLM #ip\Automatic Speech Recognition\v2\Backend\AssobioAuditoria\AuditoriaLLM.py
from .DatabaseAssobioAuditoria.Database import SQL_Functions #ip\Automatic Speech Recognition\v2\Backend\AssobioAuditoria\DatabaseAssobioAuditoria\Database.py

AUDIO_TEXT = Speech_To_Text ()
ROUTING = System_One_Model_Routing ()
AUDITORIA = Auditoria_LLM ()
DATABASE = SQL_Functions ()


def Assobio_Auditoria (PATH, CONTEXTO, PROMPT):

    yield gr.update (visible = True)
    yield "A carregar modelos ASR"
    AUDIO_TEXT.LOAD_MODELS_STT ()
    yield "Modelos Carregados!"
    time.sleep (1.5)

    for audio in PATH:

        yield gr.update (visible = True)

        ## 1. Pré Processamento
        yield "A começar o Pré Processamento do Áudio..."
        VOZES, TEMPO_ÁUDIO, TEMPO_PRE_PROCESS, PATH_PRE_PROCESS = AUDIO_TEXT.WAV_PRE_PROCESSING (audio)
        yield "Áudio Pré Processado!"
        time.sleep (1.5)
        #----------------------------------------------------------------------------#

        ## 2. Transcrição
        yield "A começar a Transcrição do Áudio para Texto..."
        TRANS, TEMPO_PROCESSAMENTO, TEMPO_INFER, LAT, TOKENS_perS_DECODE_STT = AUDIO_TEXT.SPEECH_TO_TEXT (VOZES)
        yield "Áudio Transcrito para Texto!"
        time.sleep (1.5)
        #----------------------------------------------------------------------------#

        ## 3. Model Routing
        DECISION = ROUTING.Model_Routing (TRANS)

        if DECISION == "GPU":

            ## 3.1 Load Model
            yield "A carregar modelo na GPU..."
            RANDOM_GPU, HARDWARE = AUDITORIA.LOAD_MODELS_GPU () 
            yield "Modelo carregado na GPU com sucesso!"
            time.sleep (1.5)

            ## 3.2 Infer Model
            yield "A começar inferência..."
            RESPOSTA, TOKENS, TEMPO_PREFILL, TOKENS_perS_PREFILL, TEMPO_DECODE, TOKENS_perS_DECODE, LAT_LLM = AUDITORIA.INFER_GPU (CONTEXTO, PROMPT, TRANS)
            yield "Inferência Terminada!"
            time.sleep (1.5)

            ## 3.3 Add Data DB
            DATABASE.ADD_DATA (CONTEXTO, PROMPT, audio, PATH_PRE_PROCESS, TEMPO_ÁUDIO, TEMPO_PRE_PROCESS, TRANS, TEMPO_PROCESSAMENTO, TEMPO_INFER, LAT, TOKENS_perS_DECODE_STT, HARDWARE, RANDOM_GPU, RESPOSTA, TOKENS, TEMPO_PREFILL, TOKENS_perS_PREFILL, TEMPO_DECODE, TOKENS_perS_DECODE, LAT_LLM)
            yield "Adicionado à Base de Dados!"
            time.sleep (2)
        
        else:

            ## 3.1 Load Model
            yield "A carregar modelo na CPU..."
            RANDOM_CPU, HARDWARE = AUDITORIA.LOAD_MODELS_CPU ()
            yield "Modelo carregado na CPU com sucesso!"
            time.sleep (1.5)

            ## 3.2 Infer Model
            yield "A começar inferência..."
            RESPOSTA, TOKENS, TEMPO_PREFILL, TOKENS_perS_PREFILL, TEMPO_DECODE, TOKENS_perS_DECODE, LAT_LLM = AUDITORIA.INFER_CPU (CONTEXTO, PROMPT, TRANS)
            yield "Inferência Terminada!"
            time.sleep (1.5)

            ## 3.3 Add Data DB
            DATABASE.ADD_DATA (CONTEXTO, PROMPT, audio, PATH_PRE_PROCESS, TEMPO_ÁUDIO, TEMPO_PRE_PROCESS, TRANS, TEMPO_PROCESSAMENTO, TEMPO_INFER, LAT, TOKENS_perS_DECODE_STT, HARDWARE, RANDOM_CPU, RESPOSTA, TOKENS, TEMPO_PREFILL, TOKENS_perS_PREFILL, TEMPO_DECODE, TOKENS_perS_DECODE, LAT_LLM)
            yield "Adicionado à Base de Dados!"
            time.sleep (2)
        #----------------------------------------------------------------------------#

        time.sleep (3)
        yield gr.update (visible = False)