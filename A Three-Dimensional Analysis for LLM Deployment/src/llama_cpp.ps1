#converter hf para gguf
convert_hf_to_gguf.py "file_path" --outfile x.gguf

#métricas de benchmark
llama-bench -m "file_path" -p 2000 -b 1024 -ngl 0 -n 50 -o json

#quantização do modelo
llama-quantize "file_path" "path_para_guardar_e_nome" q4_k_S

#modo command line interface cli
llama-cli -m "file_path"

#servidor estilo openai
llama-server -m "filepath"


