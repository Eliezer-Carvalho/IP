
<p align = "center">  <img width = "725" height = "600" src = "C:\Users\Admin\Desktop\ip\Automatic Speech Recognition\v1\img\main.gif">  </p>



```mermaid
flowchart TD
    subgraph INPUTS["Inputs do Sistema"]
        direction TD
        AUDIO[Áudios]
        CONTEXTO[Contexto]
        PROMPT[Prompt]
    end

    AUDIO --> TRANSCRIPTION[Transcrição do Áudio]
    TRANSCRIPTION --> SLM[Small Language Model]
    CONTEXTO --> SLM
    PROMPT --> SLM

    SLM --> AUDITORIA[Auditoria aos Áudios Transcritos]

    AUDITORIA --> SAVE[Save Database SQL]

    NOTE["Transcrição usando modelos ASR mais especificamente o modelo Whisper."]
    NOTE -.-> TRANSCRIPTION

    NOTE2["Foi usado Model Routing para o modelo não ser sempre o mesmo.\nForam usados 4 modelos e o Routing também funciona em termos de Hardware, tanto pode rodar em GPU caso a transcrição seja de um áudio longo ou roda em CPU com o motor de Inferência llama.cpp."]
    NOTE2 -.-> SLM

    NOTE3["Na Database é guardado os Áudios, Transcrição, Auditoria do Modelo, Modelo que realizou a Auditoria e Data."]
    NOTE3 -.-> SAVE

    style NOTE fill:#ff4040 , stroke:#e62020, color:#000000 
    style NOTE2 fill:#ff4040 , stroke:#e62020, color:#000000
    style NOTE3 fill:#ff4040 , stroke:#e62020, color:#000000
