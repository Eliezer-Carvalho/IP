from transformers import WhisperProcessor, WhisperForConditionalGeneration #https://huggingface.co/docs/transformers/v5.14.0/en/model_doc/whisper#whisper

import librosa

MODELO_NOME = "openai/whisper-medium"

PROCESSADOR = WhisperProcessor.from_pretrained (MODELO_NOME)
MODELO = WhisperForConditionalGeneration.from_pretrained (MODELO_NOME)


def MAIN (path):
    
    audio, sr = librosa.load (path, sr = 16000)

    inputs = PROCESSADOR (audio, sampling_rate = 16000, return_tensors = "pt")

    predicted_ids = MODELO.generate(inputs.input_features, language = "portuguese", task = "transcribe", num_beams = 2)

    text = PROCESSADOR.batch_decode(predicted_ids, skip_special_tokens = True)

    return (text[0])