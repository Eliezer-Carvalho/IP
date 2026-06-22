######################################################################################## Eliezer Carvalho - 2026 ##################################################################################################

#Quando uma Query é enviada pelo utilizador, num sistema RAG híbrido é realizada uma Procura Lexical e uma ou várias Procuras Vetoriais.
#Cada mecanismo gera a sua própria lista ordenada de resultados. É por norma utilizado o algoritmo Reciprocal Rank Fusion (RRF) para mergir estas listas numa única classificação final.
#https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def Reciprocal_Rank_Fusion (rankings, k = 60): 
    
    scores = {}
    metadata = {}

    for ranking in rankings:
        for rank, doc in enumerate(ranking):

            doc_id = doc.metadata["chunk_id"]

            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)

            metadata[doc_id] = {
                "title": doc.metadata.get("title"),
                "content": doc.page_content
            }

    ranked = sorted(scores.items(), key = lambda x: x[1], reverse = True)

    return [(metadata[doc_id]["title"], doc_id, metadata[doc_id]["content"], score)
        for doc_id, score in ranked
    ]

######################################################################################## Eliezer Carvalho - 2026 ##################################################################################################

#Estas funções têm como objetivo medir a métrica HitRate@K de um sistema RAG Híbrido tendo em conta tanto o documento ideal e o chunk ideal.
#HitRate@K é uma métrica binária. Retorna 1 caso encontre o documento ou chunk onde está contida a resposta à query. Retorna 0 caso contrário.

## Sparse Retrieval - BM25 Retriever
def hitrate_k_sparse_retrieval (sparse_retrieval_obj, dataset): #Recebe um obj que já tem em conta o K do Sparse Retrieval.

    eval_chunks = []
    eval_docs = []

    for dados in dataset:
        
        query = dados["query"] #Muda consoante o dataset
        gold_chunk = dados["chunk_id"] #Muda consoante o dataset
        gold_doc = dados["doc"] #Muda consoante o dataset

        sparse_retrieval = sparse_retrieval_obj.invoke (query)

        chunk_hit = 0
        docs_hit = 0

        for chunks in sparse_retrieval:

            if chunks.metadata["chunk_id"] == gold_chunk:
                chunk_hit = 1
                
            if chunks.metadata["title"] == gold_doc:
                docs_hit = 1
            
            if chunk_hit and docs_hit:
                break

        eval_chunks.append (chunk_hit)
        eval_docs.append (docs_hit)

    return {
        "HitRate@K Chunk Sparse Retrieval": {sum(eval_chunks) / len(eval_chunks)},
        "HitRate@K Docs Sparse Retrieval": {sum(eval_docs) / len(eval_docs)}
    }


## Dense Retrieval - Embeddings Retriever
def hitrate_k_dense_retrieval (dense_retrieval_obj, dataset):

    eval_chunks = []
    eval_docs = []

    for dados in dataset:

        query = dados["query"]
        gold_chunk = dados["chunk_id"]
        gold_doc = dados["doc"]

        dense_retrieval = dense_retrieval_obj.invoke (query)

        chunk_hit = 0
        docs_hit = 0

        for chunks in dense_retrieval:

            if chunks.metadata["chunk_id"] == gold_chunk:
                chunk_hit = 1
            
            if chunks.metadata["title"] == gold_doc:
                docs_hit = 1

            if chunk_hit and docs_hit:
                break
               

        eval_chunks.append (chunk_hit)
        eval_docs.append (docs_hit)

    return {
        "HitRate@K Chunk Dense Retrieval": {sum(eval_chunks) / len(eval_chunks)},
        "HitRate@K Docs Dense Retrieval": {sum(eval_docs) / len(eval_docs)}
    }


## Hybrid Retrieval com Reciprocal Rank Fusion
def hitrate_k_hybrid_retrieval (sparse_retrieval_obj, dense_retrieval_obj, dataset):

    eval_chunks = []
    eval_docs = []

    for dados in dataset:

        query = dados["query"]
        gold_chunk = dados["chunk_id"]
        gold_doc = dados["doc"]

        sparse_retrieval = sparse_retrieval_obj.invoke (query)
        dense_retrieval = dense_retrieval_obj.invoke (query)

        recrankf = Reciprocal_Rank_Fusion ([sparse_retrieval, dense_retrieval])

        chunk_hit = 0
        docs_hit = 0

        for chunks in recrankf:

            if chunks[1] == gold_chunk:
                chunk_hit = 1
            
            if chunks[0] == gold_doc:
                docs_hit = 1

            if chunk_hit and docs_hit:
                break
               

        eval_chunks.append (chunk_hit)
        eval_docs.append (docs_hit)

    return {
        "HitRate@K Chunk Hybrid Retrieval": {sum(eval_chunks) / len(eval_chunks)},
        "HitRate@K Docs Hybrid Retrieval": {sum(eval_docs) / len(eval_docs)}
    }
