from pathlib import Path
from unstructured.partition.auto import partition

from langchain_core.documents import Document #https://reference.langchain.com/python/langchain-core/documents/base/Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

path = Path (r"C:\Users\Admin\Desktop\ip\How To RAG\docs")

files = []
id = 0

for docs in path.iterdir():

    elements = partition (str(docs))

    for el in elements:
        files.append ({
                "id": f"{docs.name}_{id}",
                "text": el.text,
                "metadata": {
                    "source": docs.name,
                    "type": el.category,
                    "file_type": el.metadata.to_dict()["filetype"]
            }
        })

        id += 1

print (files)

'''
documents = [
    Document (
        page_content =
    )
]

'''