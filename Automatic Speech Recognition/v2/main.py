import gradio as gr
from Backend.AssobioAuditoria.main import RUN_ASSOBIO_AUDITORIA
from Backend.AssobioAuditoria.Database import SQL_FUNCTS


from Backend.AssobioChat.SLM import SLM
from Backend.AssobioChat.Database import SQL_FUNCT_ASSOBIOCHAT


DB = SQL_FUNCTS ()
LM = SLM ()

DB2 = SQL_FUNCT_ASSOBIOCHAT ()

with gr.Blocks (title = "Assobio V2") as App:
    
    ########################################### Assobio Auditoria #################################################

    with gr.Tab ("Assobio - Auditoria"):

        with gr.Row ():

            with gr.Column (scale = 2, min_width = 500):

                AUDIOS_PATH = gr.File (file_count = "multiple", file_types = ["audio"], height = 0, label = "Audio Files", elem_id = "AUDIO") 
                # Melhor que gr.Audio porque permite melhor controlo
                
            with gr.Column (scale = 2, min_width = 300):

                CONTEXTO = gr.TextArea (label = "Contexto", interactive = True, type = "text", autofocus = True, elem_id = "CONTEXTO")
                PROMPT = gr.TextArea (label = "Prompt", interactive = True, type = "text", autofocus = True, elem_id = "CONTEXTO")

        with gr.Row ():

            with gr.Column (scale = 2, min_width = 950):

                BUTTON = gr.Button (size = "sm")

                STATE = gr.Textbox (elem_id= "STATE", max_lines = 1, interactive = False, label = "Estados de Execução")

        RUN = BUTTON.click (fn = RUN_ASSOBIO_AUDITORIA, inputs = [AUDIOS_PATH, CONTEXTO, PROMPT], outputs = STATE)

        """
        ############################################################################################################
        ############################################################################################################
        ############################################################################################################
        ############################################################################################################

        ######### Base de Dados ##########################
        """

        ID = gr.Dropdown (label = "Selecionar ID", choices = DB.IDX_SQL (), elem_id = "ID") 

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

    with gr.Tab ("Assobio - Chat"):
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
        height: 412px;
    }

    #ID {
        height: 100px;
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

    theme = gr.themes.Base (
        primary_hue = "teal", 
        secondary_hue = "purple", 
        neutral_hue = "neutral", #https://gradio.app/guides/theming-guide
        
        radius_size = "md",
        text_size = "md",

        #font = "Inter",
        #font_mono = "JetBrains Mono", 
    ),

    inbrowser = True, # Tem que ficar em último, se não, não funciona!
)
