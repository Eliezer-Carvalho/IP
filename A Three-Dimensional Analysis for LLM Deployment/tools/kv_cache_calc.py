import humanize

#KV Cache consiste numa métrica bastante importante quando se quer hospedar um modelo LLM.
#À medida que uma conversa com um modelo de Processamento de Linguagem Natural vai avançando, o número de tokens aumenta.
#Desta maneira, o modelo tem que ter em conta esse contexto. Esses vetores Key e Value são armazenados para evitar recalcular attention sobre todos os tokens anteriores.
#Esses cálculos têm de ser armazenados em algum lado. Esse armazenamento tem o nome de KV Cache.

#KV Cache Tradicional calcula o KV Cache de modelos com o mecanismo Attention tradicional

def KV_CACHE_TRADICIONAL (num_layers, context_length, hidden_size, bytes_per_value): 
#Estes parâmetros podem vir em nomes bastante diferentes
#Context_Length pode ser vários valores mas nunca superiores ao contexto máximo do modelo

    KV_CACHE = humanize.naturalsize (2 * num_layers * context_length * hidden_size * bytes_per_value) #2 = [K, V]
    return KV_CACHE

#Exemplo:
    #context_max = KV_CACHE_TRADICIONAL (12, 1024, 768, 2)
    #print (f"KV_CACHE_MAX do modelo GPT2 = {context_max}")



#----------------------------------------------------------------------------------------------------------------------------------------------------------



#KV cache é um dos maiores problemas de inferência em LLMs long-context.
#Por isso surgiram várias arquiteturas para tentar atacar este problema de maneiras diferentes.

def KV_CACHE_GQA (batch_size, num_layers, context_length, kv_heads, head_dim, bytes_per_value):
#Estes parâmetros podem vir em nomes bastante diferentes
#Context_Length pode ser vários valores mas nunca superiores ao contexto máximo do modelo
#Head_dim = Hidden_Size // num_attention_heads

    KV_CACHE = humanize.naturalsize (2 * batch_size * num_layers * context_length * kv_heads * head_dim * bytes_per_value)
    #KV_CACHE = 2 * batch_size * num_layers * context_length * kv_heads * head_dim * bytes_per_value
    
    return KV_CACHE


#Exemplo:
#contexto_max = KV_CACHE_GQA (1, 36, 30000, 8, 128, 2)
#print (f"KV_CACHE_MAX do modelo Qwen3-4B-Base = {contexto_max}")

