
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq, BitsAndBytes


MODELO_NAME = "inesc-id/WhisperLv3-PT-All"

quantization = BitsAndBytesConfig (
    load_in_4bit = True,  #Quantização
    bnb_4bit_quant_type = 'nf4',  #Tipo de Quantização
    bnb_4bit_use_double_quant = True, #Double Quantization
    bnb_4bit_compute_dtype = 'float16', #Tipo de precisão usada nos cálculos durante a inferência.
)

try:
    PROCESSADOR = AutoProcessor.from_pretrained (MODELO_NAME) #Tokenizer Wanna Be
    MODELO_SPEECH = AutoModelForSpeechSeq2Seq.from_pretrained (MODELO_NAME, device_map = device, quantization_config = quantization)


    PROCESSADOR.save_pretrained (r"C:\Users\Admin\Desktop\models\SPEECH AI\SpeechAI")
    MODELO_SPEECH.save_pretrained (r"C:\Users\Admin\Desktop\models\SPEECH AI\SpeechAI")


except Exception as e:
    print (e)
