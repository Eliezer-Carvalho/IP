import gradio as gr
from dataclasses import dataclass

from Backend.AssobioAuditoria.main import RUN_ASSOBIO_AUDITORIA

from Backend.AssobioAuditoria.Database import SQL_FUNCTS

from Backend.AssobioChat.SLM import SLM
from Backend.AssobioChat.Database import SQL_FUNCT_ASSOBIOCHAT


@dataclass
class Info:
    contexto: str = "O Contexto refere-se ás instruções que queremos que o sistema siga.\nAqui é onde devemos defenir papéis, regras e limitações."
    prompt: str = "O Prompt é a mensagem que queremos enviar ao modelo.\nTendo defenido o contexto, o Prompt tem como objetivo comunicar com o modelo."



DB = SQL_FUNCTS ()
LM = SLM ()

DB2 = SQL_FUNCT_ASSOBIOCHAT ()

with gr.Blocks (title = "Assobio V2") as App:
    
    """
    Código para a Interface da Aba Assobio - Auditoria.
    ##################################################
    """
    with gr.Tab ("Assobio - Auditoria"):

        with gr.Row ():
            with gr.Column (scale = 1):

                AUDIOS_PATH = gr.File (file_count = "multiple", file_types = ["audio"], label = "", show_label = False, elem_id = "AUDIO") # Melhor que gr.Audio porque permite melhor controlo
                CONTEXTO = gr.TextArea (label = "Contexto", interactive = True, type = "text", autofocus = True, info = Info.contexto) # Text area para colocar o contexto
                PROMPT = gr.TextArea (label = "Prompt", interactive = True, type = "text", autofocus = True, info = Info.prompt) # Text area para colocar o prompt

                RUN = gr.Button (size = "md", elem_id = "RUN") # Botão para rodar o sistema
                ESTADO = gr.Textbox (interactive = False, label = "", show_label =  False, visible = False, elem_id = "ESTADO") # Textbox para mostrar o estado da auditoria
                RUN.click (fn = RUN_ASSOBIO_AUDITORIA, inputs = [AUDIOS_PATH, CONTEXTO, PROMPT], outputs = ESTADO) # O que acontece após clicar no botão ? 
                    
    """
    Código para a Interface da Aba Assobio - Auditoria.
    ##################################################
    """
    
    with gr.Tab ("Assobio - Base de Dados"):

        ID = gr.Dropdown (label = "", show_label = False, choices = DB.IDX_SQL (), elem_id = "ID") 

        with gr.Row ():

            with gr.Column (scale = 2, min_width = 500):

                DATA = gr.DateTime (label = "Data", interactive = False)

            with gr.Column (scale = 2, min_width = 500):
                
                MODELO = gr.Textbox (label = "Modelo")

                ################################################

            with gr.Column (scale = 2, min_width = 1000):

                AUDIO = gr.Audio (label = "Audio File")

                ################################################

            with gr.Column (scale = 2, min_width = 500):

                TRANS = gr.Textbox (label = "Transcrição")

            with gr.Column (scale = 2, min_width = 500):

                AUDITORIA = gr.Textbox (label = "Auditoria")

                ###############################################

        INFO = ID.change (fn = DB.VIEW_SQL, inputs = ID, outputs = [DATA, AUDIO, TRANS, AUDITORIA, MODELO])
        INFO.then (fn = lambda: gr.update (choices = DB.IDX_SQL ()), outputs = ID) # Para alterar o idx após run


    ############################################### Assobio Chat #################################################
    ##############################################################################################################
    ##############################################################################################################

    with gr.Tab ("Assobio - Chat - FASE BETA"):
        with gr.Sidebar (open = False):

            gr.Markdown ("## Conversas")

            CHAT_LIST = gr.Radio (choices = DB2.NUMBER_CHATS (), label = "", show_label = False, min_width = 50)



        #gr.ChatInterface (fn = print ("Hello World"))
        #gr.Chatbot (value = [{"role": "user", "content": "Olá"}, {"role": "assistant", "content": "Olá! Como posso ajudar?"}], label = "NJSCSNJ", buttons = ["copy_all"], layout = "bubble", placeholder = ["Olá", "Adeus"])
        #gr.ChatMessage (content = "")


        CHATBOX = gr.Chatbot (visible = True, elem_id = "CHATBOX", min_height = 725, label = "", show_label = False)

        CHATBOXSAVE = gr.List (visible = False) # Este componente guarda o histórico da conversa.

        CHATBOX.clear (fn = DB2.ADD_CHAT_HISTORY, inputs = CHATBOXSAVE) # Ao limpar, guarda na DB a conversa.
        #print (CHATBOX)
        
        X = CHAT_LIST.change (fn = DB2.GET_CHAT, inputs = CHAT_LIST, outputs = CHATBOX)
        X.then (fn = lambda: gr.update (choices = DB2.NUMBER_CHATS ()), outputs = CHAT_LIST)

        #MODELS = gr.Dropdown (show_label = False, choices = ["Mistral 7B Q4.0", "Microsoft Phi 4 Q4.0", "Amália 9B DPO Q8"], interactive = True, elem_id = "MODELS")
        PROMPT = gr.Textbox (submit_btn = True, type = "text", label = "", show_label = False, elem_id = "PROMPT", placeholder = "Olá")
        PROMPT.submit (LM.LOAD_INFER_MODEL, inputs = [PROMPT, CHATBOX], outputs = [CHATBOX, CHATBOXSAVE])
        
   
"""
És um sistema de Inteligência Artificial inserido num sistema de Transcrição de Áudios em Português Europeu.
Deves realizar auditoria ás transcrições dos áudios de acordo com estes parâmetros:

 . Análise de Sentimentos - Contente, Neutro ou Infeliz
 . Análise de Linguagem Técnica - Forte, Neutra ou Fraca
Deves retornar o output em formato JSON.

Lembra-te do teu papel, és um modelo que Audita transcrições de Áudio e deves retornar o output em formato JSON.

Olá, faz uma análise de Transcrição destes áudios.

"""

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

    #CHATBOX {
        height: 1000px;
    }

    #PROMPT {
        position: absolute;
        top: 765px;
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
