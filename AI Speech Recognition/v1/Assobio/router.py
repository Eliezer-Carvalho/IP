from transformers import AutoModelForCausalLM, AutoTokenizer
import yaml
import random 
import torch
import traceback
from subprocess import Popen #https://coderivers.org/blog/python-popen-subprocess/



class Model_Routing:

    def __init__ (self):

        with open  (r"v1\Assobio\Models_GPU.yaml", "r", encoding = "utf-8") as file:
            self.CONFIG_GPU = yaml.safe_load (file)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
#####################################

        with open (r"v1\Assobio\Models_CPU.yaml", "r", encoding = "utf-8") as file:
            self.CONFIG_CPU = yaml.safe_load (file)


    def LOAD_MODEL_GPU (self):
        """
        3 MODELOS PARA RODAR NA GPU.
        Amália 9B Q8 | Microsoft Phi 4 Q4 | Mistral 7B Q4
        """
        SELECTED = random.choice (list(self.CONFIG_GPU["MODELS"].keys())) # random.choice faz random de uma lista, melhor do que usar números

        try: 

            MODELO = AutoModelForCausalLM.from_pretrained (self.CONFIG_GPU["MODELS"][SELECTED]["path"], device_map = self.device, dtype = torch.float16)
            TOKENIZER = AutoTokenizer.from_pretrained (self.CONFIG_GPU["MODELS"][SELECTED]["path"])
    
        except Exception as e:
            traceback.print_exc()


        return SELECTED


    def LOAD_MODEL_CPU (self):
        """
        3 MODELOS PARA RODAR NA CPU. ÓBVIO QUE NÃO VAMOS RODAR DIRETO NA CPU, VAMOS USAR O MOTOR DE INFERÊNCIA llama.cpp PARA OBTERMOS UMA BOA PERFOMANCE NA CPU.
        Qwen 2.5 0.5B | Phi 3.5 Q4.0 | Bonsai 27B Q1.0
        """
        SELECTED = random.choice (list(self.CONFIG_CPU["MODELS"].keys()))

        try:

            self.SERVER = Popen ([
                r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\ggml.llamacpp_Microsoft.Winget.Source_8wekyb3d8bbwe\llama-server.exe",
                "-m", self.CONFIG_CPU["MODELS"][SELECTED]["path"],
                "-ngl", "0",
                "--no-webui",
            ])

        except Exception as e:
            traceback.print_exc()


        return SELECTED




    def TESTE (self):

        self.SERVER.kill()



