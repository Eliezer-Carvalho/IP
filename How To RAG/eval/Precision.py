######################################################################################## Eliezer Carvalho - 2026 ##################################################################################################

#Quando uma Query é enviada pelo utilizador, num sistema RAG híbrido é realizada uma Procura Lexical e uma ou várias Procuras Vetoriais.
#Cada mecanismo gera a sua própria lista ordenada de resultados. É por norma utilizado o algoritmo Reciprocal Rank Fusion (RRF) para mergir estas listas numa única classificação final.
#https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking

def Reciprocal_Rank_Fusion (rankings, k = 60): #60 é um default value #Consultar doc -> https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf
    
    scores = {} #dict para save scores
    metadata = {} #dict para preservar os metadados

    for ranking in rankings: #iter sobre os resultados dos retrievals
        for rank, doc in enumerate(ranking): #rank carrega a pos dos docs e doc carrega os dados

            doc_id = doc.metadata["chunk_id"] #atribuição dos chunks_ids

            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1) #aplicação da fórmula e saved no dict scores

            ###Preservar os dados
            metadata[doc_id] = {
                "title": doc.metadata.get("title"),
                "content": doc.page_content
            }
            ####

    ranked = sorted(scores.items(), key = lambda x: x[1], reverse = True) #Ordenar pelos scores

    return [(metadata[doc_id]["title"], doc_id, metadata[doc_id]["content"], score) #Return final com scores, posições e dados importantes
        for doc_id, score in ranked
    ]

######################################################################################## Eliezer Carvalho - 2026 ##################################################################################################

#Estas funções têm como objetivo medir a métrica Precision@K de um sistema RAG tendo em conta o chunk ideal.
#Precision@K tem em vista calcular o número de chunks relevantes encontrados dentro do top_k 

## Sparse Retrieval - BM25 Retriever
def precision_sparse_retrieval (sparse_retrieval_obj, dataset):

    eval = []

    for dados in dataset:

        query = dados["query"]
        gold_chunks = set (dados["chunk_id"])

        sparse_retrieval = sparse_retrieval_obj.invoke (query)

        retrieved_ids = set (x.metadata["chunk_id"] for x in sparse_retrieval)

        equals = len (gold_chunks.intersection (retrieved_ids))

        precision = equals / len (sparse_retrieval) #Melhor maneira de perceber, encontra-se os relevantes dentro dos chunks ideais e depois divide-se pelo top_k

        eval.append (precision)

    return {
        "Precision@K Sparse Retrieval:": sum (eval) / len (eval)
    }


## Dense Retrieval - Embeddings Retriever
def precision_dense_retrieval (dense_retrieval_obj, dataset):

    eval = []

    for dados in dataset:

        query = dados ["query"]
        gold_chunk = set (dados ["chunk_id"])

        dense_retrieval = dense_retrieval_obj.invoke (query)

        retrieved_ids = set (x.metadata["chunk_id"] for x in dense_retrieval)

        equals = len (gold_chunk.intersection (retrieved_ids))

        precision = equals / len (dense_retrieval)

        eval.append (precision)

    return {
        "Precision@K Dense Retrieval:": sum (eval) / len (eval)
    }


## Hybrid Retrieval - Reciprocal Rank Fusion
def precision_hybrid_retrieval (sparse_retrieval_obj, dense_retrieval_obj, dataset, k: int):

    eval = []

    for dados in dataset:

        query = dados["query"]
        gold_chunks = set (dados["chunk_id"])

        sparse_retrieval = sparse_retrieval_obj.invoke (query)
        dense_retrieval = dense_retrieval_obj.invoke (query)

        rrf = Reciprocal_Rank_Fusion ([sparse_retrieval, dense_retrieval])

        rrf = rrf [:k]

        retrieved_ids = set (x[1] for x in rrf)

        equals = len (gold_chunks.intersection (retrieved_ids))

        precision = equals / len (rrf) #len(rrf) representa o k

        eval.append (precision)

    return {
        "Precision@K Hybrid Retrieval:": sum (eval) / len (eval)
    }


######################################################################################## Eliezer Carvalho - 2026 ##################################################################################################


from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

## Full RAG System usando Sparse Retrieval + Reranker
def precision_sparse_system (sparse_retrieval_obj, dataset, path: str, k: int):

    cross_encoder_tokenizer = AutoTokenizer.from_pretrained (path)
    cross_encoder_model = AutoModelForSequenceClassification.from_pretrained (path)

    eval = []

    cross_encoder_model.eval()
    for dados in dataset:
        
        query = dados ["query"]
        gold_ids = set (dados ["chunk_id"])

        sparse_retrieval = sparse_retrieval_obj.invoke (query)

        query_reranker = [query] * len (sparse_retrieval)
        chunks = [c.page_content for c in sparse_retrieval]
        chunks_ids = [c.metadata["chunk_id"] for c in sparse_retrieval]

        pares = list(zip(query_reranker, chunks)) # [query, chunks]
        #print (pares)

        inputs = cross_encoder_tokenizer (pares, return_tensors = "pt", padding = True, truncation = True)
        #print (inputs)

        with torch.no_grad():
            logits = cross_encoder_model (**inputs).logits
            #print (logits)

        rerank = sorted(zip(chunks_ids, chunks, logits.tolist()), key = lambda x: x[2], reverse = True)

        final = [chunk_id for chunk_id, _, _ in rerank [:k]]

        retrieved_ids = set (final)

        equals = len (gold_ids.intersection (retrieved_ids))

        precision = equals / len (sparse_retrieval)

        eval.append (precision)

    return {
        f"(Sparse Retrieval + Reranker) Precision@{k}:": sum (eval) / len (eval)
    }


## Full RAG System usando Dense Retrieval + Reranker
def precision_dense_system (dense_retrieval_obj, dataset, path: str, k: int):

    cross_encoder_tokenizer = AutoTokenizer.from_pretrained (path)
    cross_encoder_model = AutoModelForSequenceClassification.from_pretrained (path)

    eval = []

    cross_encoder_model.eval()
    for dados in dataset:
        
        query = dados ["query"]
        gold_ids = set (dados ["chunk_id"])

        dense_retrieval = dense_retrieval_obj.invoke (query)

        query_reranker = [query] * len (dense_retrieval)
        chunks = [c.page_content for c in dense_retrieval]
        chunks_ids = [c.metadata["chunk_id"] for c in dense_retrieval]

        pares = list(zip(query_reranker, chunks)) # [query, chunks]
        #print (pares)

        inputs = cross_encoder_tokenizer (pares, return_tensors = "pt", padding = True, truncation = True)
        #print (inputs)

        with torch.no_grad():
            logits = cross_encoder_model (**inputs).logits
            #print (logits)

        rerank = sorted(zip(chunks_ids, chunks, logits.tolist()), key = lambda x: x[2], reverse = True)

        final = [chunk_id for chunk_id, _, _ in rerank [:k]]

        retrieved_ids = set (final)

        equals = len (gold_ids.intersection (retrieved_ids))

        precision = equals / len (dense_retrieval)

        eval.append (precision)

    return {
        f"(Dense Retrieval + Reranker) Precision@{k}:": sum (eval) / len (eval)
    }


## Full RAG System usando Hybrid Retrieval + Reranker
def precision_hybrid_system (sparse_retrieval_obj, dense_retrieval_obj, dataset, path: str, k: int):

    cross_encoder_tokenizer = AutoTokenizer.from_pretrained (path)
    cross_encoder_model = AutoModelForSequenceClassification.from_pretrained (path)

    eval = []

    cross_encoder_model.eval()
    for dados in dataset:
        
        query = dados ["query"]
        gold_ids = set (dados ["chunk_id"])

        sparse_retrieval = sparse_retrieval_obj.invoke (query)
        dense_retrieval = dense_retrieval_obj.invoke (query)

        rrf = Reciprocal_Rank_Fusion ([sparse_retrieval, dense_retrieval])

        query_reranker = [query] * len (rrf)
        chunks = [c[2] for c in rrf]
        chunks_ids = [c[1] for c in rrf]

        pares = list(zip(query_reranker, chunks)) # [query, chunks]
        #print (pares)

        inputs = cross_encoder_tokenizer (pares, return_tensors = "pt", padding = True, truncation = True)
        #print (inputs)

        with torch.no_grad():
            logits = cross_encoder_model (**inputs).logits
            #print (logits)

        rerank = sorted(zip(chunks_ids, chunks, logits.tolist()), key = lambda x: x[2], reverse = True)

        final = [chunk_id for chunk_id, _, _ in rerank [:k]]

        retrieved_ids = set (final)

        equals = len (gold_ids.intersection (retrieved_ids))

        precision = equals / len (rrf)

        eval.append (precision)

    return {
        f"(Hybrid Retrieval + Reranker) Precision@{k}:": sum (eval) / len (eval)
    }