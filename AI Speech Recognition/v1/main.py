import gradio as gr

from Assobio.stats import GPU_NAME, GPU_MEM_ALLOCADA, GPU_MEM_RESERVADA, CPU_NAME, CPU_MEM_TOTAL, CPU_MEM_USADA
from Assobio.whisper import WHISPER_AI

###################################################################################################




#################
WHISPER = WHISPER_AI() # Criar a Instância
#################

#WHISPER.LOAD_MODEL()


with gr.Blocks(title = "Assobio V1") as App:

    with gr.Tab ("Assobio"):

        with gr.Sidebar (open = False):

            gr.Markdown ("# Estatísticas")
            gr.Markdown ("<hr>")

            #####################################################
            gr.Markdown (value = GPU_NAME) #https://gradio-two.vercel.app/main/docs/gradio/markdown
            gr.Markdown (value = GPU_MEM_ALLOCADA, every = 1) #https://gradio-two.vercel.app/main/docs/gradio/markdown
            gr.Markdown (value = GPU_MEM_RESERVADA, every = 1) #https://gradio-two.vercel.app/main/docs/gradio/markdown

            gr.Markdown ("<hr>")

            gr.Markdown (value = CPU_NAME)
            gr.Markdown (value = CPU_MEM_TOTAL, every = 1)
            gr.Markdown (value = CPU_MEM_USADA, every = 1)
            #####################################################

        ###################################
        gr.Markdown (
        """
        <p> <b> Assobio </b> é uma aplicação desenvolvida no âmbito do estágio curricular do curso de Robótica e Inteligência Artificial. 
        O projeto visa o desenvolvimento de uma plataforma para transcrição automática e análise inteligente de conteúdos áudio, 
        integrando modelos de Automatic Speech Recognition (ASR) e Small Language Models (SLMs) disponibilizados através de uma interface web interativa. </p>
        """
        )
        gr.Markdown ("<hr>")
        ###################################

        #gr.Audio ()
        ###########################################
        AUDIOS_PATH = gr.File (file_count = "multiple", file_types = ["audio"], height = 175, label = "WAV Files")

        button = gr.Button ("Transcrever Áudio")

        y = gr.Textbox ()
        button.click (fn = WHISPER.ASSOBIO, inputs = AUDIOS_PATH, outputs = y)
        ###########################################
        
    #audio = gr.Audio()



tema = gr.themes.Default(primary_hue = gr.themes.colors.red, secondary_hue = gr.themes.colors.pink, font = [gr.themes.GoogleFont("Inconsolata"), "Arial", "sans-serif"]) #gr.themes.Default() gr.themes.Soft() gr.themes.Monochrome() gr.themes.Glass() gr.themes.Base()
App.launch (
    theme = tema, 
    # N funciona ?? favicon_path = "v1\logos\IP_LogomarcaPrincipal_RGB-Cor.jpg",
    css = 
    """
    
    footer {
        visibility: hidden;
    }
    
    
    """
    )
