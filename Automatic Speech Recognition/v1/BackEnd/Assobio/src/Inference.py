from openai import OpenAI #https://developers.openai.com/api/reference/python
import torch

import time
from transformers import GenerationConfig


"""
Esta classe representa a fase de Inferência dos modelos nas suas respetivas configurações.
"""

class Inference:

    def __init__ (self):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"


    def INFERENCE_GPU (self, modelo, tokenizer, context, prompt, transcrição):

        mensagens = [
            {"role": "system", "content": context},
            {"role": "user", "content": f"{prompt}\n Transcrição: {transcrição}"}
        ]

        tokens = tokenizer.apply_chat_template (mensagens, tokenize = True, add_generation_prompt = True, return_tensors = "pt").to(self.device)

        """
        Uso de GenerationConfig, permite modificar de maneira fácil e simples a geração
        """
        generation_config = GenerationConfig (
                max_new_tokens = 480,
                temperature = 0.2,
                top_p = 0.9,
                do_sample = False,      # Respostas mais determinísticas
                eos_token_id = tokenizer.eos_token_id,
                pad_token_id = tokenizer.eos_token_id
            )

        with torch.inference_mode():
            logits = modelo.generate (**tokens, generation_config = generation_config)

        """
        Aqui temos de ter atenção porque os logits retornam o prompt mais a resposta.
        Por tal razão temos de indexar.
        """
        return tokenizer.decode (logits[0][tokens["input_ids"].shape[1]:], skip_special_tokens = True)

###############################################################################################################

    """
    Este método é especial porque usamos o motor de inferência Llama.cpp para rodar modelos mais pequenos na CPU.
    Desta maneira, realizamos Routing tanto de modelos como também de Hardware
    """
    def INFERENCE_CPU (self, context, prompt, transcrição):

        mensagens = [
            {"role": "system", "content": context},
            {"role": "user", "content": f"{prompt}\n Transcrição: {transcrição}"}
        ]


        """
        Comunicação via API com a biblioteca OpenAI! Não, não é apenas para modelos da OpenAI, é uma library multifacetada para todo o tipo de modelos.
        """

        API = OpenAI (base_url = "http://127.0.0.1:8080", api_key = "IP2026")


        time.sleep (3) #time.sleep para dar delay no código, estava-me a dar alguns erros ao carregar tudo muito rápido

        output = API.chat.completions.create (
            model = "x",
            messages = mensagens
        )

        print (output)

        return output.choices[0].message.content
   