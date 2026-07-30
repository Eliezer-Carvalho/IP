from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
from transformers.audio_utils import load_audio
import torch


'''
Classes para objetos que mantêm estado (modelo, processador, configuração).
Funções para utilitários independentes (estatísticas da GPU, conversões, carregamento de áudio, etc.).
'''

class WHISPER_AI:

    def __init__ (self): # self usado para partilhar variáveis entre classes
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.PROCESSADOR = None
        self.MODELO = None


    def LOAD_MODEL (self): 

        try:
        
            self.PROCESSADOR = AutoProcessor.from_pretrained (r"C:\Users\Admin\Desktop\models\SPEECH AI\SpeechAI-8Bit") #Tokenizer
            self.MODELO = AutoModelForSpeechSeq2Seq.from_pretrained (r"C:\Users\Admin\Desktop\models\SPEECH AI\SpeechAI-8Bit", device_map = self.device)
        
        except Exception as e:
            print (e)


    def INFERENCE (self, wav):

        for PATH in wav:
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
        