from openai import OpenAI #https://developers.openai.com/api/reference/python
import torch

from transformers import GenerationConfig


"""
Esta classe representa a fase de Inferência dos modelos nas suas respetivas configurações.
"""

class Inference:

    def __init__ (self):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"


    def INFERENCE_GPU (self, modelo, tokenizer, context, prompt):

        mensagens = [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]

        tokens = tokenizer.apply_chat_template (mensagens, tokenize = True, add_generation_prompt = True, return_tensors = "pt").to(self.device)

        generation_config = GenerationConfig (
                max_new_tokens = 3200,
                temperature = 0.2,
                top_p = 0.9,
                do_sample = False,      # Respostas mais determinísticas
                eos_token_id = tokenizer.eos_token_id,
                pad_token_id = tokenizer.eos_token_id
            )

        with torch.inference_mode():
            logits = modelo.generate (**tokens, generation_config = generation_config)

        return tokenizer.decode (logits[0][tokens["input_ids"].shape[1]:], skip_special_tokens = True)


    def INFERENCE_CPU (context, prompt):

        mensagens = [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]


        """
        Comunicação via API com a biblioteca OpenAI! Não, não é apenas para modelos da OpenAI, é uma library multifacetada para todo o tipo de modelos.
        """

        API = OpenAI (base_url = "http://127.0.0.1:8080", api_key = "IP2026")


        return API.chat_completions.create (
            messages = mensagens
        )
   