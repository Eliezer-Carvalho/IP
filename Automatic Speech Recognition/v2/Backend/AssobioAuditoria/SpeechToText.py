from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import torch
import librosa
import yaml

"""
    Esta classe serve para carregar um modelo ASR a partir de um ficheiro CONFIG.yaml
    Qualquer adição de modelos, simplesmente basta alterar o ficheiro CONDIG.yaml

    O método STT (Speech To Text) tem como principal função converter áudio para texto.
    Na primeira fase realiza Tokenização ao tensor proveniente do áudio. Após isso o Modelo ASR entra em ação usando o Encoder para converter a Tokenização em Embeddings
    e depois o Decoder converte os Embeddings em Texto usando Geração Auto Regressiva.

    Para melhor perfomance foi usado Beam Search que permite ter X opções em parelo antes de selecionar o próximo token.

    Para áudios mais longos (>30s) é fulcrar deixar truncation = False e return_timestamps = True.

    No fim é realizada uma mini normalização do output.
"""


class Speech_To_Text:

    def __init__ (self):

        self.device = "cuda" if torch.cuda.is_available () else "cpu"

        self.PROCESSOR = None
        self.MODEL_ASR = None

        with open (r"v2\Backend\AssobioAuditoria\__config__.yaml", "r", encoding = "utf-8") as f:
            self.CONFIG = yaml.safe_load (f)


    def LOAD_ASR_MODEL (self):

        if self.PROCESSOR is None:

            self.PROCESSOR = AutoProcessor.from_pretrained (self.CONFIG["WhisperPT"]["path"])
            self.MODEL_ASR = AutoModelForSpeechSeq2Seq.from_pretrained (self.CONFIG["WhisperPT"]["path"], device_map = self.device, dtype = torch.float16)


    def STT (self, audio):

        WAV = librosa.load (audio, sr = self.PROCESSOR.feature_extractor.sampling_rate, mono = True)[0] # Índice 0 porque load devolve dois valores, WAV e SAMPLE_RATE

        inputs = self.PROCESSOR (WAV, sampling_rate = self.PROCESSOR.feature_extractor.sampling_rate, return_tensors = "pt", truncation = False) # Truncation obrigatório para áudios >30s
        inputs = inputs["input_features"].to (self.device, dtype = torch.float16) # Passar para GPU

        with torch.inference_mode ():
            outputs = self.MODEL_ASR.generate (inputs, return_timestamps = True, task = "transcribe", language = "pt", num_beams = 7) # Beam Search # return_timestamps obrigatório para áudios >30s 

        trans = self.PROCESSOR.batch_decode (outputs, skip_special_tokens = True)[0]
        trans = " ".join (str(trans).split()).lower() # Mini Tratamento do output # Remoção de espaços em branco em excesso e conversão para minúsculas 

        return (trans)
