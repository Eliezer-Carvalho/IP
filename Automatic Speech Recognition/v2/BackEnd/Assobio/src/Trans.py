from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
from transformers.audio_utils import load_audio

import torch
import traceback




class Whisper:

    def __init__ (self):

        self.device = "cuda" if torch.cuda.is_available () else "cpu"
        self.MODEL = None
        self.PROCESSOR = None


    def LOAD_MODEL (self):


        try:
            self.MODEL = AutoModelForSpeechSeq2Seq.from_pretrained (r"C:\Users\Admin\Desktop\models\ASR Models\Whisper\WhisperLv3-PT-All 8Bit", device_map = self.device, dtype = torch.float16)
            self.PROCESSOR = AutoProcessor.from_pretrained (r"C:\Users\Admin\Desktop\models\ASR Models\Whisper\WhisperLv3-PT-All 8Bit")


        except Exception as e:

            traceback.print_exc ()


    def WHISPER_TRANSCRIPTION (self, path):

        try:

            TRANS = []

            for audio in path:

                WAV = load_audio (audio, sampling_rate = self.PROCESSOR.feature_extractor.sampling_rate)

                inputs = self.PROCESSOR (WAV, sampling_rate = self.PROCESSOR.feature_extractor.sampling_rate, return_tensors = "pt", truncation = False)
                inputs = inputs["input_features"].to (self.device, dtype = torch.float16)

                outputs = self.MODEL.generate (inputs, return_timestamps = True, task = "transcribe", language = "pt", num_beams = 8)

                TRANSCRITO = self.PROCESSOR.decode (outputs)

                TRANS.append (str(TRANSCRITO))

            print (TRANS)
            return TRANS

        except Exception as e:
            traceback.print_exc ()