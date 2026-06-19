#################################### Eliezer Carvalho - 2026 ###########################################
###### Reciprocal Rank Fusion - método utilizado para juntar Sparse e Dense Retrieval numa avaliação só.
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

'''
Estas funções têm como objetivo avaliar a métrica Recall@K de um sistema RAG.
Funciona apenas para sistemas onde o número de documentos ideais é exatamente 1 por chunks.
O parâmetro K tem de ser antes definido.
'''


##### Sparse Retrieval - BM25 Retriever
def recall_k_sparse_retrieval (sparse_retrieval_obj, dataset):

    eval_chunks = []
    eval_docs = []

    for dados in dataset:
        
        query = dados["query"]
        gold_chunk = dados["chunk_id"]
        gold_doc = dados["doc"]

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


    print (f"Recall@K Chunk -> {sum(eval_chunks) / len(eval_chunks)}\nRecall@K Docs -> {sum(eval_docs) / len(eval_docs)}")




##### Dense Retrieval - Embeddings Retriever
def recall_k_dense_retrieval (dense_retrieval_obj, dataset):

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


    print (f"Recall@K Chunk -> {sum(eval_chunks) / len(eval_chunks)}\nRecall@K Docs -> {sum(eval_docs) / len(eval_docs)}") 




##### Hybrid Retrieval com Reciprocal Rank Fusion
def recall_k_hybrid_retrieval (sparse_retrieval_obj, dense_retrieval_obj, dataset):

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


    print (f"Recall@K Chunk -> {sum(eval_chunks) / len(eval_chunks)}\nRecall@K Docs -> {sum(eval_docs) / len(eval_docs)}") 
