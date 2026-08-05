from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
from transformers import pipeline
from transformers.audio_utils import load_audio
import torch
import traceback #ERROS

# https://realpython.com/python3-object-oriented-programming/
'''
Classes para objetos que mantêm estado (modelo, processador, configuração).
Funções para utilitários independentes (estatísticas da GPU, conversões, carregamento de áudio, etc.).
'''

"""
Esta classe é encarregada por carregar o modelo Whisper (inesc-id/WhisperLv3-PT-All | https://huggingface.co/inesc-id/WhisperLv3-PT-All/tree/main) na meória GPU.
Também serve para realizar a Transcrição de Áudio.
"""

class Whisper:

    def __init__ (self): # self usado para partilhar variáveis entre classes
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        ################################
        self.PROCESSADOR_SPEECH = None
        self.MODELO_SPEECH = None
        self.SETUP = None


    def LOAD_MODEL (self): 

        if self.PROCESSADOR_SPEECH is None: # Excelente condição para melhorar memória management, se o modelo já estiver loaded, salta

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


            except Exception as e:
                traceback.print_exc()



    def TRANSCRIPTION (self, path):

            #yield f"Áudio Número {idx}" #yield é como um return mas que não termina a função. GOAT Stuff

        try:

            WAV = load_audio (path, sampling_rate = 16000)

            TRANSCRITO = self.SETUP (
                WAV, 
                chunk_length_s = 30,
                generate_kwargs = {
                    "num_beams": 5
                },
                )

            #yield f"Áudio Número {idx} Transcrito"
            #print (TRANSCRITO) #{'text': 'x'}
            ##################################

            ROUTING = len(TRANSCRITO["text"].split()) # Número de Palavras ou Número de Caractéres ? 
            TEXTO = str(TRANSCRITO["text"])
            #print (ROUTING)
            #print (TEXTO)

            #torch.cuda.empty_cache ()

            return (ROUTING, TEXTO)

        except Exception as e:
            traceback.print_exc()

            



############################################################ CÓDIGO ANTIGO


"""
    def MODEL_ROUTING_LOADING (self):
            
            if self.ROUTING > 100:
                self.MODEL_NAME, self.MODELO, self.TOKENIZER = ROUTER.LOAD_MODEL_GPU ()
                yield f"Modelo Atríbuido: {MODEL_NAME}"

            else: 
                MODEL_NAME = ROUTER.LOAD_MODEL_CPU ()
                yield f"Modelo Atríbuido: {self.MODEL_NAME}"

                #torch.cuda.empty_cache()


    def INFER (self):

    
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
"""
