<h1> Introdução </h1>

Os modelos de Speech são normalmente compostos por um encoder responsável por transformar o áudio em embeddings ricos, contendo informação acústica, fonética e linguística. Estes encoders podem ser Foundation Models, treinados em grandes volumes de dados para aprender representações gerais (por exemplo, wav2vec 2.0, HuBERT, WavLM ou XLS-R), ou Task-specific Encoders, treinados diretamente para uma tarefa como ASR (por exemplo, Conformer, FastConformer ou Zipformer).

A partir dos embeddings produzidos pelo encoder, é adicionada uma head adequada à tarefa. Para reconhecimento automático de fala (ASR), as heads mais comuns são CTC e RNN-T, enquanto para classificação basta normalmente uma camada de pooling seguida de uma camada linear.

Existe ainda uma segunda família de modelos, baseada na arquitetura Transformer Encoder–Decoder, como o Whisper. Nestes modelos, o encoder produz embeddings do áudio e um decoder autoregressivo gera a transcrição token a token. Mais recentemente, alguns modelos multimodais substituem este decoder por um LLM (por exemplo, Qwen2-Audio), recorrendo a um projector para adaptar os embeddings do encoder ao espaço de embeddings do modelo de linguagem.

<h1> Conclusão </h1>

<b> Automatic Speech Recognition </b> é claramente uma área bastante interessante para empresas que trabalham com áudio. Foi também desenvolvido um sistema com capacidade de transcrever áudio e de realizar uma auditoria usando Small Language Models.

<h1> Papers Interessantes </h1>

https://arxiv.org/pdf/2402.08846 -> Paper aplicado no modelo <a href = "https://huggingface.co/amalia-llm/AMALIA-SFT-FALA"> AMALIA-SFT-FALA </a>

<h1> Stack </h1>

datasets, gradio, nvidiampl, openai, sqllite3, POO, yaml, traceback, subprocess, psutil, transformers, torch, llama.cpp 



