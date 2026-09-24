import gradio as gr


from Backend.Estats import Statistics_Monitor
from Backend.Infer import GPU_vLLM_INFER

STATS = Statistics_Monitor ()
INFER = GPU_vLLM_INFER ()

with gr.Blocks (title = "RAG") as App:

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
    #########################################################################################

    
    gr.File (label = "", show_label = False, file_types = [".pdf"], file_count = "multiple", elem_id = "File_Input")

    gr.Markdown ("<hr>")
    
    CHATBOX = gr.Chatbot (show_label = False, min_height = 750)
    gr.Interface (fn = INFER.RUN, chatbot = CHATBOX)






App.launch (

    css = 
    """
    #File_Input {
        height: 200px;
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