<h1> Transcrição.py </h1>

Responsável por dar Load do Model Whisper e por realizar ASR.

<h1> Model_Routing.py </h1>

Responsável pela implementação do Roteamento entre modelos e hardware.

<h1> Inference.py </h1>

Após o Roteamento ter terminado, envia-se a informação para a Inferência que realiza a auditoria.

<h1> Database.py </h1>

Responsável por guardar os dados e também por fornecer dados para o Front End.

<h1> Main.py </h1>

Responsável por ligar todas estes ficheiros num só. <br>
O sistema funciona da seguinte maneira: <br>

```mermaid
flowchart LR
    WHISPER.LOAD_MODEL[Load ASR Model]
    --> WHISPER.TRANSCRIPTION[Transcrição do Áudio]
    --> MODEL.ROUTING[Model Routing]
    --> ROUTING.LOAD_MODEL[Carregamento do SLM]
    --> INFERENCE.INFERENCE[Inferência do SLM]
    --> DB.ADD_DATA[Guardar na Base de Dados]
    DB.ADD_DATA --> |Áudio a Áudio| WHISPER.TRANSCRIPTION