import gradio as gr

from BackEnd.Assobio.Stats import Statistics_Monitor
####################################################
from BackEnd.Assobio.src.Main import Whisper





ESTATS = Statistics_Monitor ()
WHISPER = Whisper ()

""" LOAD MODEL """
WHISPER.LOAD_MODEL_WHISPER ()
WHISPER.LOAD_MODEL_SLM ()



with gr.Blocks (title = "Assobio V2") as App:

    with gr.Tab ("Assobio"):

        with gr.Sidebar (open = True):

            gr.Markdown ("# Estatísticas")

            gr.Markdown ("<hr>")

            #####################################################
            gr.Markdown (value = ESTATS.GPU_NAME) #https://gradio-two.vercel.app/main/docs/gradio/markdown
            gr.Markdown (value = ESTATS.GPU_MEMORY, every = 1) #https://gradio-two.vercel.app/main/docs/gradio/markdown
            gr.Markdown (value = ESTATS.GPU_UTILIZATION, every = 1) #https://gradio-two.vercel.app/main/docs/gradio/markdown
            gr.Markdown (value = ESTATS.GPU_TEMP, every = 1) #https://gradio-two.vercel.app/main/docs/gradio/markdown
            gr.Markdown (value = ESTATS.GPU_POWER, every = 1)
            gr.Markdown (value = ESTATS.GPU_ENERGY, every = 1)

            gr.Markdown ("<hr>")

            gr.Markdown (value = ESTATS.CPU_NAME)
            gr.Markdown (value = ESTATS.CPU_MEM_TOTAL, every = 1)
            gr.Markdown (value = ESTATS.CPU_MEM_USADA, every = 1)
            gr.Markdown (value = ESTATS.CPU_UTIL, every = 1)
            #####################################################

    
        gr.Markdown (
        """
        <p> <b> Assobio </b> é uma aplicação desenvolvida no âmbito do estágio curricular do curso de Robótica e Inteligência Artificial. 
        O projeto tem como objetivo o desenvolvimento de uma plataforma para transcrição automática e análise inteligente de conteúdos áudio, 
        integrando modelos de Automatic Speech Recognition (ASR) e Small Language Models (SLMs) disponibilizados através de uma interface web interativa. </p>
        """
        )
        gr.Markdown ("<hr>")


        gr.Markdown ("<h1> Carregar Áudios </h1>")
        AUDIOS_PATH = gr.File (file_count = "multiple", file_types = ["audio"], height = 150, label = "WAV Files")

        BUTTON = gr.Button ("RUN TRANSCRIÇÃO")
        TRANSCRI = gr.TextArea (interactive = True)
        BUTTON.click (fn = WHISPER.WHISPER_TRANSCRIPTION, inputs = [AUDIOS_PATH], outputs = TRANSCRI)
         
        
        gr.Markdown ("<h1> Chat </h1>")
        CHAT = gr.ChatInterface (fn = WHISPER.INFERENCE)

        
        #BUTTON.click (fn = FUNCTION, inputs = [], outputs = )
 


App.launch (
    #theme = tema, 
    # N funciona ?? favicon_path = "v1\logos\IP_LogomarcaPrincipal_RGB-Cor.jpg",
    css = 
    """
    
    footer {
        visibility: hidden;
    }
    
    
    """,
    )
