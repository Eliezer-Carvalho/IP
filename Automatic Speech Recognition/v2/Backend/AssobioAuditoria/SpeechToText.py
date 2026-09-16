from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import torch
import torchaudio
import librosa
import yaml
import time 
from demucs.api import Separator
import soundfile as sf
from uuid import uuid4

"""
Esta classe é a PRIMEIRA classe da aba Assobio - Auditoria do sistema Assobio.
Tem como principal objetivo carregar os modelos, realizar pré processamento do áudio e realizar a transcrição dos áudios usando modelos de Automatic Speech Recognition.

View Geral:
                                        LOAD_MODEL_STT --> WAV_PRE_PROCESSING --> SPEECH_TO_TEXT

É usado um ficheiro .YAML como config file do modelo ASR, assim se for preciso adicionar ou remover modelos é mais prático e não há necessidade de mexer em código.
C:/Users/Admin/Desktop/ip/Automatic Speech Recognition/v2/Backend/AssobioAuditoria/__config__.yaml
"""

class Speech_To_Text:

    def __init__ (self):

        """
        Método construtor, inicia variáveis importantes.
        """

        self.device = "cuda" if torch.cuda.is_available () else "cpu"

        self.PROCESSOR_ASR = None
        self.MODEL_ASR = None
        self.DEMUCS_SEPARATOR = None

        with open (r"v2\Backend\AssobioAuditoria\__config__.yaml", "r", encoding = "utf-8") as f:
            self.CONFIG = yaml.safe_load (f)


    def LOAD_MODELS_STT (self):

        """
        Load dos modelos importantes para realizar Speech To Text, neste caso representa o load do modelo Whisper e Separator.
        """

        if self.PROCESSOR_ASR is None:

            self.PROCESSOR_ASR = AutoProcessor.from_pretrained (self.CONFIG["WhisperLarge"]["path"])
            self.MODEL_ASR = AutoModelForSpeechSeq2Seq.from_pretrained (self.CONFIG["WhisperLarge"]["path"], device_map = self.device, dtype = torch.float16)
            self.DEMUCS_SEPARATOR = Separator (model = "htdemucs")


    def WAV_PRE_PROCESSING (self, path_wav):

        """
        Este método representa a camada de pré processamento adotada na versão 2 do sistema Assobio.
        Para mais info: 
        https://github.com/Eliezer-Carvalho/IP/blob/master/Automatic%20Speech%20Recognition/Automatic%20Speech%20Recognition.pdf
        https://github.com/Eliezer-Carvalho/IP/tree/master/Automatic%20Speech%20Recognition/v2/Eval
        """

        pre_process_begin = time.time ()

        #O modelo Separator do Demucs recebe como input áudio estéreo com sample rate a 44.1kHz
        #e o TDS em formato PyTorch
        WAV, SR = librosa.load (path_wav, sr = 44100, mono = False)
        WAV = torch.from_numpy (WAV)

        #Camada de proteção caso o áudio continue em formato Mono. #Aconteceu várias vezes na
        #fase de Eval
        if len (WAV.shape) == 1:
            WAV = WAV.unsqueeze (0) #https://stackoverflow.com/questions/57237352/what-does-unsqueeze-do-in-pytorch
            WAV = WAV.repeat (2, 1) #https://docs.pytorch.org/docs/2.14/generated/torch.Tensor.repeat.html
 
        #Primeira fase de Peak Normalization
        #torch.max -> valor máximo do array | torch.abs -> apenas valores absolutos ou seja > 0
        WAV = WAV / torch.max (torch.abs (WAV))

        #Demucs Separator
        # https://github.com/facebookresearch/demucs
        ORIGINAL, SEPARADO = self.DEMUCS_SEPARATOR.separate_tensor (WAV, sr = SR)

        #Queremos apenas ficar com as vozes
        VOZES = SEPARADO ["vocals"]
        #Conversão para 16kHz, que é o Sample Rate que os modelos ASR aceitam
        VOZES = torchaudio.functional.resample (VOZES, orig_freq = SR, new_freq = 16000)
        #Conversão para mono, modelos ASR também só aceitam áudio mono
        VOZES = VOZES.mean (dim = 0) #Isto faz todo o sentido porque um áudio estéreo é um áudio com dois canais, e mono ao contrário

        #Segunda fase de Peak Normalization
        VOZES = VOZES / torch.max (torch.abs (VOZES))

        #Aumento do Volume, uso da fórmula do Ganho
        #20 log10 (Aout / Ain)
        GANHO_DB = 6
        GANHO = 10 ** (GANHO_DB / 20)
        VOZES = VOZES * GANHO

        ##Guardar o áudio pré processado para depois guardar na Database
        PATH = rf"C:\Users\Admin\Desktop\ip\Automatic Speech Recognition\v2\Backend\AssobioAuditoria\DatabaseAssobioAuditoria\audios_pre_process\{uuid4().hex}.wav"
        sf.write (PATH, VOZES, samplerate = 16000)

        TEMPO_PRE_PROCESS = time.time () - pre_process_begin
        #Fórmula = num_samples / sample_rate em hz
        TEMPO_ÁUDIO = len (VOZES) / 16000

        return (VOZES, TEMPO_ÁUDIO, TEMPO_PRE_PROCESS, PATH)


    def SPEECH_TO_TEXT (self, AUDIO_POST_PROCESS):

        """
        Este método recebe o áudio após o Pré Processamento e utiliza um modelo ASR
        para converter o áudio para texto.
        """

        torch.cuda.synchronize ()
        begin_process = time.time ()

        #Nesta primeira fase o áudio no processador do modelo ASR.
        #O processador converte o mesmo para tokens e após o processamento
        #converte para embeddings. Aqui até parece que podíamos usar Prefill e Decode mas o Prefill aqui acaba por ser diferente.
        #Por esse motivo dei o nome de tempo de processamento.
        inputs = self.PROCESSOR_ASR (AUDIO_POST_PROCESS, sampling_rate = self.PROCESSOR_ASR.feature_extractor.sampling_rate, return_tensors = "pt", truncation = False) # Truncation obrigatório para áudios >30s
        inputs = inputs["input_features"].to (self.device, dtype = torch.float16) # Passar para GPU

        torch.cuda.synchronize ()
        TEMPO_PROCESSAMENTO = time.time () - begin_process 

        #----------------------------------------------------------------------------------#

        torch.cuda.synchronize ()
        begin_infer = time.time ()

        #Aqui os embeddings entram no decoder do modelo ASR que vai converter os embeddings para tokens de output.
        with torch.inference_mode ():
            outputs = self.MODEL_ASR.generate (inputs, return_timestamps = True, task = "transcribe", language = "pt", num_beams = 5) # Beam Search # return_timestamps obrigatório para áudios >30s 

        #print (outputs)
        #print (len (outputs))
        #print (outputs.shape)
        #print (outputs[0])
        #print (len(outputs[0]))
        
        torch.cuda.synchronize ()
        TEMPO_INFER = time.time () - begin_infer

        LAT = TEMPO_PROCESSAMENTO + TEMPO_INFER
        TOKENS_perS_DECODE = len (outputs[0]) / TEMPO_INFER  

        TRANS = self.PROCESSOR_ASR.batch_decode (outputs, skip_special_tokens = True)[0] 

        return (TRANS, TEMPO_PROCESSAMENTO, TEMPO_INFER, LAT, TOKENS_perS_DECODE)
