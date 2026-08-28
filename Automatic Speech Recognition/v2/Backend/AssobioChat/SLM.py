from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer, GenerationConfig
import torch
import yaml

from threading import Thread


class SLM: 

    def __init__ (self):

        self.device = "cuda" if torch.cuda.is_available () else "cpu"

        self.TOKENIZER = None
        self.MODELO = None

        with open (r"C:\Users\Admin\Desktop\ip\Automatic Speech Recognition\v2\Backend\AssobioChat\__config__.yaml", "r", encoding = "utf-8") as f:
            self.CONFIG = yaml.safe_load (f)

 
    def LOAD_INFER_MODEL (self, PROMPT, HISTORY):

        if self.MODELO is None:

            """
            Só LOAD de um modelo
            """
            MODELO_PATH = self.CONFIG["SLM_GPU"]["Microsoft Phi 4 Q4.0"]["path"] 
        
            self.TOKENIZER = AutoTokenizer.from_pretrained (MODELO_PATH)
            self.MODELO = AutoModelForCausalLM.from_pretrained (MODELO_PATH, device_map = self.device, dtype = torch.float16)

        
        HISTÓRICO = [] # Reconstrução do History porque traz informação a mais

        #print (HISTORY)

        """ Debug
        #if len (HISTORY) > 0:

            #print (HISTORY)
            #print (HISTORY[0].keys())
            #print (HISTORY[0])
            #print (HISTORY[0]["role"])
            #print (HISTORY[0]["content"])
        """

        if HISTORY: 
            for i in HISTORY:

                """ Debug 
                #print (i)
                #print (i["role"])
                #print (i["content"])
                """

                HISTÓRICO.append ({
                    "role": i["role"], "content": i["content"][0]["text"],
                }) 

        #print (HISTÓRICO)
        
        contexto = """
        És um modelo de Inteligência Artificial que está inserido num sistema de Chatbot em Português Europeu.
        Vais receber o contexto todo das conversas para conseguires responder de acordo com o contexto.
        
        Deves responder ás perguntas dos utilizadores de maneira fiel, simpática e correta. É fulcral que respondas apenas em Português Europeu.
        
        <Exemplo>
        Olá, quanto é 9 + 9 ?
        Olá, tudo bem ? 9 + 9 = 18.
        </Exemplo> 

        Deves funcionar como um Chatbot amigável e prestável e responder de maneira correta, direta e em Português Europeu.
        """ 

        message = [
            {"role": "system", "content": contexto},
            *HISTÓRICO,
            {"role": "user", "content": PROMPT}
        ]

        tokens = self.TOKENIZER.apply_chat_template (message, tokenize = True, add_generation_prompt = True, return_tensors = "pt").to (self.device)

        GEN_CONFIG = GenerationConfig (
            max_new_tokens = 512, 
            do_sample = True, 
            use_cache = True, 
            cache_implementation = "dynamic", 
            temperature = 1, 
            repetition_penalty = 1.1,
            exponentional_decay_length_penalty = -0.5,
            top_k = 50
            )

        STREAMING = TextIteratorStreamer (self.TOKENIZER, skip_prompt = True, skip_special_tokens = True)

        THREAD = Thread (target = self.MODELO.generate,
                         kwargs = {
                             **tokens,
                             "generation_config": GEN_CONFIG,
                             "streamer": STREAMING
                         }
        )
        THREAD.start ()

        #################### #################### #################### #################### ####################
        #################### #################### #################### #################### ####################
        
        output = [
            *HISTÓRICO,
            {"role": "user", "content": PROMPT},
            {"role": "assistant", "content": ""}
        ]        

        #print (output)

        resposta = ""

        for token in STREAMING:

            resposta += token

            output[-1]["content"] = resposta #-1 é o último
        
            yield output, output

        #print (type(output)) List