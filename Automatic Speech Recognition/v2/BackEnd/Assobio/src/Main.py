from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
from transformers.audio_utils import load_audio

from transformers import AutoModelForCausalLM, AutoTokenizer

from transformers import TextStreamer

import torch
import traceback




class Whisper:

    def __init__ (self):

        self.device = "cuda" if torch.cuda.is_available () else "cpu"
        self.MODEL = None
        self.PROCESSOR = None
        self.TRANS = []


        self.MODELO = None
        self.TOKENIZER = None

    def LOAD_MODEL_WHISPER (self):


        try:
            self.MODEL = AutoModelForSpeechSeq2Seq.from_pretrained (r"C:\Users\Admin\Desktop\models\ASR Models\Whisper\WhisperLv3-PT-All 8Bit", device_map = self.device, dtype = torch.float16)
            self.PROCESSOR = AutoProcessor.from_pretrained (r"C:\Users\Admin\Desktop\models\ASR Models\Whisper\WhisperLv3-PT-All 8Bit")


        except Exception as e:

            traceback.print_exc ()


    def WHISPER_TRANSCRIPTION (self, path):

        try:

            for audio in path:

                WAV = load_audio (audio, sampling_rate = self.PROCESSOR.feature_extractor.sampling_rate)

                inputs = self.PROCESSOR (WAV, sampling_rate = self.PROCESSOR.feature_extractor.sampling_rate, return_tensors = "pt", truncation = False)
                inputs = inputs["input_features"].to (self.device, dtype = torch.float16)

                outputs = self.MODEL.generate (inputs, return_timestamps = True, task = "transcribe", language = "pt", num_beams = 5)

                TRANSCRITO = self.PROCESSOR.decode (outputs)

                self.TRANS.append (str(TRANSCRITO))

            print (self.TRANS)
            return self.TRANS

        except Exception as e:
            traceback.print_exc ()


    def LOAD_MODEL_SLM (self):

        self.MODELO = AutoModelForCausalLM.from_pretrained (r"C:\Users\Admin\Desktop\models\Language Models\Mistral 7B Q4", device_map = self.device)
        self.TOKENIZER = AutoTokenizer.from_pretrained (r"C:\Users\Admin\Desktop\models\Language Models\Mistral 7B Q4")


    def INFERENCE (self, prompt, history):

        mensagens = [
            {"role": "system", "content": "És um modelo inserido num sistema de conversas sobre Transcrição de áudio em Português Europeu. Vais receber Transcrições de Áudio e deves ter a capacidade de falar sobre as mesmas."},
            {"role": "user", "content": f"{prompt}\n Transcrição: {self.TRANS}"}
        ]

        tokens = self.TOKENIZER.apply_chat_template (mensagens, tokenize = True, add_generation_prompt = True, return_tensors = "pt").to(self.device)
        
        with torch.inference_mode ():
            logits = self.MODELO.generate (**tokens, max_new_tokens = 500) #com return_tensors = "pt" não é preciso

        #return logits
        return self.TOKENIZER.decode (logits[0][tokens["input_ids"].shape[1]:], skip_special_tokens = True)
