from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
import librosa
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
    

    def LOAD_MODEL (self): 

        if self.PROCESSADOR_SPEECH is None: # Excelente condição para melhorar memória management, se o modelo já estiver loaded, salta

            try:
            
                self.PROCESSADOR_SPEECH = AutoProcessor.from_pretrained (r"C:\Users\Admin\Desktop\models\ASR Models\Whisper\WhisperLv3-PT-All 8Bit") #Tokenizer
                self.MODELO_SPEECH = AutoModelForSpeechSeq2Seq.from_pretrained (r"C:\Users\Admin\Desktop\models\ASR Models\Whisper\WhisperLv3-PT-All 4Bit", device_map = self.device, dtype = torch.float16)

            except Exception as e:
                traceback.print_exc()



    def TRANSCRIPTION (self, path):

            #yield f"Áudio Número {idx}" #yield é como um return mas que não termina a função. GOAT Stuff

        try:

            WAV, SAMPLE_RATE = librosa.load (path, sr = 16000, mono = True)

            """ Prefill 
            NOVA VERSÃO - Mais controlo do sistema, e aplicação de Truncation para áudios > 30s.
            """
            inputs = self.PROCESSADOR_SPEECH (WAV, sampling_rate = self.PROCESSADOR_SPEECH.feature_extractor.sampling_rate, return_tensors = "pt", truncation = False)

            inputs = inputs["input_features"].to (self.device, dtype = torch.float16)


            """ Inferência 
            NOVA VERSÃO - Mais controlo sobre a inferência, uso de Beam Decoding para remover Greedy Decoding.
            #https://huggingface.co/blog/mlabonne/decoding-strategies
            """

            outputs = self.MODELO_SPEECH.generate (inputs, return_timestamps = True, task = "transcribe", language = "pt") #beams, número de opções que o modelo tem para selecionar

            TRANSCRITO = self.PROCESSADOR_SPEECH.batch_decode (outputs, skip_special_tokens = True)[0]

            #yield f"Áudio Número {idx} Transcrito"
            #print (TRANSCRITO) #{'text': 'x'}
            ##################################

            ROUTING = len(TRANSCRITO.split()) # Número de Palavras ou Número de Caractéres ? 
            TEXTO = TRANSCRITO
            #print (ROUTING)
            #print (TEXTO)

            #torch.cuda.empty_cache ()

            print (ROUTING, TEXTO)
            return ROUTING, TEXTO

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
