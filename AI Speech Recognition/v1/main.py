import gradio as gr


from BackEnd.Assobio.Stats import Statistics_Monitor

from BackEnd.Assobio.src.main import SOURCE
###################################################################################################




#################
STATS = Statistics_Monitor ()
#################




with gr.Blocks(title = "Assobio V1") as App:

    with gr.Tab ("Assobio"):

        with gr.Sidebar (open = False):

            gr.Markdown ("# Estatísticas")
            gr.Markdown ("<hr>")

            #####################################################
            gr.Markdown (value = STATS.GPU_NAME) #https://gradio-two.vercel.app/main/docs/gradio/markdown
            gr.Markdown (value = STATS.GPU_MEMORY, every = 1) #https://gradio-two.vercel.app/main/docs/gradio/markdown
            gr.Markdown (value = STATS.GPU_UTILIZATION, every = 1) #https://gradio-two.vercel.app/main/docs/gradio/markdown
            gr.Markdown (value = STATS.GPU_TEMP, every = 1) #https://gradio-two.vercel.app/main/docs/gradio/markdown
            gr.Markdown (value = STATS.GPU_POWER, every = 1)
            gr.Markdown (value = STATS.GPU_ENERGY, every = 1)

            gr.Markdown ("<hr>")

            gr.Markdown (value = STATS.CPU_NAME)
            gr.Markdown (value = STATS.CPU_MEM_TOTAL, every = 1)
            gr.Markdown (value = STATS.CPU_MEM_USADA, every = 1)
            gr.Markdown (value = STATS.CPU_UTIL, every = 1)
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
        gr.Markdown ("<h1> Carregue os seus Áudios </h1>")
        AUDIOS_PATH = gr.File (file_count = "multiple", file_types = ["audio"], height = 175, label = "WAV Files")

        gr.Markdown ("<h1> Insira o seu Contexto </h1>")
        CONTEXTO = gr.TextArea (placeholder = "Olá", interactive = True, type = "text", label = "Olá", info = """És um sistema de Inteligência Artificial, deves avaliar a Transcrição proveviente dos Áudios de acordo com estas métricas: Divertido, Importante, Linguagem.
                                                                                                                Cada métrica deve ser avaliada de 0 a 10.

                                                                                                                Deves:
                                                                                                                Avaliar as métricas no formato pretendido.
                                                                                                                Devolver o resultado usando o menor número de tokens possíveis.
                                                                                                                Não precisas de dar justificação.



                                                                                                                Qualquer resposta fora deste contexto, está considerada errada!!!?""")

        gr.Markdown ("<h1> Insira o seu Prompt </h1>")
        PROMPT = gr.TextArea (placeholder = "Olá", interactive = True, type = "text", label = "Olá", info = "Olá, faz-me a análise do conteúdo Transcrito deste áudio!")

    
        button = gr.Button ("DO ALL")
        TRANSCRIÇÃO = button.click (fn = SOURCE, inputs = [AUDIOS_PATH, CONTEXTO, PROMPT])
    
        ###########################################

    #audio = gr.Audio()


    with gr.Tab ("Assobio - Base de Dados"):

        gr.Dropdown (label = "dkcmkd")


tema = gr.themes.Default (primary_hue = gr.themes.colors.red, secondary_hue = gr.themes.colors.blue, font = [gr.themes.GoogleFont("Inconsolata"), "Arial", "sans-serif"]) #gr.themes.Default() gr.themes.Soft() gr.themes.Monochrome() gr.themes.Glass() gr.themes.Base()
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
