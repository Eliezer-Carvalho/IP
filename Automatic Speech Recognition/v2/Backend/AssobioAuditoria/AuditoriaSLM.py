from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time
import yaml
import random
from subprocess import Popen #https://coderivers.org/blog/python-popen-subprocess/
from openai import OpenAI


class AuditoriaSLM:

    def __init__ (self):

        self.TOKENIZER = None
        self.MODELO = None

        self.device = "cuda" if torch.cuda.is_available () else "cpu"

        self.API = OpenAI (base_url = "http://127.0.0.1:8080", api_key = "IP")

        with open (r"v2\Backend\Assobio - Auditoria\__config__.yaml", "r", encoding = "utf-8") as f:
            self.CONFIG = yaml.safe_load (f)

    def LOAD_MODELO_GPU (self):

        MODELO_SELECIONADO = random.choice (list(self.CONFIG["SLM_GPU"].keys()))

        self.TOKENIZER = AutoTokenizer.from_pretrained (self.CONFIG["SLM_GPU"][MODELO_SELECIONADO]["path"])
        self.MODELO = AutoModelForCausalLM.from_pretrained (self.CONFIG["SLM_GPU"][MODELO_SELECIONADO]["path"], device_map = self.device, dtype = torch.float16)

        return MODELO_SELECIONADO

    def INFER_GPU (self, contexto, prompt, transcrição):

        mensagens = [
            {"role": "system", "content": contexto},
            {"role": "user", "content": f"{prompt}\n Transcrição: {transcrição}"}
        ]

        tokens = self.TOKENIZER.apply_chat_template (mensagens, tokenize = True, add_generation_prompt = True, return_tensors = "pt").to(self.device)

        with torch.inference_mode():
            logits = self.MODELO.generate (**tokens, max_new_tokens = 640)

        """
        Aqui temos de ter atenção porque os logits retornam o prompt mais a resposta.
        Por tal razão temos de indexar.
        """
        return self.TOKENIZER.decode (logits[0][tokens["input_ids"].shape[1]:], skip_special_tokens = True)

        """
        ############################################ ############################################ ############################################ ############################################ 
        ############################################ ############################################ ############################################ ############################################
        ############################################ ############################################ ############################################ ############################################
        """
    
    def LOAD_MODELO_CPU (self):

        MODELO_SELECIONADO = random.choice (list(self.CONFIG["SLM_CPU"].keys()))

        ##https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
        SERVER = Popen ([
                r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\ggml.llamacpp_Microsoft.Winget.Source_8wekyb3d8bbwe\llama-server.exe",
                "-m", self.CONFIG_CPU["SLM_CPU"][MODELO_SELECIONADO]["path"],
                "-ngl", "0",
                "--no-jinja",
                "--no-webui",            
        ])

        return MODELO_SELECIONADO, SERVER
    """
    Este método é especial porque usamos o motor de inferência Llama.cpp para rodar modelos mais pequenos na CPU.
    Desta maneira, realizamos Routing tanto de modelos como também de Hardware
    """
    def INFER_CPU (self, contexto, prompt, transcrição):

        mensagens = [
            {"role": "system", "content": contexto},
            {"role": "user", "content": f"{prompt}\n Transcrição: {transcrição}"}
        ]


        time.sleep (1) #time.sleep para dar delay no código, estava-me a dar alguns erros ao carregar tudo muito rápido

        output = self.API.chat.completions.create (
            model = "x",
            messages = mensagens,
            max_tokens = 640
        )

        #print (output)

        return output.choices[0].message.content


"""
with open (r"v2\Backend\Assobio - Auditoria\__config__.yaml", "r", encoding = "utf-8") as f:
    CONFIG = yaml.safe_load (f)

print (CONFIG)
print (CONFIG.keys())
print (CONFIG["SLM_GPU"].keys())
"""