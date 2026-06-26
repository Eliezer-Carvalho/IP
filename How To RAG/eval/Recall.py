######################################################################################## Eliezer Carvalho - 2026 ##################################################################################################

#Quando uma Query é enviada pelo utilizador, num sistema RAG híbrido é realizada uma Procura Lexical e uma ou várias Procuras Vetoriais.
#Cada mecanismo gera a sua própria lista ordenada de resultados. É por norma utilizado o algoritmo Reciprocal Rank Fusion (RRF) para mergir estas listas numa única classificação final. 
#Retirando dups e tendo em conta os scores e se aparece em ambos os retrievals.
#https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking

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

#Recall@K é uma métrica que permite relacionar o número total de chunks relevantes recuperados pelo Retriver e o número total de chunks relevantes possíveis para cada query. 

## Sparse Retrieval - BM25 Retriever
def recall_k_sparse_retrieval (sparse_retrieval_obj, dataset):
    
    eval = [] #Lista de eval

    for dados in dataset: #Iter do dataset

        query = dados ["query"] #Query
        gold_chunks = set (dados ["chunk_id"]) #Gold Id Chunk

        sparse_retrieval = sparse_retrieval_obj.invoke (query) #Sparse Retrieval para cada query

        retrieved_ids = set (x.metadata["chunk_id"] for x in sparse_retrieval) #Iterar sobre os chunks ids return pelo sparse_retrieval

        equals = len (gold_chunks.intersection (retrieved_ids)) #Intersection muito importante porque permite comparar se há equals

        eval.append (equals / len (gold_chunks)) #Recall@K

    return {
        "Recall@K Sparse Retrieval:": sum (eval) / len (eval) 
    }
 


## Dense Retrieval - Embeddings Retriver
def recall_k_dense_retrieval (dense_retrieval_obj, dataset):

    eval = []

    for dados in dataset:

        query = dados["query"]
        gold_chunk = set (dados["chunk_id"])

        dense_retrieval = dense_retrieval_obj.invoke (query)

        retrieved_ids = set (x.metadata["chunk_id"] for x in dense_retrieval)

        equals = len (gold_chunk.intersection (retrieved_ids))

        eval.append (equals / len (gold_chunk))

    return {
        "Recall@K Dense Retrieval:": sum (eval) / len (eval)
    }



## Hybrid Retrieval com Reciprocal Rank Fusion
def recall_k_hybrid_retrieval (sparse_retrieval_obj, dense_retrieval_obj, dataset):
    
    eval = []

    for dados in dataset:

        query = dados["query"]
        gold_chunk = set (dados["chunk_id"])

        sparse_retrieval = sparse_retrieval_obj.invoke (query)
        dense_retrieval = dense_retrieval_obj.invoke (query)

        rrf = Reciprocal_Rank_Fusion ([sparse_retrieval, dense_retrieval])

        retrieved_ids = set (x[1] for x in rrf)

        equals = len (gold_chunk.intersection (retrieved_ids))

        eval.append (equals / len (gold_chunk))

    return {
        "Recall@K Hybrid Retrieval:": sum (eval) / len (eval)
    }