from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
from transformers import pipeline
from transformers.audio_utils import load_audio
import torch
import traceback #ERROS
from dataclasses import dataclass

from Assobio.router import Model_Routing


# https://realpython.com/python3-object-oriented-programming/
'''
Classes para objetos que mantêm estado (modelo, processador, configuração).
Funções para utilitários independentes (estatísticas da GPU, conversões, carregamento de áudio, etc.).
'''

ROUTER = Model_Routing ()


class WHISPER_AI:

    def __init__ (self): # self usado para partilhar variáveis entre classes
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        ################################
        self.PROCESSADOR_SPEECH = None
        self.MODELO_SPEECH = None
        self.SETUP = None
        ################################
        self.SLM_MODEL = None
        self.SLM_TOKENIZER = None

    def LOAD_MODEL (self): 

        try:
        
            self.PROCESSADOR_SPEECH = AutoProcessor.from_pretrained (r"C:\Users\Admin\Desktop\models\ASR Models\Whisper\WhisperLv3-PT-All 4Bit") #Tokenizer
            self.MODELO_SPEECH = AutoModelForSpeechSeq2Seq.from_pretrained (r"C:\Users\Admin\Desktop\models\ASR Models\Whisper\WhisperLv3-PT-All 4Bit", device_map = self.device)

            """
            SETUP porque para áudios mais longos, o modelo Whisper corta os áudios de em blocos de 30 segundos.
            Só com SETUP dá para acionar essa possibilidade.

            """

            self.SETUP = pipeline (
                    "automatic-speech-recognition", 
                    model = self.MODELO_SPEECH, 
                    tokenizer = self.PROCESSADOR_SPEECH.tokenizer, 
                    feature_extractor = self.PROCESSADOR_SPEECH.feature_extractor,
                    ignore_warning = True,
                    )

        except Exception:
            traceback.print_exc()




    def ASSOBIO (self, path):

        for PATH in path:
            try:

                WAV = load_audio (PATH, sampling_rate = self.PROCESSADOR_SPEECH.feature_extractor.sampling_rate)

                TRANSCRITO = self.SETUP (
                    WAV, 
                    chunk_length_s = 30,
                    generate_kwargs = {
                        "num_beams": 5
                    },
                    )
                #print (TRANSCRITO) #{'text': 'x'}
                ##################################

                ROUTING = len(TRANSCRITO["text"].split()) # Número de Palavras ou Número de Caractéres ? 
                TEXTO = str(TRANSCRITO["text"])

                print (ROUTING)
                print (TEXTO)
                torch.cuda.empty_cache ()
                

                if ROUTING > 100:
                    MODEL = ROUTER.LOAD_MODEL_GPU ()
                    print (MODEL)

                else: 
                    MODEL = ROUTER.LOAD_MODEL_CPU ()
                    print (MODEL)

                #torch.cuda.empty_cache()

            except Exception:
                traceback.print_exc()






        #print (trans)
        #return "\n\n".join (trans) # Para retornar string, em vez de lista




            

            













'''
            try:
        
                AUDIO = load_audio (PATH, sampling_rate = self.PROCESSADOR.feature_extractor.sampling_rate) 
        
                TOKENS = self.PROCESSADOR (
                    AUDIO, 
                    sampling_rate = self.PROCESSADOR.feature_extractor.sampling_rate, 
                    return_tensors = "pt",
                    generate_kwargs = {
                        "language":"portuguese",
                        "task": "transcribe"
                        },
                    ).to(self.device)
        
                TRANSCRITO = self.MODELO.generate (**TOKENS, num_beams = 5)
        
                OUTPUT = self.PROCESSADOR.decode (TRANSCRITO, skip_special_tokens = True)
        
                return OUTPUT[0]
                    
            except Exception as e:
                print (e)
'''
