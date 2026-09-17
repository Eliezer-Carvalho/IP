import yaml
import random
from subprocess import Popen #https://coderivers.org/blog/python-popen-subprocess/
from openai import OpenAI
import requests
import time

"""
Esta classe é a SEGUNDA classe da aba Assobio - Auditoria do sistema Assobio.
Tem como principal objetivo carregar Large Language Models tanto em CPU ou GPU. O sistema tem um Model Routing
que permite ao mesmo realizar auditoria tanto com modelos carregados na CPU ou na GPU.

O motor de inferência selecionado para realizar a Auditoria é o llama.cpp. Para CPU é o ideal e para GPU não é
o mais indicado mas tem sempre melhor perfomance que raw Transformers Inferência.

Os modelos disponíveis estão no ficheiro config YAML.
C:/Users/Admin/Desktop/ip/Automatic Speech Recognition/v2/Backend/AssobioAuditoria/__config__.yaml

View Geral:
                            LOAD_MODELO_GPU --> INFER_GPU      
                            LOAD_MODELO_CPU --> INFER_CPU
"""

class Auditoria_LLM:

    def __init__ (self):

        """
        Método construtor, inicia variáveis importantes.
        """

        self.GPU = None #Variáveis que vão carregar os subprocessos
        self.CPU = None #Variáveis que vão carregar os subprocessos
        self.API = OpenAI (base_url = "http://127.0.0.1:8080", api_key = "IP")

        with open (r"v2\Backend\AssobioAuditoria\__config__.yaml", "r", encoding = "utf-8") as f:
            self.CONFIG = yaml.safe_load (f)

        with open (r"C:\Users\Admin\Desktop\ip\Automatic Speech Recognition\v2\Backend\AssobioAuditoria\SYSTEM_PROMPT.md", "r", encoding = "utf-8") as f:
            self.SYSTEM_PROMPT = f.read ()


    def LOAD_MODELS_GPU (self):

        """
        Após o Model Routing, chama-se uma classe que carregua o modelo na GPU.
        Neste caso em específico, há vários modelos que podem ser carregados.
        Assim sendo, há um random que decide qual modelo rodar.
        """

        HARDWARE = "NVIDIA RTX A4000"
        RANDOM_GPU = random.choice (list(self.CONFIG["GPU_CONFIG"]["llama.cpp"].keys()))

        #Usando a library subprocess podemos rodar comandos do cmd.
        self.GPU = Popen ([            
            r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\ggml.llamacpp_Microsoft.Winget.Source_8wekyb3d8bbwe\llama-server.exe",
            "-m", self.CONFIG["GPU_CONFIG"]["llama.cpp"][RANDOM_GPU]["path"],
            "-c", "2048",
            "-ngl", "all",
            "--reasoning", "off",

            "--host", "127.0.0.1",
            "--port", "8080",

            "--no-webui",
        ])

        #MUITO IMPORTANTE! #Muita Atenção com loops while, facilmente podem entrar num loop infinito
        #Podemos rodar comandos do cmd mas os comandos não rodam de maneira instantânea.
        #Precisamos de um mecanismo que confirme que o modelo já está a escutar na porta.
        time.sleep (3)
        while True:

            request = requests.get ("http://127.0.0.1:8080/health", timeout = 2)
            estado = request.status_code #503 - loading | 200 - loaded

            if estado == 200:
                break

            if estado == 503:
                continue

            else:
                print ("Erro na Porta GPU!")
                break
                
        return RANDOM_GPU, HARDWARE


    def INFER_GPU (self, CONTEXTO, PROMPT, TRANSCRIÇÃO):

        """
        Após o carregamento do modelo, temos que realizar a inferência.
        No fim retornamos informações importantes que vão para a Database.
        """

        MENSAGENS = [
            {"role": "system", "content": f"{self.SYSTEM_PROMPT}\n" f"{CONTEXTO}\n" f"{TRANSCRIÇÃO}\n"},
            {"role": "user", "content": f"{PROMPT}"}
        ]

        print (MENSAGENS)
        
        try:

            OUTPUT = self.API.chat.completions.create (model = "None", messages = MENSAGENS)

            RESPOSTA = OUTPUT.choices[0].message.content
            TOKENS = OUTPUT.usage.total_tokens

            ##Prefil Stats
            TEMPO_PREFILL = OUTPUT.timings["prompt_ms"] / 1000
            TOKENS_perS_PREFILL = OUTPUT.timings["prompt_per_second"] 

            ##Decode Stats
            TEMPO_DECODE = OUTPUT.timings["predicted_ms"] / 1000
            TOKENS_perS_DECODE = OUTPUT.timings["predicted_per_second"] 

            ##Latência Total
            LAT = TEMPO_PREFILL + TEMPO_DECODE

            return RESPOSTA, TOKENS, TEMPO_PREFILL, TOKENS_perS_PREFILL, TEMPO_DECODE, TOKENS_perS_DECODE, LAT

        finally:

            self.GPU.kill ()
            self.GPU = None

        
    """
    ########################################################################################################################################################################################################################
    ########################################################################################################################################################################################################################
    ########################################################################################################################################################################################################################
    ########################################################################################################################################################################################################################
    ########################################################################################################################################################################################################################
    ########################################################################################################################################################################################################################
    ########################################################################################################################################################################################################################
    """

    def LOAD_MODELS_CPU (self):

        """
        Após o Model Routing, chama-se uma classe que carregua o modelo na CPU.
        Neste caso em específico, há vários modelos que podem ser carregados.
        Assim sendo, há um random que decide qual modelo rodar.
        """

        HARDWARE = "Intel(R) Xeon(R) W-2255 CPU @ 3.70GHz"
        RANDOM_CPU = random.choice (list(self.CONFIG["CPU_CONFIG"].keys()))

        #Usando a library subprocess podemos rodar comandos do cmd.
        self.CPU = Popen ([            
            r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\ggml.llamacpp_Microsoft.Winget.Source_8wekyb3d8bbwe\llama-server.exe",
            "-m", self.CONFIG["CPU_CONFIG"][RANDOM_CPU]["path"],
            "-c", "2048",
            "-ngl", "0",
            "--reasoning", "off",

            "--host", "127.0.0.1",
            "--port", "8080",

            "--no-webui",
        ])

        #MUITO IMPORTANTE! 
        #Podemos rodar comandos do cmd mas os comandos não rodam de maneira instantânea.
        #Precisamos de um mecanismo que confirme que o modelo já está a escutar na porta. 
        time.sleep (3)
        while True:

            request = requests.get ("http://127.0.0.1:8080/health", timeout = 2)
            estado = request.status_code #503 - loading | 200 - loaded

            if estado == 200:
                break

            if estado == 503: 
                continue

            else:
                print ("Erro na Porta CPU!")
                break

        return RANDOM_CPU, HARDWARE


    def INFER_CPU (self, CONTEXTO, PROMPT, TRANSCRIÇÃO):
    
        """
        Após o carregamento do modelo, temos que realizar a inferência.
        No fim retornamos informações importantes que vão para a Database.
        """
    
        MENSAGENS = [
            {"role": "system", "content": f"{self.SYSTEM_PROMPT}\n" f"{CONTEXTO}\n" f"{TRANSCRIÇÃO}\n"},
            {"role": "user", "content": f"{PROMPT}"}
        ]

        print (MENSAGENS)

        try: 
    
            OUTPUT = self.API.chat.completions.create (model = "None", messages = MENSAGENS)
        
            RESPOSTA = OUTPUT.choices[0].message.content
            TOKENS = OUTPUT.usage.total_tokens
        
            ##Prefil Stats
            TEMPO_PREFILL = OUTPUT.timings["prompt_ms"] / 1000
            TOKENS_perS_PREFILL = OUTPUT.timings["prompt_per_second"]
        
            ##Decode Stats 
            TEMPO_DECODE = OUTPUT.timings["predicted_ms"] / 1000
            TOKENS_perS_DECODE = OUTPUT.timings["predicted_per_second"]
        
            ##Latência Total
            LAT = TEMPO_PREFILL + TEMPO_DECODE

            return RESPOSTA, TOKENS, TEMPO_PREFILL, TOKENS_perS_PREFILL, TEMPO_DECODE, TOKENS_perS_DECODE, LAT
    
        finally:

            self.CPU.kill ()
            self.CPU = None
    
        


























