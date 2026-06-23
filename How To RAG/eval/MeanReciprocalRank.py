######################################################################################## Eliezer Carvalho - 2026 ##################################################################################################

#Quando uma Query é enviada pelo utilizador, num sistema RAG híbrido é realizada uma Procura Lexical e uma ou várias Procuras Vetoriais.
#Cada mecanismo gera a sua própria lista ordenada de resultados. É por norma utilizado o algoritmo Reciprocal Rank Fusion (RRF) para mergir estas listas numa única classificação final.
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

#Estas funções têm como objetivo medir a métrica MRR (Mean Reciprocal Rank) de um sistema RAG Híbrido tendo em conta tanto o documento ideal e o chunk ideal.
#MRR é uma métrica que tem em peso as posições dos documentos ou chunks. Esta métrica tem em vista calcular o quão cedo o documento ou chunk ideal aparece.

## Sparse Retrieval - BM25 Retriever
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

    return {
        "Mean Reciprocal Rank Chunk Sparse Retrieval": sum(mrr_chunks) / len(mrr_chunks),
        "Mean Reciprocal Rank Docs Sparse Retrieval": sum(mrr_docs) / len(mrr_docs)
    }
    
        
## Dense Retrieval - Embeddings Retriever
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

    return {
        "Mean Reciprocal Rank Chunks Dense Retrieval": sum(mrr_chunks) / len(mrr_chunks),
        "Mean Reciprocal Rank Docs Dense Retrieval": sum(mrr_docs) / len(mrr_docs)
    }
    
         

## Hybrid Retrieval com Reciprocal Rank Fusion
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

    return {
        "Mean Reciprocal Rank Chunks Hybrid Retrieval": sum(mrr_chunks) / len(mrr_chunks),
        "Mean Reciprocal Rank Docs Hybrid Retrieval": sum(mrr_docs) / len(mrr_docs)
    }


######################################################################################## Eliezer Carvalho - 2026 ##################################################################################################
#Estas funções têm como objetivo avaliar o sistema RAG final. Retrieval -> Rerank
#Usa-se a métrica MRR porque o Reranker mexe diretamente com a posição dos chunks antes de ser enviado para o LLM.

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

#Mean Reciprocal Rank num Sistema [Sparse Retrieval - Reranker]
def mrr_ranker_sparse_system (sparse_retrieval_obj, dataset):
    
    path = r"C:\Users\Admin\Desktop\models\Cross Encoder"

    cross_encoder_model = AutoModelForSequenceClassification.from_pretrained (path)
    cross_encoder_model_tokenization = AutoTokenizer.from_pretrained (path)

    mrr_chunks = []
    mrr_docs = []

    for dados in dataset:

        query = dados["query"]
        gold_chunk = dados["chunk_id"]
        gold_doc = dados["doc"]

        sparse_retrieval = sparse_retrieval_obj.invoke (query)

        query_reranker = [query] * len (sparse_retrieval)
        chunks = [c.page_content for c in sparse_retrieval]
        docs_names = [d.metadata["title"] for d in sparse_retrieval]
        chunks_ids = [c.metadata["chunk_id"] for c in sparse_retrieval]

        pares = list(zip(query_reranker, chunks)) # [query, chunks]
        #print (pares)

        inputs = cross_encoder_model_tokenization (pares, return_tensors = "pt", padding = True, truncation = True)
        #print (inputs)

        cross_encoder_model.eval()
        with torch.no_grad():
            logits = cross_encoder_model (**inputs).logits
            #print (logits)

        #Organiza os logits com os chunks correspondentes #Muita Atenção! Para calcular HitRate e MRR com as funções criadas é necessário estar no mesmo formato do output do RRF.
        rerank = sorted(zip(docs_names, chunks_ids, chunks, logits.tolist()), key = lambda x: x[3], reverse = True)

        final = [(docs, chunks) for docs, chunks, chunks_content, scores in rerank [:5]]

        rr_chunk = 0
        rr_docs = 0

        for ordem, (doc_name, chunk_id) in enumerate (final, start = 1):
            
            if rr_chunk == 0 and chunk_id == gold_chunk:
                rr_chunk = 1 / ordem

            if rr_docs == 0 and doc_name == gold_doc:
                rr_docs = 1 / ordem

            if rr_chunk and rr_docs:
                break

        mrr_chunks.append (rr_chunk)
        mrr_docs.append (rr_docs)   

    return {
        "Mean Reciprocal Rank Chunks Rerank": sum(mrr_chunks) / len(mrr_chunks),
        "Mean Reciprocal Rank Docs Rerank": sum(mrr_docs) / len(mrr_docs)
    }


#Mean Reciprocal Rank num Sistema [Dense Retrieval - Reranker]
def mrr_ranker_dense_system (dense_retrieval_obj, dataset):
    
    #Pouco eficiente estar sempre a dar load do modelo mas vamos prosseguir assim
    path = r"C:\Users\Admin\Desktop\models\Cross Encoder"

    cross_encoder_model = AutoModelForSequenceClassification.from_pretrained (path)
    cross_encoder_model_tokenization = AutoTokenizer.from_pretrained (path)

    mrr_chunks = []
    mrr_docs = []

    for dados in dataset:

        query = dados["query"]
        gold_chunk = dados["chunk_id"]
        gold_doc = dados["doc"]

        dense_retrieval = dense_retrieval_obj.invoke (query)

        query_reranker = [query] * len (dense_retrieval)
        chunks = [c.page_content for c in dense_retrieval]
        docs_names = [d.metadata["title"] for d in dense_retrieval]
        chunks_ids = [c.metadata["chunk_id"] for c in dense_retrieval]

        pares = list(zip(query_reranker, chunks)) # [query, chunks]
        #print (pares)

        inputs = cross_encoder_model_tokenization (pares, return_tensors = "pt", padding = True, truncation = True)
        #print (inputs)

        cross_encoder_model.eval()
        with torch.no_grad():
            logits = cross_encoder_model (**inputs).logits
            #print (logits)

        #Organiza os logits com os chunks correspondentes #Muita Atenção! Para calcular HitRate e MRR com as funções criadas é necessário estar no mesmo formato do output do RRF.
        rerank = sorted(zip(docs_names, chunks_ids, chunks, logits.tolist()), key = lambda x: x[3], reverse = True)

        final = [(docs, chunks) for docs, chunks, chunks_content, scores in rerank [:5]]

        rr_chunk = 0
        rr_docs = 0

        for ordem, (doc_name, chunk_id) in enumerate (final, start = 1):
            
            if rr_chunk == 0 and chunk_id == gold_chunk:
                rr_chunk = 1 / ordem

            if rr_docs == 0 and doc_name == gold_doc:
                rr_docs = 1 / ordem

            if rr_chunk and rr_docs:
                break

        mrr_chunks.append (rr_chunk)
        mrr_docs.append (rr_docs)   

    return {
        "Mean Reciprocal Rank Chunks Rerank": sum(mrr_chunks) / len(mrr_chunks),
        "Mean Reciprocal Rank Docs Rerank": sum(mrr_docs) / len(mrr_docs)
    }


#Mean Reciprocal Rank num Sistema [Hybrid Retrieval - Reranker]
def mrr_ranker_hybrid_system (sparse_retrieval_obj, dense_retrieval_obj, dataset):

    path = r"C:\Users\Admin\Desktop\models\Cross Encoder"

    cross_encoder_model = AutoModelForSequenceClassification.from_pretrained (path)
    cross_encoder_model_tokenization = AutoTokenizer.from_pretrained (path)

    mrr_chunks = []
    mrr_docs = []

    for dados in dataset:

        query = dados["query"]
        gold_chunk = dados["chunk_id"]
        gold_doc = dados["doc"]

        sparse_retrieval = sparse_retrieval_obj.invoke (query)
        dense_retrieval = dense_retrieval_obj.invoke (query)

        rrf = Reciprocal_Rank_Fusion ([sparse_retrieval, dense_retrieval])

        query_reranker = [query] * len (rrf)
        chunks = [t[2] for t in rrf]
        docs_names = [t[0] for t in rrf]
        chunks_ids = [t[1] for t in rrf]

        pares = list(zip(query_reranker, chunks)) # [query, chunks]
        #print (pares)

        inputs = cross_encoder_model_tokenization (pares, return_tensors = "pt", padding = True, truncation = True)
        #print (inputs)

        cross_encoder_model.eval()
        with torch.no_grad():
            logits = cross_encoder_model (**inputs).logits
            #print (logits)

        #Organiza os logits com os chunks correspondentes #Muita Atenção! Para calcular HitRate e MRR com as funções criadas é necessário estar no mesmo formato do output do RRF.
        rerank = sorted(zip(docs_names, chunks_ids, chunks, logits.tolist()), key = lambda x: x[3], reverse = True)

        final = [(docs, chunks) for docs, chunks, chunks_content, scores in rerank [:5]]

        rr_chunk = 0
        rr_docs = 0

        for ordem, (doc_name, chunk_id) in enumerate (final, start = 1):
            
            if rr_chunk == 0 and chunk_id == gold_chunk:
                rr_chunk = 1 / ordem

            if rr_docs == 0 and doc_name == gold_doc:
                rr_docs = 1 / ordem

            if rr_chunk and rr_docs:
                break

        mrr_chunks.append (rr_chunk)
        mrr_docs.append (rr_docs)   

    return {
        "Mean Reciprocal Rank Chunks Rerank": sum(mrr_chunks) / len(mrr_chunks),
        "Mean Reciprocal Rank Docs Rerank": sum(mrr_docs) / len(mrr_docs)
    }