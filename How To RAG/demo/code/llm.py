from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer, GenerationConfig
import torch

from threading import Thread
#import streamlit as st

device = "cuda" if torch.cuda.is_available() else "cpu"

MODELOS_PATH = {
    "Qwen 0.5B": 
        {
            "path": r"C:\Users\Admin\Desktop\models\Qwen2.5-0.5B-Instruct", 
            "system_prompt": 
    """
    <|im_start|>system
     És um modelo de Inteligência Artificial, deves responder de maneira concisa e direta da maneira mais curta e rápida possível.
     Responde apenas em Português Europeu.
    <|im_end|>

    <|im_start|>user

    """ 
        },


    "Phi 3B":
        { 
            "path": r"C:\Users\Admin\Desktop\models\Phi-3.5-mini-instruct-Q4",
        },

    "Mistral 7B": 
        {
            "path": r"C:\Users\Admin\Desktop\models\Mistral-7B-Instruct-v0.3-Q4",
        },

    "Amália":
        {
            "path": r"C:\Users\Admin\Desktop\models\AMALIA-9B-0626-DPO-bnb",
        },
}

#@st.cache_resource # Esta ideia funcionava se desse para ter 3 modelos em memoria de uma vez
def LOAD_MODEL (model_name):

    tokenizer = AutoTokenizer.from_pretrained (MODELOS_PATH[model_name]["path"])
    modelo = AutoModelForCausalLM.from_pretrained (MODELOS_PATH[model_name]["path"], device_map = device)

    return tokenizer, modelo


#-----------------------------------------

def INFERENCE_MODEL (msg, tokenizer, modelo, model_name):

    tokens = tokenizer (msg, return_tensors = "pt").to(device)

    generation_config = GenerationConfig (
        max_new_tokens = 120,
        temperature = 0.2,
        top_p = 0.9,
        do_sample = False,      # Respostas mais determinísticas
        eos_token_id = tokenizer.eos_token_id,
        pad_token_id = tokenizer.eos_token_id
    )




    streaming = TextIteratorStreamer (tokenizer, skip_prompt = True, skip_special_tokens = True)

    thread = Thread (target = modelo.generate,
                     kwargs = {
                         **tokens,
                         "generation_config": generation_config,
                         "streamer": streaming,
                     })
    thread.start()

    return streaming


def INFERENCE_MODEL_RAG (msg, tokenizer, modelo, contexto, RAG):

    prompt = f"""
        ### Contexto do utilizador
        {contexto}

        ### Documentos recuperados
        {RAG}

        ### Pergunta
        {msg}

        ### Instruções
        - Dá prioridade aos documentos recuperados.
        - Usa o contexto do utilizador apenas como informação complementar.
        - Não inventes factos.
        - Se não houver informação suficiente, indica-o.
    """


    tokens = tokenizer (prompt, return_tensors = "pt").to(device)

    streaming = TextIteratorStreamer (tokenizer, skip_prompt = True, skip_special_tokens = True)

    thread = Thread (target = modelo.generate,
                     kwargs = {
                         **tokens,
                         "streamer": streaming,
                         "max_new_tokens": 256
                     })
    thread.start()

    return streaming






