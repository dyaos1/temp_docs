from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


loader = TextLoader("./state_of_union.txt")
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
all_splits = text_splitter.split_documents(data)


openai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = Chroma.from_documents(documents=all_splits, embedding=openai_embeddings)

retriever = vectorstore.as_retriever(search_type="similarity")

retriever.invoke("")



prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise."
            "All answers must be in Korean." 
            "\n\n{context}"),
        ("human", "{input}"),
    ]
)


model = ChatOpenAI(model="gpt-4o-mini")

prompt_ai = create_stuff_documents_chain(model, prompt)
rag_ai = create_retrieval_chain(retriever, prompt_ai)

response = rag_ai.invoke({"input": "내용 중 의료 복지에 관련된 내용을 설명해줘"})
print(response["answer"])