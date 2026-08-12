from transformers import AutoModelForCausalLM, AutoTokenizer

import torch

import traceback


class SLM:

    def __init__ (self):

        self.device = "cuda" if torch.cuda.is_available () else "cpu"
        self.MODELO = None
        self.TOKENIZER = None


    def LOAD_MODEL (self):

        self.MODELO = AutoModelForCausalLM.from_pretrained (r"C:\Users\Admin\Desktop\models\Language Models\Mistral 7B Q4", device_map = self.device)
        self.TOKENIZER = AutoTokenizer.from_pretrained (r"C:\Users\Admin\Desktop\models\Language Models\Mistral 7B Q4")


    def INFERENCE (self, prompt, transcrição):

        mensagens = [
            {"role": "system", "content": "És um modelo inserido num sistema de conversas sobre Transcrição de áudio. Vais receber Transcrições de Áudio e deves ter a capacidade de falar sobre as mesmas."},
            {"role": "user", "content": f"{prompt}\n Transcrição: {transcrição}"}
        ]

        tokens = self.TOKENIZER.apply_chat_template (mensagens, tokenize = True, add_generation_prompt = True, return_tensors = "pt").to(self.device)
        
        with torch.inference_mode ():
            logits = self.MODELO.generate (**tokens)


        return self.TOKENIZER.decode (logits[0][tokens["input_ids"].shape[1]:], skip_special_tokens = True)
