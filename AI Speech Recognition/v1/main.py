import gradio as gr

from Assobio.stats import GPU_NAME, GPU_MEM_ALLOCADA, GPU_MEM_RESERVADA
from Assobio.whisper import WHISPER_AI

###################################################################################################




#################
WHISPER = WHISPER_AI() # Criar a Instância
#################


WHISPER.LOAD_MODEL()


with gr.Blocks() as App:

    with gr.Tab ("Assobio"):

        with gr.Sidebar (open = False):

            gr.Markdown ("# Estatísticas")
            gr.Markdown ("<hr>")

            #####################################################
            gr.Markdown (value = GPU_NAME) #https://gradio-two.vercel.app/main/docs/gradio/markdown
            gr.Markdown (value = GPU_MEM_ALLOCADA, every = 1) #https://gradio-two.vercel.app/main/docs/gradio/markdown
            gr.Markdown (value = GPU_MEM_RESERVADA, every = 1) #https://gradio-two.vercel.app/main/docs/gradio/markdown
            #####################################################

        ###################################
        gr.Markdown ("<p> <b> Assobio </b> é um projeto realizado no âmbito do estágio curricular do curso Robótica e Inteligência Artificial. </p>")
        gr.Markdown ("<hr>")
        ###################################

        #gr.Audio ()
        ###########################################
        x = gr.File (file_count = "directory", file_types = ["audio"], height = 175)

        buton = gr.Button ("Transcrever Áudio")

        y = gr.Markdown ()
        buton.click (fn = WHISPER.INFERENCE, inputs = x, outputs = y)
        ###########################################
        
    #audio = gr.Audio()



tema = gr.themes.Base() #gr.themes.Default() gr.themes.Soft() gr.themes.Monochrome() gr.themes.Glass() gr.themes.Base()
App.launch (
    theme = tema, 
    css = 
    """
    
    footer {
        visibility: hidden;
    }
    
    
    """
    )
