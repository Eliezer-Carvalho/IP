import gradio as gr
from Backend.AssobioAuditoria.main import RUN_ASSOBIO_AUDITORIA





with gr.Blocks (title = "Assobio V2") as App:
    

    with gr.Tab ("Assobio - Auditoria"):

        with gr.Row ():

            with gr.Column (scale = 2, min_width = 500):

                AUDIOS_PATH = gr.File (file_count = "multiple", file_types = ["audio"], height = 0, label = "Audio Files", elem_id = "AUDIO") 
                # Melhor que gr.Audio porque permite melhor controlo
                
            with gr.Column (scale = 2, min_width = 300):

                CONTEXTO = gr.TextArea (label = "Contexto", interactive = True, type = "text", autofocus = True, elem_id = "CONTEXTO")
                PROMPT = gr.TextArea (label = "Prompt", interactive = True, type = "text", autofocus = True, elem_id = "CONTEXTO")


        BUTTON = gr.Button ()
        RUN = BUTTON.click (fn = RUN_ASSOBIO_AUDITORIA, inputs = [AUDIOS_PATH, CONTEXTO, PROMPT])


#COLORS = gr.themes.Soft (primary_hue = "slate", secondary_hue = "gray", neutral_hue = "teal")


App.launch (
    css = 
    """
    #AUDIO {
        height: 412px;
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







