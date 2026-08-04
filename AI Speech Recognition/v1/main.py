import gradio as gr
###################################################################################################
from dataclasses import dataclass
###################################################################################################
from BackEnd.Assobio.Stats import Statistics_Monitor
from BackEnd.Assobio.src.Database import SQL_FUNCTS
###################################################################################################
from BackEnd.Assobio.src.main import SOURCE
###################################################################################################

"""
Frontend principal. Usado Gradio que abstrai muita complexidade e torna mais rápido o processo
"""
"""
@dataclass de mensagens tipo da aplicação
"""

@dataclass
class TXT_MSG:

    msg_contexto_explained: str = """
    O prompt é apenas uma peça da arquitetura. O verdadeiro desafio está em desenhar instruções que forneçam o contexto certo. 
    Neste sentido, é importante definir um bom, curto e direto contexto para desta maneira aumentar a eficácia do modelo de Linguagem.
    """

    msg_context: str = """
    És um sistema de Inteligência Artificial, deves avaliar a Transcrição proveviente dos Áudios de acordo com estas métricas: Divertido, Importante, Linguagem.
    Cada métrica deve ser avaliada de 0 a 10.

    Deves:
    Avaliar as métricas no formato pretendido.
    Devolver o resultado usando o menor número de tokens possíveis.
    Não precisas de dar justificação.

    Qualquer resposta fora deste contexto, está considerada errada!!!
    """ 

    msg_prompt: str = """
    Olá, faz-me a análise do conteúdo Transcrito deste áudio!
    """


"""
LOAD das Instâncias
"""
#################
STATS = Statistics_Monitor ()
DB = SQL_FUNCTS ()
#################


with gr.Blocks(title = "Assobio V1") as App:

    with gr.Tab ("Assobio"):

        """
        Aba de Estatísticas. ####################################################################################################################
        """
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

        """
        Aba Principal ####################################################################################################################
        """
        gr.Markdown (
        """
        <p> <b> Assobio </b> é uma aplicação desenvolvida no âmbito do estágio curricular do curso de Robótica e Inteligência Artificial. 
        O projeto tem como objetivo o desenvolvimento de uma plataforma para transcrição automática e análise inteligente de conteúdos áudio, 
        integrando modelos de Automatic Speech Recognition (ASR) e Small Language Models (SLMs) disponibilizados através de uma interface web interativa. </p>
        """
        )
        gr.Markdown ("<hr>")
        
        #Load Áudio Files
        gr.Markdown ("<h1> Carregar Áudios </h1>")
        AUDIOS_PATH = gr.File (file_count = "multiple", file_types = ["audio"], height = 150, label = "WAV Files")

        #Load Context
        gr.Markdown ("<h1> Qual é o Context ?  </h1>")
        CONTEXTO = gr.TextArea (placeholder = TXT_MSG.msg_context, interactive = True, type = "text", label = "O que é Contexto ?", info = TXT_MSG.msg_contexto_explained, autofocus = True, lines = 2, max_lines = 15)

        #Load Prompt
        gr.Markdown ("<h1> Prompt </h1>")
        PROMPT = gr.TextArea (placeholder = TXT_MSG.msg_prompt, interactive = True, type = "text", autofocus = True, lines = 1, max_lines = 10)

        #Botão para Rodar Tudo
        button = gr.Button ("RUN")
        TRANSCRIÇÃO = button.click (fn = SOURCE, inputs = [AUDIOS_PATH, CONTEXTO, PROMPT])
    
##################################################################################################################################################################################################################################################################
##################################################################################################################################################################################################################################################################
##################################################################################################################################################################################################################################################################
##################################################################################################################################################################################################################################################################


    with gr.Tab ("Assobio - Base de Dados"):

        """
        Aba de Visualização da Base de Dados
        """

        #Seleção de ID para visualizar os dados de X id
        ID = gr.Dropdown (label = "Selecionar ID", choices = DB.IDX_SQL(), every = 1)

        #################################
        DATA = gr.Textbox (label = "Data")
        AUDIO = gr.Audio (label = "Áudio Original")
        TRANS = gr.TextArea (lines = 2, max_lines = 10, label = "Transcrição")
        AUDITORIA = gr.TextArea (label = "Auditoria do Modelo de Linguagem", lines = 5, max_lines = 10)
        MODEL = gr.TextArea (label = "Modelo que Realizou a Auditoria", max_lines = 1)
        AVAL = gr.TextArea (submit_btn = True, label = "Por favor, avalie a auditoria do Modelo!", max_lines = 1)
        #################################

        ID.change (fn = DB.VIEW_SQL, inputs = ID, outputs = [DATA, AUDIO, TRANS, AUDITORIA, MODEL, AVAL])
        AVAL.change (fn = DB.UPDATE_AVAL_SQL, inputs = [AVAL, ID])




tema = gr.themes.Default (font = [gr.themes.GoogleFont("Inconsolata"), "Arial", "sans-serif"]) #gr.themes.Default() gr.themes.Soft() gr.themes.Monochrome() gr.themes.Glass() gr.themes.Base()
App.launch (
    theme = tema, 
    # N funciona ?? favicon_path = "v1\logos\IP_LogomarcaPrincipal_RGB-Cor.jpg",
    css = 
    """
    
    footer {
        visibility: hidden;
    }
    
    
    """,
    # share = True
    )
