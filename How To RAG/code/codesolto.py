'''from sentence_transformers import SentenceTransformer

name = "jinaai/jina-embeddings-v5-text-small-retrieval"

model = SentenceTransformer (name)

model.save (r"C:\Users\Admin\Desktop\models\Jina")'''

#------------------------------------------------------------------------------
##Cross Encoder 
'''query_reranker = [query] * len (teste)
chunks = [t[2] for t in teste]
docs_names = [t[0] for t in teste]
chunks_ids = [t[1] for t in teste]

pares = list(zip(query_reranker, chunks)) # [query, chunks]
#print (pares)

inputs = cross_encoder_model_tokenization (pares, return_tensors = "pt", padding = True, truncation = True)
#print (inputs)

cross_encoder_model.eval()
with torch.no_grad():
    logits = cross_encoder_model (**inputs).logits
    #print (logits)

#Organiza os logits com os chunks correspondentes #Muita Atenção! Para calcular HitRate e MRR com as funções criadas é necessário estar no mesmo formato do output do RRF.
rerank = sorted(zip(docs_names, chunks_ids, chunks, logits.tolist()), key = lambda x: x[3], reverse = True) #x[3] define que arg é usado pelo reverse

#display (rerank)
'''

#------------------------------------------------------------------------------
'''from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model = AutoModelForSequenceClassification.from_pretrained ("BAAI/bge-reranker-v2-m3")
tokenizer = AutoTokenizer.from_pretrained ("BAAI/bge-reranker-v2-m3")

model.save_pretrained (r"C:\Users\Admin\Desktop\models\Cross Encoder")
tokenizer.save_pretrained (r"C:\Users\Admin\Desktop\models\Cross Encoder")'''


#------------------------------------------------------------------------------
'''device = "cuda" if torch.cuda.is_available() else "cpu"

print (device)
print (torch.__version__)
print (torch.version.cuda)'''


#------------------------------------------------------------------------------
'''from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model = AutoModelForCausalLM.from_pretrained ("mistralai/Mistral-7B-Instruct-v0.3")
tokenization = AutoTokenizer.from_pretrained ("mistralai/Mistral-7B-Instruct-v0.3")

model.save_pretrained (r"C:\Users\Admin\Desktop\models\Mistral-7B-Instruct-v0.3")
tokenization.save_pretrained (r"C:\Users\Admin\Desktop\models\Mistral-7B-Instruct-v0.3")
'''