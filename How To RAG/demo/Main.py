import streamlit as st
from code.llm import LOAD_MODEL, INFERENCE_MODEL

import torch
import gc


if "modelo_atual" not in st.session_state:
    st.session_state.modelo_atual = None

# Sidebar
with st.sidebar:
    
    # Config
    st.header ("Configurações")
    SELECT_MODEL = st.selectbox(label = "Modelos Disponíveis:", options = ["Qwen 0.5B", "Phi 3B", "Mistral 7B", "Amália"], index = None)

    estado = st.empty() #placeholder vazio para depois enviar mensagem de modelo carregado


    #Estatísticas
    st.header ("Estatísticas")

    st.metric ("GPU:", torch.cuda.get_device_name())

    gpu_mem_allocada = st.empty() #placeholder vazio para mais tarde atualizar
    gpu_mem_reservada = st.empty()

    mem_atual_allocada = torch.cuda.memory_allocated() / 1024**3
    mem_atual_reserved = torch.cuda.memory_reserved() / 1024**3
    
    gpu_mem_allocada.metric ("Memória Alocada:" , f"{mem_atual_allocada:.2f} GB")
    gpu_mem_reservada.metric ("Memória Reservada:", f"{mem_atual_reserved:.2f} GB")


if SELECT_MODEL != st.session_state.modelo_atual:
    #------- LOAD MODEL #---------

    if "modelo" in st.session_state:
        del st.session_state.modelo
        del st.session_state.tokenizer
        torch.cuda.empty_cache()
        gc.collect()

    if SELECT_MODEL != None:
        tokenizer, modelo = LOAD_MODEL (SELECT_MODEL)

        st.session_state.tokenizer = tokenizer
        st.session_state.modelo = modelo
        st.session_state.modelo_atual = SELECT_MODEL

        estado.success (f"Modelo {SELECT_MODEL} carregado.")

    if SELECT_MODEL == None:

        torch.cuda.empty_cache ()
        torch.cuda.reset_max_memory_allocated ()
        gc.collect()

        mem_atual_allocada = torch.cuda.memory_allocated() / 1024**3
        mem_atual_reserved = torch.cuda.memory_reserved() / 1024**3

        gpu_mem_allocada.metric ("Memória Alocada:" , f"{mem_atual_allocada:.2f} GB")
        gpu_mem_reservada.metric ("Memória Reservada:", f"{mem_atual_reserved:.2f} GB")

        st.session_state.modelo_atual = None
    #-------------

    #------------ GPU MEM #------------------
    mem_atual_allocada = torch.cuda.memory_allocated() / 1024**3
    mem_atual_reserved = torch.cuda.memory_reserved() / 1024**3

    gpu_mem_allocada.metric ("Memória Alocada:" , f"{mem_atual_allocada:.2f} GB")
    gpu_mem_reservada.metric ("Memória Reservada:", f"{mem_atual_reserved:.2f} GB")
    #-------------------


#----------------------------------------------------------------------------------------------------------------------------------------------------


mensagens = st.chat_input ()

if mensagens != None and SELECT_MODEL != None:

    tokens = INFERENCE_MODEL (mensagens, st.session_state.tokenizer, st.session_state.modelo, st.session_state.modelo_atual)

    with st.chat_message ("assistant"):

            resposta = ""

            placeholder = st.empty()

            for token in tokens:

                resposta += token

                placeholder.markdown(resposta)

            placeholder.markdown (resposta)