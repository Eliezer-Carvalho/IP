from transformers import AutoModelForCausalLM, AutoTokenizer
import yaml #https://www.datacamp.com/pt/blog/what-is-yaml
import random 
import torch
import traceback
from subprocess import Popen #https://coderivers.org/blog/python-popen-subprocess/



"""
Esta classe é a implementação de um Model Routing para o lado dos Modelos de Linguagem Natural.
O Model Routing seleciona entre 6 modelos. De início a unica ponderação é o número de palavras da transcrição. Ou seja, quanto maior for a transcrição, mais potente o modelo carregado será.
O Model Routing também tem em conta load de modelos tanto em CPU como em GPU. Em vez de sobrecarregar a GPU com todos os modelos, os modelos mais leves são rodados pelo motor de inferência
llama.cpp em CPU. 
"""

class Model_Routing:

    def __init__ (self):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        """
        Uso de YAML, para criação de ficheiros de configuração! No futuro é mais fácil mudar algo, adicionar ou remover modelos.
        """

        with open  (r"v1\BackEnd\Assobio\__configs__\Models_GPU.yaml", "r", encoding = "utf-8") as file:
            self.CONFIG_GPU = yaml.safe_load (file)

        with open (r"v1\BackEnd\Assobio\__configs__\Models_CPU.yaml", "r", encoding = "utf-8") as file:
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


        return SELECTED, MODELO, TOKENIZER


    def LOAD_MODEL_CPU (self):
        """
        3 MODELOS PARA RODAR NA CPU. ÓBVIO QUE NÃO VAMOS RODAR DIRETO NA CPU, VAMOS USAR O MOTOR DE INFERÊNCIA llama.cpp PARA OBTERMOS UMA BOA PERFOMANCE NA CPU.
        Qwen 2.5 0.5B | Phi 3.5 Q4.0 | Bonsai 27B Q1.0
        """

        SELECTED = random.choice (list(self.CONFIG_CPU["MODELS"].keys()))

        """
        O motor de inferências llama.cpp tem as usas bases fundamentadas em Linux, o que torna o uso em Python no Windows uma grande dor de cabeça.
        Desta maneira, o sistema uso a CLI para iniciar um server com llama.cpp com o modelo selecionado carregado.
        Mais tarde para comunicarmos usamos uma API.
        """
        try:

            self.SERVER = Popen ([
                r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\ggml.llamacpp_Microsoft.Winget.Source_8wekyb3d8bbwe\llama-server.exe",
                "-m", self.CONFIG_CPU["MODELS"][SELECTED]["path"],
                "-c", "3200",
                "-ngl", "0",
                "--no-jinja",
                "--no-webui",
            ])

        except Exception as e:
            traceback.print_exc()


        return SELECTED



