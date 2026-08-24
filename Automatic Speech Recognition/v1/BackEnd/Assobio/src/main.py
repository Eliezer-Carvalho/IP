import torch
import gc
from subprocess import Popen

from .Transcrição import Whisper
from .Model_Routing import Model_Routing
from .Inference import Inference
from .Database import SQL_FUNCTS

"""
Esta função junta todas as Classes criadas numa e assim no FrontEnd basta rodar esta função para o sistema funcionar como um todo.
É a melhor abordagem e por isso o nome de "main.py" porque representa a principal função do sistema.
"""

WHISPER = Whisper ()
ROUTING = Model_Routing ()
INFERENCE = Inference ()
DB = SQL_FUNCTS ()


#WHISPER.LOAD_MODEL ()


def SOURCE (path, contexto, prompt): # Aqui passo a instância já criada no Main porque essa é que dá load do Model Whisper

    WHISPER.LOAD_MODEL ()
    
    #print (path) #['C:\\Users\\Admin\\AppData\\Local\\Temp\\gradio\\9aadfa40e4809df056ab4cf553fab63b281735fb97cd3cc3af7ef48956e4b636\\audio3.wav']

    for CAMINHO in path:

        #print (CAMINHO) #C:\Users\Admin\AppData\Local\Temp\gradio\9aadfa40e4809df056ab4cf553fab63b281735fb97cd3cc3af7ef48956e4b636\audio3.wav
        
        ALPHA, TRANS = WHISPER.TRANSCRIPTION (CAMINHO)

        yield "Transcrição Concluída"

        """
        Limpeza de MEM after Transcrição
        """
        torch.cuda.empty_cache ()
        #torch.cuda.reset_max_memory_allocated ()
        gc.collect()


        if ALPHA > 100:

            SELECTED, MODEL, TOKENIZER = ROUTING.LOAD_MODEL_GPU ()

            yield f"Modelo {SELECTED} Carregado na GPU"
            yield "Realizando Inferência..."

            TEXTO = INFERENCE.INFERENCE_GPU (MODEL, TOKENIZER, contexto, prompt, TRANS)

            yield "Inferência Concluída!"

            SAVE = DB.ADD_DATA (CAMINHO, TRANS, TEXTO, SELECTED)

            yield "Guardado na Base de Dados!!"

            """
            Limpeza de MEM
            """
            del SELECTED, MODEL, TOKENIZER, TEXTO
            gc.collect ()
            torch.cuda.empty_cache ()
            

        else: 

            SELECTED, SERVER = ROUTING.LOAD_MODEL_CPU ()

            yield f"Modelo {SELECTED} Carregado na CPU"
            yield "Realizando Inferência..."

            TEXTO = INFERENCE.INFERENCE_CPU (contexto, prompt, TRANS)

            yield "Inferência Concluída!"

            SAVE = DB.ADD_DATA (CAMINHO, TRANS, TEXTO, SELECTED)

            yield "Guardado na Base de Dados!!"

            """
            Limpeza de MEM
            """
            SERVER.terminate ()
            gc.collect ()
            del SELECTED, SERVER, TEXTO


        del ALPHA, TRANS
