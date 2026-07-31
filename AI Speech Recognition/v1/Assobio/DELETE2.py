import subprocess

'''
server = Popen ([
])
time.sleep (10)
server.terminate()
'''


from transformers import AutoModelForCausalLM, AutoTokenizer
from subprocess import Popen
import time

'''
MODEL_NAME = "microsoft/Phi-3.5-mini-instruct"

MODELO = AutoModelForCausalLM.from_pretrained (MODEL_NAME)
TOKENIZER = AutoTokenizer.from_pretrained (MODEL_NAME)

MODELO.save_pretrained ()
TOKENIZER.save_pretrained ()

'''
'''
hf_gguf = Popen ([
    
])

hf_gguf.wait()
hf_gguf.terminate()
'''

gguf_q4 = Popen ([
    r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\ggml.llamacpp_Microsoft.Winget.Source_8wekyb3d8bbwe\llama-quantize.exe",
    r"C:\Users\Admin\Desktop\models\Language Models\x\Microsoft Phi 3.5.gguf",
    r"C:\Users\Admin\Desktop\models\Language Models\xxx\Microsoft Phi 3.5 Q4.0.gguf",
    "Q4_K_S"
])

gguf_q4.wait()
gguf_q4.terminate()