import streamlit as st
from run import MAIN



st.header ("Selecione o caminho para um ficheiro de áudio:")
AUDIO_FILE = st.text_input ("Caminho")
SAVE = st.button ("Guardar Áudio")

if SAVE == True:
    st.spinner ("A guardar..")
    st.session_state.audio = AUDIO_FILE
    st.success ("Guardado!")


RUN_TRANSCRIÇÃO = st.button ("Começar Transcrição!")

if RUN_TRANSCRIÇÃO == True:

    st.spinner ("A transcrever o áudio..")
    trans = MAIN (st.session_state.audio)

    st.write (trans)
    st.success ("Áudio convertido para texto com sucesso!")