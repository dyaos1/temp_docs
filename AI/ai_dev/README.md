# ai dev

### 설치

```
pip install langchain langchain-openai langchain-chroma chromadb
```

### 1.BASIC

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

model = ChatOpenAI(model="gpt-4o-mini")

messages = [
    SystemMessage(content="Translate the following into English"),
    HumanMessage(content="사람은 바로 서야 합니다."),
]

result = model.invoke(messages)

print(result)
```

간단하다. model 인스턴스를 생성하고, 메시지에 SystemMessage, HumanMessage 를 집어 넣은 후에, invoke 메서드로 결과를 불려오면 된다.


### 2.History Awareness

원래 api를 이용한 질문 답변은 ai 가 이전에 했던 대화를 기억하지 못한다.

하지만 invoke 메서드가 list를 받기 때문에, 
이전에 ai 와 나누었던 대화를 list로 넣으면
대화의 맥락을 기억할 수 있게 된다.

```python
messages = [
    HumanMessage(content="Hi! I'm Bob"),
    AIMessage(content="Hello Bob! How can I assist you today?"),
    HumanMessage(content="What's my name?"),
]
```

위의 예시처럼 주고받는 대화를 넣어서 그 맥락을 토대로 질문을 하면 답변을 제대로 한다.

개발을 할 때에는 frontend의 채팅 대화 리스트를 전달 받는 식으로 하거나
아니면 cache에 이전 대화들을 넣어서 전달하는 식으로 개발한다.



### 3. RAG

 - 문자열 자르기

```python
loader = TextLoader("./state_of_union.txt")
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
all_splits = text_splitter.split_documents(data)
```

vector database에 저장할때 문서 전체를 통으로 저장할 수 없다. 
보통은 1000~2000 자 정도로 잘라서 넣게 된다.

잘라서 넣게 되면 단어가 중간에 끊어져서 무슨 뜻인지 알게 되지 못하는 경우가 생기므로,
chunk_overlap에 겹침 정도를 부여해서 약간 중복되게 자른다.



- 임베딩

위에서 자른 문서를 벡터DB에 넣기 전에 먼저 임베딩 로직을 이용해서 문서를 벡터값으로 바꾸어야 한다.

```python
openai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(documents=all_splits, embedding=openai_embeddings)
```

벡터로 저장한 내용을 유사성 검색으로 찾는 인스턴스를 만든다.
```python
retriever = vectorstore.as_retriever(search_type="similarity")
```


- 프롬프트 엔지니어링

위에서 긴 문장을 잘라서 임베딩해서 벡터DB에 보관하고,
질문에 따라 비슷한 내용을 찾는 기능까지 만들었다.

이제 찾은 내용을 바탕으로 프롬프트 엔지니어링을 하면 된다.

원리는 매우간단하다.
프롬프트를 만들어 모델과 더하고 위에서 만든 retriever 인스턴스를 합치면 결과가 나온다.

```python
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
```



### 4. vector db

조금전까지 RAG 를 만드는 예제를 했는데, vector db를 본격적으로 쓰지 않았다.

왜냐하면 텍스트를 불러와서 vector db에 저장했다기 보다는, 
vector db의 인스턴스를 만들어서 처리했기 때문이다.

즉 읽어들인 문서를 vector db의 로직만 빌려와서 인스턴스로 만들었을 뿐이기 때문에,
대용량의 문서를 메모리가 아닌 db에 저장해놓고 쓴 방식이 아니다.

여기서는 db에 저장하는 방식을 설명하겠다.

 - chroma_client

클라이언트를 생성하고,
OpenAI 임베딩 함수를 설정하고,
컬렉션을 생성한다.

```python
API_KEY = os.environ["OPENAI_API_KEY"]

vdb_client = chromadb.PersistentClient(path="./", settings=Settings(allow_reset=True))
vdb_client.reset()

ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=API_KEY,
        model_name="text-embedding-3-small"
    )

collection = vdb_client.get_or_create_collection(name="state_of_union", embedding_function=ef)
```


- 텍스트 스플릿

이전에 연습했던 텍스트 스플릿을 한다.

```python

loader = TextLoader("./state_of_union.txt")
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
all_splits = (text_splitter.split_documents(data))
```

- 컬렉션에 스플릿된 텍스트를 업데이트 한다.

문서의 내용, 메타데이터, 인덱스를 각각 list를 만들어, 컬렉션에 추가한다.

```python
documents = []
metadatas = []
ids = []

for idx, content in enumerate(all_splits):
    documents.append(content.page_content)
    metadatas.append(content.metadata)
    ids.append("id-"+str(idx))


collection.upsert(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)
```

- 테스트
```python
results = collection.query(
    query_texts=["내용 중 의료 복지에 관련된 내용을 설명해줘"],
    n_results=2
)

print(results)
```

쿼리를 날려서 검색이 잘 되는지 확인한다.


### 끝으로

이상으로 
1. ai개발의 기본
2. ai에게 지난 대화 인식시키기 
3. 벡터DB로부터 불러온 내용으로 ai답변 생성하기(RAG)
4. 벡터DB에 저장하기
까지 알아보았다.

이상의 기술들을 조합하면 chatbot을 만들 수 있다.

하지만 ai에 집중하기 이전에 자문해 보기 바란다. 채팅앱을 만들 수는 있는지

ai기술에 기반한 어플리케이션에 있어서 중요한 것은 ai 기술 그 자체가 아니라,
바로 어플리케이션을 만드는 기술이다.
