#### Carregar Modelos ####

# Duas Opções -> Upload Local ou Upload via Hugging Face
#Como o objetivo é hospedar um modelo local foi feito o download do modelo para o ambiente pessoal para começar desde cedo a estabelecer algumas boas práticas.

#Libraries
from transformers import AutoTokenizer, AutoModelForCausalLM #https://huggingface.co/docs/transformers/index
import torch #https://pytorch.org/

MODELO_NAME = "x" #Se for via HF usar o nome do modelo
MODELO_PATH = "x" #Se for via ambiente pessoal é meter o caminho que indica a pasta

modelo = AutoModelForCausalLM.from_pretrained (MODELO_PATH, device_map = "auto") #device_map pode ser "cpu" ou "cuda"

tokenizer = AutoTokenizer.from_pretrained (MODELO_PATH) #load do tokenizer do modelo, importante para prompt processing e token generation


#### Inferência ####

# A Inferência pode ser um processo bem mais trabalhado (top_k, top_p, etc) mas aqui está uma versão simples.

input = tokenizer (prompt, return_tensor = "pt") #return_tensor = pytorch

probs = modelo (**input) #opcional

tokens = modelo.generate (**input, max_new_tokens = x) #** desfaz dict

texto = tokenizer.decode (tokens[0]) #token a token