import gradio as gr
import time


from Assobio.stats import Statistics_Monitor
from Assobio.whisper import WHISPER_AI
from Assobio.router import Model_Routing
###################################################################################################




#################
MONITOR = Statistics_Monitor ()
WHISPER = WHISPER_AI () # Criar a Instância
TESTE = Model_Routing ()
#################

WHISPER.LOAD_MODEL()


with gr.Blocks(title = "Assobio V1") as App:

    with gr.Tab ("Assobio"):

        with gr.Sidebar (open = False):

            gr.Markdown ("# Estatísticas")
            gr.Markdown ("<hr>")

            #####################################################
            gr.Markdown (value = MONITOR.GPU_NAME) #https://gradio-two.vercel.app/main/docs/gradio/markdown
            gr.Markdown (value = MONITOR.GPU_MEMORY, every = 1) #https://gradio-two.vercel.app/main/docs/gradio/markdown
            gr.Markdown (value = MONITOR.GPU_UTILIZATION, every = 1) #https://gradio-two.vercel.app/main/docs/gradio/markdown
            gr.Markdown (value = MONITOR.GPU_TEMP, every = 1) #https://gradio-two.vercel.app/main/docs/gradio/markdown
            gr.Markdown (value = MONITOR.GPU_POWER, every = 1)
            gr.Markdown (value = MONITOR.GPU_ENERGY, every = 1)

            gr.Markdown ("<hr>")

            gr.Markdown (value = MONITOR.CPU_NAME)
            gr.Markdown (value = MONITOR.CPU_MEM_TOTAL, every = 1)
            gr.Markdown (value = MONITOR.CPU_MEM_USADA, every = 1)
            gr.Markdown (value = MONITOR.CPU_UTIL, every = 1)
            #####################################################




        ###################################
        gr.Markdown (
        """
        <p> <b> Assobio </b> é uma aplicação desenvolvida no âmbito do estágio curricular do curso de Robótica e Inteligência Artificial. 
        O projeto tem como objetivo o desenvolvimento de uma plataforma para transcrição automática e análise inteligente de conteúdos áudio, 
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
        
########
        button2 = gr.Button ("Fechar Server")
        sd = print ("Server Fechado")
        button2.click (fn = TESTE.TESTE, outputs = sd)

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
