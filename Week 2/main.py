

from llama_index.core import VectorStoreIndex
from llama_index.core import SimpleDirectoryReader
from llama_index.core import Settings

from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# LLM
llm = LlamaCPP(
    model_path = r"C:\Users\eliez\Desktop\Modelos\ggml-model-Q4_K.gguf",
    temperature = 0.1,
    max_new_tokens = 256,
    context_window = 4096,
)

# LOCAL EMBEDDINGS
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

# documentos
documents = SimpleDirectoryReader(
    input_files=[
        r"C:\Users\eliez\Desktop\ria\Neuro-Flap\Neuro Flap.pdf"
    ]
).load_data()

# índice
index = VectorStoreIndex.from_documents(
    documents
)

query_engine = index.as_query_engine(
    llm=llm
)

response = query_engine.query(
    "Resume este documento"
)

print(response)