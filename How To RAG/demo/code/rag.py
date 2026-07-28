from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title

from pathlib import Path

import tempfile

from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever #Sparse Retrieval
from langchain_huggingface import HuggingFaceEmbeddings #Dense Retrieval
from langchain_community.vectorstores import FAISS

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"




###
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
###


def PARSING_CHUNKING (files):

    documentos = []
    chunk_id = 1

    # Necessário guardar temporariamente o pdf porque o streamlit não retorna texto, apenas um objeto
    for file in files:
        with tempfile.NamedTemporaryFile (suffix = ".pdf", delete = False) as tmp:
            
            tmp.write (file.getbuffer())
            tmp.flush()
            caminho = tmp.name
            #print (caminho)
    #-------------------------------------------------------------------

        parser = partition_pdf (str(caminho), languages = ["por"])
        chunks = chunk_by_title (parser[3:], max_characters = 750)

        for chunk in chunks:

            documentos.append (
                Document (
                    page_content = chunk.text,
                    metadata = {
                        "title": file.name,
                        "chunk_id": chunk_id
                    }
                )
            )

            chunk_id += 1

    return (documentos)


def RETRIEVALS (documentos):

    #SPARSE RETRIEVAL - PROCURA LEXICAL
    SPARSE_RETRIEVAL = BM25Retriever.from_documents (documentos, k = 20)

    #DENSE RETRIEVAL - PROCURA SEMÂNTICA
    BI_ENCODER = HuggingFaceEmbeddings (model_name = r"C:\Users\Admin\Desktop\models\Bi Encoder - Jina")
    DATABASE = FAISS.from_documents (documentos, BI_ENCODER)
    DENSE_RETRIEVAL = DATABASE.as_retriever (search_type = "similarity", search_kwargs = {"k": 20})

    return SPARSE_RETRIEVAL, DENSE_RETRIEVAL


def CROSS_ENCODER ():

    CROSS_ENCODER_TOKENIZER = AutoTokenizer.from_pretrained (r"C:\Users\Admin\Desktop\models\Cross Encoder - BAAIbge-reranker-v2-m3")
    CROSS_ENCODER_MODEL = AutoModelForSequenceClassification.from_pretrained (r"C:\Users\Admin\Desktop\models\Cross Encoder - BAAIbge-reranker-v2-m3", device_map = device)

    return CROSS_ENCODER_TOKENIZER, CROSS_ENCODER_MODEL



def RAG (query, files):

    documentos = PARSING_CHUNKING (files)

    SPARSE_RETRIEVAL, DENSE_RETRIEVAL = RETRIEVALS (documentos)

    LEXICAL = SPARSE_RETRIEVAL.invoke (query)
    SEMANTIC = DENSE_RETRIEVAL.invoke (query)

    HYBRID_RETRIEVAL = Reciprocal_Rank_Fusion ([LEXICAL, SEMANTIC])

    # Preparação dos dados que saem do RRF para Cross Encoder
    query_reranker = [query] * len(HYBRID_RETRIEVAL)
    chunks = [c[2] for c in HYBRID_RETRIEVAL]

    # Construção de pares [query -> chunk]
    pares = list(zip(query_reranker, chunks))

    #Cross Encoder Model

    CROSS_ENCODER_TOKENIZER, CROSS_ENCODER_MODEL = CROSS_ENCODER ()

    inputs = CROSS_ENCODER_TOKENIZER (pares, return_tensors = "pt", padding = True, truncation = True).to(device)

    with torch.no_grad():
        logits = CROSS_ENCODER_MODEL (**inputs).logits

    rerank = sorted(zip(chunks, logits.tolist()), key = lambda x: x[1], reverse = True)

    feed_llm = [chunks for chunks, scores in rerank [:8]]

    return feed_llm