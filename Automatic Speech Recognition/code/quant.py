
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


    PROCESSADOR.save_pretrained ("")
    MODELO_SPEECH.save_pretrained ("")


except Exception as e:
    print (e)


#####Having fun

"""
import torch
import torch.nn as nn


tensor = torch.randn (4, 4) #matriz, tensor de 1 dimensão 

Q = nn.Linear (4, 2)
K = nn.Linear (4, 2)
V = nn.Linear (4, 2)

Q = Q (tensor)
K = K (tensor)
V = V (tensor)


ATTENTION = Q @ K.T

#### masked attention
#### softmax
#### + V
#### proj para multi head 



print (tensor)
print (Q)
print (K)
print (V)

print (ATTENTION)

"""