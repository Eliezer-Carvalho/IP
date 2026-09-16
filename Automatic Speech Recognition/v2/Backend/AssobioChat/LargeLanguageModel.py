from subprocess import Popen
from openai import OpenAI
import yaml
import requests

"""
Esta classe é a primeira classe do sistema Assobio - Chat.
Tem como principal objetivo rodar um modelo com o motor de inferência vLLM, reencaminhar mensagens para o modelo e retornar as respostas para o GUI.
"""

class LargeLanguageModelvLLM ():

    def __init__ (self):

        