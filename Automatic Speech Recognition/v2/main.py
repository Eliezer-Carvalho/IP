import gradio as gr

from dataclasses import dataclass

from Backend.AssobioAuditoria.main import Assobio_Auditoria
from Backend.AssobioAuditoria.DatabaseAssobioAuditoria.Database import SQL_Functions
from Backend.AssobioAuditoria.Estats import Statistics_Monitor

SQL = SQL_Functions ()
STATS = Statistics_Monitor ()

###################################

#from Backend.AssobioChat.SLM import SLM

#from Backend.AssobioChat.Database import SQL_Functions_Chat

#SQL_CHAT = SQL_Functions_Chat ()

from Backend.AssobioChat.LargeLanguageModel import LargeLanguageModelvLLM

vLLM_LLM = LargeLanguageModelvLLM ()

###################################

from Backend.AssobioChat.SemanticLayer import Semantic_Layer

SM_Layer = Semantic_Layer ()




@dataclass
class Info:
    contexto: str = "O Contexto refere-se ás instruções que queremos que o sistema siga.\nAqui é onde devemos defenir papéis, regras e limitações."
    prompt: str = "O Prompt é a mensagem que queremos enviar ao modelo.\nTendo defenido o contexto, o Prompt tem como objetivo comunicar com o modelo."





with gr.Blocks (title = "Assobio V2") as App:
    
    """
    Código para a Interface da Aba Assobio - Auditoria.
    ##################################################
    """
    with gr.Tab ("Assobio - Auditoria"):

        with gr.Sidebar (open = True):
        
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

        with gr.Row ():
            with gr.Column (scale = 1):

                AUDIOS_PATH = gr.File (file_count = "multiple", file_types = ["audio"], label = "", show_label = False, elem_id = "AUDIO") # Melhor que gr.Audio porque permite melhor controlo
                CONTEXTO = gr.TextArea (label = "Contexto", interactive = True, type = "text", autofocus = True, info = Info.contexto) # Text area para colocar o contexto
                PROMPT = gr.TextArea (label = "Prompt", interactive = True, type = "text", autofocus = True, info = Info.prompt) # Text area para colocar o prompt

                RUN = gr.Button (size = "md", elem_id = "RUN") # Botão para rodar o sistema
                ESTADO = gr.Textbox (interactive = False, label = "", show_label =  False, visible = False, elem_id = "ESTADO") # Textbox para mostrar o estado da auditoria
                RUN.click (fn = Assobio_Auditoria, inputs = [AUDIOS_PATH, CONTEXTO, PROMPT], outputs = ESTADO) # O que acontece após clicar no botão ? 
                    
    """
    Código para a Interface da Aba Assobio - Auditoria.
    ##################################################
    """
    
    with gr.Tab ("Assobio - Base de Dados"):

        with gr.Sidebar (open = True):
                
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

        ID = gr.Dropdown (label = "", show_label = False, choices = SQL.IDX_SQL (), elem_id = "ID") 

        with gr.Row ():

            DATA = gr.DateTime (interactive = False, label = "Data", min_width = 300)
            CONTEXT = gr.Textbox (label = "Contexto", min_width = 300)
            PROMPT = gr.Textbox (label = "Prompt", min_width = 300)

        with gr.Row ():

            AUDIO_ORIGINAL = gr.Audio (label = "Áudio Original", min_width = 500)
            AUDIO_PRE_PROCESS = gr.Audio (label = "Áudio Pré Processado", min_width = 500)

        with gr.Row ():

            AUDIO_TIME = gr.Textbox (label = "Duração do Áudio (s)", min_width = 500)
            TEMPO_PRE_PROCESS = gr.Textbox (label = "Tempo de Pré Processamento (s)", min_width = 500)

        with gr.Row ():

            TRANS = gr.Textbox (label = "Transcrição do Áudio")

        with gr.Row ():

            TEMPO_PROCESS = gr.Textbox (label = "Tempo de Processamento do Modelo ASR (s)", min_width = 300)
            TEMPO_INFER = gr.Textbox (label = "Tempo de Inferência do Modelo ASR (s)", min_width = 300)
            LAT = gr.Textbox (label = "Latência do Modelo ASR (s)", min_width = 300)
            TOKENS_per_s = gr.Textbox (label = "Throughput do Modelo ASR (tokens/s)", min_width = 300)

        gr.Markdown ("\n<hr>\n")

        with gr.Row ():

            HARDWARE = gr.Textbox (label = "Hardware", min_width = 500)
            MODELO = gr.Textbox (label = "Modelo", min_width = 500)

        with gr.Row ():

            AUDITORIA = gr.Markdown (label = "Auditoria")

        with gr.Row ():

            NUMERO_TOKENS = gr.Textbox (label = "Número de Tokens Processados pelo Modelo", min_width = 500)
            LATENCIA_LLM = gr.Textbox (label = "Latência (s)", min_width = 500)

        with gr.Row ():

            TEMPO_PREFILL = gr.Textbox (label = "Tempo Prefill (s)")
            TOKENS_PER_s_PREFILL = gr.Textbox (label = "Throughput Prefill (tokens/s)")
            TEMPO_DECODE = gr.Textbox (label = "Tempo Decode (s)")
            TOKENS_PER_S_DECODE = gr.Textbox (label = "Throughput Decode (tokens/s)")
            
            
        INFO = ID.change (fn = SQL.VIEW_SQL, inputs = ID, outputs = [DATA, CONTEXT, PROMPT, AUDIO_ORIGINAL, AUDIO_PRE_PROCESS, AUDIO_TIME, TEMPO_PRE_PROCESS, TRANS, TEMPO_PROCESS, TEMPO_INFER, LAT, TOKENS_per_s, HARDWARE, MODELO, AUDITORIA, NUMERO_TOKENS, TEMPO_PREFILL, TOKENS_PER_s_PREFILL, TEMPO_DECODE, TOKENS_PER_S_DECODE, LATENCIA_LLM])
        INFO.then (fn = lambda: gr.update (choices = SQL.IDX_SQL ()), outputs = ID) # Para alterar o idx após run


    """
    Código para a Interface da Aba Assobio - Chat.
    ##################################################
    """

    
    with gr.Tab ("Assobio - Chat"):
        with gr.Sidebar (open = True):

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

            gr.Markdown ("<hr>")

            BUTTON_LOAD_MODEL_vLLM = gr.Button (value = "Load Model", size = "md")
            ESTADO_LOAD_MODEL = gr.Textbox (interactive = False, label = "", show_label =  False, visible = False)
            BUTTON_LOAD_MODEL_vLLM.click (fn = vLLM_LLM.LOAD_MODEL_GPU_vLLM_DOCKER, outputs = ESTADO_LOAD_MODEL)

            BUTTON_KILL_vLLM = gr.Button (value = "Kill Model", size = "md")
            ESTADO_KILL_vLLM = gr.Textbox (interactive = False, label = "", show_label = False, visible = False)
            BUTTON_KILL_vLLM.click (fn = vLLM_LLM.KILL_DOCKER_vLLM_MODEL, outputs = ESTADO_KILL_vLLM)

        #-----------------------------------------------------------------------------------------------------------------------------#

        with gr.Row ():

            ESTADO_SEMANTIC_LAYER = gr.State (False)
            BUTTON_SEMANTIC_LAYER = gr.Button ("Camada Semântica: OFF", variant = "secondary", size = "md")
            BUTTON_SEMANTIC_LAYER.click (fn = SM_Layer.GRADIO_SEMANTIC_LAYER_ACTIVE, inputs = BUTTON_SEMANTIC_LAYER, outputs = [BUTTON_SEMANTIC_LAYER, ESTADO_SEMANTIC_LAYER])

            
        gr.Markdown ("<hr>")

        with gr.Column ():
            CHATBOT = gr.Chatbot (show_label = False, min_height = 700)
            CHATBOX = gr.ChatInterface (fn = vLLM_LLM.INFER_GPU_vLLM_DOCKER, chatbot = CHATBOT, additional_inputs = [ESTADO_SEMANTIC_LAYER])
         
        

App.launch (
    css = 
    """
    #AUDIO {
        height: 200px;
    }

    #ESTADO {
        height: 50px;
    }

    /* */

    #ID {
        height: 75px;
    }

    #STATE {
        height: 100px;
    }

    footer {
        visibility: hidden;
    }

    """,

    theme = gr.themes.Ocean (
        primary_hue = "red", #https://gradio.app/guides/theming-guide
        secondary_hue = "blue",

        text_size = "md",

        #font = "Inter",
        #font_mono = "JetBrains Mono", 
    ),

    inbrowser = True, # Tem que ficar em último, se não, não funciona!
)
