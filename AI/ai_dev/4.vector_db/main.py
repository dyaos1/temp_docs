import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import os


API_KEY = os.environ["OPENAI_API_KEY"]

vdb_client = chromadb.PersistentClient(path="./", settings=Settings(allow_reset=True))
vdb_client.reset()

ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=API_KEY,
        model_name="text-embedding-3-small"
    )

collection = vdb_client.get_or_create_collection(name="state_of_union", embedding_function=ef)


loader = TextLoader("./state_of_union.txt")
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
all_splits = (text_splitter.split_documents(data))


documents = []
metadatas = []
ids = []

for idx, content in enumerate(all_splits):
    documents.append(content.page_content)
    metadatas.append(content.metadata)
    ids.append("id-"+str(idx))


collection.upsert(
    documents=documents,
    ids=ids
)
results = collection.query(
    query_texts=["내용 중 의료 복지에 관련된 내용을 설명해줘"],
    n_results=2
)

print(results)