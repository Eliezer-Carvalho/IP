<h1> Docker </h1>
O Docker é um software de código aberto usado para implantar apps dentro de containers virtuais. A conteinerização permite que vários aplicativos funcionem em diferentes ambientes complexos. Por exemplo: o Docker permite executar o WordPress em sistemas Windows, Linux e macOS, sem problemas.
<hr>

<h2> Imagem </h2>
Uma imagem é como uma receita de uma aplicação. Na mesma está contida todas as dependências e código para uma aplicação funcionar.
<hr>

<h2> Container </h2>
Um container é onde uma imagem vive. Os containers são especiais porque podemos ter vários containers a rodar uma imagem. 
<hr>



docker images -> ver as imagens
docker image -> ver as opções para iniciar uma imagem
docker container -> ver as opções para iniciar um container 


docker run `     
   --gpus all `
   --ipc=host `
   -p 8000:8000 `
   -e VLLM_USE_V2_MODEL_RUNNER=0 `
   -v "C:\Users\Admin\Desktop\models\Language Models\GPU\Qwen 14B AWQ Q4:/models/qwen14B" `
   vllm/vllm-openai:latest `
   /models/qwen14B `
   --max-model-len 2046


docker run --rm`     
   --gpus all `
   --ipc=host `
   -p 8000:8000 `
   -e VLLM_USE_V2_MODEL_RUNNER=0 `
   -v "C:\Users\Admin\Desktop\models\Language Models\GPU\Qwen 14B AWQ Q4:/models/qwen14B" `
   vllm/vllm-openai:latest `
   /models/qwen14B `
   --max-model-len 2046





docker run --runtime nvidia --gpus "device=0" --ipc=host -v "C:\Users\Admin\Desktop\models\Language Models\GPU\Microsoft Phi 14B Q4:models/phi14b" -p 8000:8000 vllm/vllm-openai:latest --model models/phi14b --gpu-memory-utilization 0.85 --max-model-len 1600