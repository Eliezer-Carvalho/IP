from subprocess import Popen
import subprocess
from openai import OpenAI
import yaml
import time
import requests
import gradio as gr


from .mainSMLayer import RUN_SEMANTIC_LAYER


"""
Esta classe é a primeira classe do sistema Assobio - Chat.
Tem como principal objetivo rodar um modelo com o motor de inferência vLLM, reencaminhar mensagens para o modelo e retornar as respostas para o GUI.
"""

class LargeLanguageModelvLLM:

    def __init__ (self):

        """
        Métodos construtores iniciais da classe
        """

        self.vLLM_MODEL = None
        self.API = OpenAI (base_url = "http://127.0.0.1:8000/v1", api_key = "IP")

        with open (r"v2\Backend\AssobioAuditoria\__config__.yaml", "r", encoding = "utf-8") as f:
            self.CONFIG = yaml.safe_load (f)

        with open (r"C:\Users\Admin\Desktop\ip\Automatic Speech Recognition\v2\Backend\AssobioChat\SystemPrompts\SYSTEM_PROMPT.md", "r", encoding = "utf-8") as f:
            self.SYSTEM_PROMPT = f.read ()

        with open (r"C:\Users\Admin\Desktop\ip\Automatic Speech Recognition\v2\Backend\AssobioChat\SystemPrompts\CHAT_SYSTEM_PROMPT_SEMANTIC.md", "r", encoding = "utf-8") as f:
            self.SYSTEM_PROMPT_SMLayer = f.read ()

    def LOAD_MODEL_GPU_vLLM_DOCKER (self):

        """
        Este método é especial. 
        Como vamos usar vLLM como motor de inferência, precisamos de usar Docker para hospedar o modelo.
        Para tal temos que garantir que o Docker está iniciado e que o Container está a correr.
        """
        yield gr.update (visible = True) 

        #Primeira confirmação do estado do Docker, para perceber se já está aberto ou não.
        yield "A confirmar o estado do Docker.."
        DOCKER_STATE = subprocess.run (["docker", "info"], capture_output = True, text = True)
        DOCKER_STATE = DOCKER_STATE.returncode #1 ou 0

        #Se não tiver aberto o Docker, abre.
        if DOCKER_STATE == 1:
            Popen ([r"C:\Users\Admin\AppData\Local\Programs\DockerDesktop\Docker Desktop.exe"]) #Caminho do .exe

        #Podes abrir a aplicação mas o motor do Docker, o Daemon, pode ainda não estar inicializado e por isso vamos pingando o docker info até receber a resposta pretendida.
        while True:

            CHECK_DOCKER_STATE = subprocess.run (["docker", "info"], capture_output = True, text = True)
            CHECK_DOCKER_STATE = CHECK_DOCKER_STATE.returncode

            if CHECK_DOCKER_STATE == 1:
                continue

            else:
                time.sleep (1)
                break #Docker Available
        yield "Docker aberto!"
        time.sleep (1.5)

        #!!MUITO IMPORTANTE!!
        #Estando com o Docker aberto e com o Daemon arrancado, temos que correr o Container que contém a imagem do vLLM e as configs da run do modelo selecionado.
        yield "A iniciar o Container..."
        DOCKER_CONTAINER_vLLM_MODEL_RUN = subprocess.run (["docker", "start", f"{self.CONFIG['GPU_CONFIG']['vLLM']['Microsoft Phi 15B GPTQ Q4']['container']}"], capture_output = True, text = True)
        DOCKER_CONTAINER_vLLM_MODEL_RUN = DOCKER_CONTAINER_vLLM_MODEL_RUN.returncode

        if DOCKER_CONTAINER_vLLM_MODEL_RUN == 0:
            pass

        elif DOCKER_CONTAINER_vLLM_MODEL_RUN != 0:
            print ("Erro na Inicialização do Container do Docker")
        yield "Container a correr!"
        time.sleep (1.5)
        #---------------------- ------------------------------------------------------------------------------------------------------------------------------------#
        
        #!!MUITO IMPORTANTE!!
        #Tal como o llama.cpp, o vLLM abre uma porta do computador que permite a comunicação entre a OpenAI SDK e o modelo, como o Container demora algum tempo a arrancar, vamos
        #pingando a porta até receber uma resposta positiva 
        yield "A estabelecer comunicação com a porta..."
        while True:

            try:
                vLLM_RESPOSTA = requests.get ("http://127.0.0.1:8000/health", timeout = 2)
                vLLM_RESPOSTA = vLLM_RESPOSTA.status_code

                if vLLM_RESPOSTA == 200:
                    break
                    
                    
                elif vLLM_RESPOSTA == 503:
                    continue

            except requests.exceptions.RequestException:
                continue
                print ("Erro na comunicação com a porta do Docker")

        yield "Comunicação estabelecida!"
        time.sleep (5)
        yield gr.update (visible = False)
        #No fim deste método, temos o modelo selecionado a correr num Container Docker com uma imagem vLLM!

    def INFER_GPU_vLLM_DOCKER (self, PROMPT, HISTÓRICO, ESTADO_SMLayer):

        if ESTADO_SMLayer == True:

            OUTPUT_SEMANTIC_LAYER = RUN_SEMANTIC_LAYER (PROMPT)

            #print ("\n\n\n\n\n\n\n", OUTPUT_SEMANTIC_LAYER)

            MENSAGENS = [
                {"role": "system", "content": f"{self.SYSTEM_PROMPT_SMLayer}" f"{OUTPUT_SEMANTIC_LAYER}"}
            ]
                    
            if HISTÓRICO:
                MENSAGENS.extend (HISTÓRICO)
                        
            MENSAGENS.append (
                {"role": "user", "content": PROMPT}
            )

            print ("SML Ativado")

        else:

            MENSAGENS = [
                {"role": "system", "content": self.SYSTEM_PROMPT}
            ]
        
            if HISTÓRICO:
                MENSAGENS.extend (HISTÓRICO)
            
            MENSAGENS.append (
                {"role": "user", "content": PROMPT}
            )

            print (MENSAGENS)

        try:

            OUTPUT = self.API.chat.completions.create (model = "/modelos/MicrosoftPhi15B", messages = MENSAGENS, stream = True)
            print (OUTPUT)

            RESPOSTA = ""
            for tokens in OUTPUT:
                RESPOSTA += tokens.choices[0].delta.content
                yield RESPOSTA
                

            #TOKENS = OUTPUT.usage.total_tokens

            ##Prefil Stats
            #TEMPO_PREFILL = OUTPUT.timings["prompt_ms"] / 1000
            #TOKENS_perS_PREFILL = OUTPUT.timings["prompt_per_second"] 
            
            ##Decode Stats
            #TEMPO_DECODE = OUTPUT.timings["predicted_ms"] / 1000
            #TOKENS_perS_DECODE = OUTPUT.timings["predicted_per_second"] 
            
            ##Latência Total
            #LAT = TEMPO_PREFILL + TEMPO_DECODE
            
            #return RESPOSTA #TOKENS, TEMPO_PREFILL, TOKENS_perS_PREFILL, TEMPO_DECODE, TOKENS_perS_DECODE, LAT

        except Exception as e:
            print (e)
            print ("Erro na Inferência!")
            
        
    def KILL_DOCKER_vLLM_MODEL (self):

        yield gr.update (visible = True)

        KILL_DOCKER = subprocess.run (["docker", "stop", f"{self.CONFIG['GPU_CONFIG']['vLLM']['Microsoft Phi 15B GPTQ Q4']['container']}"], capture_output = True, text = True)
        KILL_DOCKER = KILL_DOCKER.returncode

        if KILL_DOCKER == 0:
            pass

        if KILL_DOCKER == 1:
            print ("Erro no término do Docker!")

        yield "Modelo descarregado da memória!"
        time.sleep (5)

        yield gr.update (visible = False)