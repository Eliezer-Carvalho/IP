#converter hf para gguf
convert_hf_to_gguf.py "file_path" --outfile x.gguf
python .\convert_hf_to_gguf.py "C:\Users\Admin\Desktop\models\amalia-llmAMALIA-9B-0626-DPO\Original" --outfile "C:\Users\Admin\Desktop\models\amalia-llmAMALIA-9B-0626-DPO\GGUF\amalia-bf16.gguf" --outtype bf16

#métricas de benchmark
llama-bench -m "file_path" -p 2000 -b 1024 -ngl 0 -n 50 -o json

#quantização do modelo
llama-quantize "file_path" "path_para_guardar_e_nome" q4_k_S
llama-quantize "C:\Users\Admin\Desktop\models\amalia-llmAMALIA-9B-0626-DPO\GGUF\amalia-bf16.gguf" "C:\Users\Admin\Desktop\models\amalia-llmAMALIA-9B-0626-DPO\ggufq\amalia_q2K" Q2_K
#https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md
#https://github.com/ggml-org/llama.cpp/pull/1684

#modo command line interface cli
llama-cli -m "file_path"

#servidor estilo openai
llama-server -m "filepath" #https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md?utm_source=chatgpt.com
  --host #Endereço  
  --port #Porta HTTP
  -c #Contexto
  -ngl #GPU Layers
  -t #Número de Threads da CPU
  -b #Batch Size
  -ub #Micro Batch Size
  --flash-attn #Flash Attention se suportado
  --jinja #Ativa Chat Template
  --no-webui #Desativa interface WEB
  --verbose #Logs detalhados

