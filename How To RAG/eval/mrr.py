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
Estas funções têm como objetivo avaliar a métrica Mean Reciprocal Rank de um sistema RAG.
'''

##### Sparse Retrieval - BM25 Retriever
def mrr_sparse_retrieval (sparse_retrieval_obj, dataset):

    mrr_chunks = []
    mrr_docs = []

    for dados in dataset:

        query = dados["query"]
        gold_chunk = dados["chunk_id"]
        gold_doc = dados["doc"]

        sparse_retrieval = sparse_retrieval_obj.invoke (query)

        rr_chunk = 0
        rr_docs = 0

        for ordem, doc in enumerate (sparse_retrieval, start = 1):
            
            if rr_chunk == 0 and doc.metadata["chunk_id"] == gold_chunk:
                rr_chunk = 1 / ordem

            if rr_docs == 0 and doc.metadata["title"] == gold_doc:
                rr_docs = 1 / ordem

            if rr_chunk and rr_docs:
                break

        mrr_chunks.append (rr_chunk)
        mrr_docs.append (rr_docs)   

    print (f"MRR Chunk -> {sum(mrr_chunks) / len(mrr_chunks)}\nMRR Docs -> {sum(mrr_docs) / len(mrr_docs)}")
         


##### Dense Retrieval - Embeddings Retriever
def mrr_dense_retrieval (dense_retrieval_obj, dataset):

    mrr_chunks = []
    mrr_docs = []

    for dados in dataset:

        query = dados["query"]
        gold_chunk = dados["chunk_id"]
        gold_doc = dados["doc"]

        dense_retrieval = dense_retrieval_obj.invoke (query)

        rr_chunk = 0
        rr_docs = 0

        for ordem, doc in enumerate (dense_retrieval, start = 1):
            
            if rr_chunk == 0 and doc.metadata["chunk_id"] == gold_chunk:
                rr_chunk = 1 / ordem

            if rr_docs == 0 and doc.metadata["title"] == gold_doc:
                rr_docs = 1 / ordem

            if rr_chunk and rr_docs:
                break

        mrr_chunks.append (rr_chunk)
        mrr_docs.append (rr_docs)   

    print (f"MRR Chunk -> {sum(mrr_chunks) / len(mrr_chunks)}\nMRR Docs -> {sum(mrr_docs) / len(mrr_docs)}")
         


##### Hybrid Retrieval com Reciprocal Rank Fusion
def mrr_hybrid_retrieval (sparse_retrieval_obj, dense_retrieval_obj, dataset):

    mrr_chunks = []
    mrr_docs = []

    for dados in dataset:

        query = dados["query"]
        gold_chunk = dados["chunk_id"]
        gold_doc = dados["doc"]

        sparse_retrieval = sparse_retrieval_obj.invoke (query)
        dense_retrieval = dense_retrieval_obj.invoke (query)

        recrankf = Reciprocal_Rank_Fusion ([sparse_retrieval, dense_retrieval])

        rr_chunk = 0
        rr_docs = 0

        for ordem, (doc_name, chunk_id, chunk_text, score) in enumerate (recrankf, start = 1):
            
            if rr_chunk == 0 and chunk_id == gold_chunk:
                rr_chunk = 1 / ordem

            if rr_docs == 0 and doc_name == gold_doc:
                rr_docs = 1 / ordem

            if rr_chunk and rr_docs:
                break

        mrr_chunks.append (rr_chunk)
        mrr_docs.append (rr_docs)   

    print (f"MRR Chunk -> {sum(mrr_chunks) / len(mrr_chunks)}\nMRR Docs -> {sum(mrr_docs) / len(mrr_docs)}")

