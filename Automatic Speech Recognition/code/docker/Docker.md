<h1> Docker </h1>
O Docker é um software de código aberto usado para implantar apps dentro de containers virtuais. A conteinerização permite que vários aplicativos funcionem em diferentes ambientes complexos. Por exemplo: o Docker permite executar o WordPress em sistemas Windows, Linux e macOS, sem problemas.
<hr>

<h2> Imagem </h2>
Uma imagem é como uma receita de uma aplicação. Na mesma está contida todas as dependências e código para uma aplicação funcionar.
<hr>

<h2> Container </h2>
Um container é onde uma imagem vive. Os containers são especiais porque podemos ter vários containers a rodar uma imagem. 
<hr>

<h2> Alguns Comandos Importantes </h2>

<i>docker images</i> -> ver as imagens <br>
<i>docker image</i> -> ver as opções para iniciar uma imagem <br>
<i>docker container</i> -> ver as opções para iniciar um container <br> 
<i>docker ps -a</i> -> ver containers <br> 
<i>docker rename "nome" "nome-novo"</i> -> alterar o nome de um container <br>
<i>docker start "nome-container"</i> -> Correr container existente <br>


Esta run funcionou no servidor:
``` python
docker run --runtime nvidia --gpus "device=0" -e VLLM_USE_V2_MODEL_RUNNER=0 --ipc=host -v "C:\Users\Admin\Desktop\models\Language Models\GPU\Microsoft Phi 15B GPTQ:/modelos/MicrosoftPhi15B" -p 8000:8000 vllm/vllm-openai:latest --model /modelos/MicrosoftPhi15B --gpu-memory-utilization 0.85 --max-model-len 1600
```