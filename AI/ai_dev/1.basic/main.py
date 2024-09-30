from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

model = ChatOpenAI(model="gpt-4o-mini")

messages = [
    SystemMessage(content="Translate the following into English"),
    HumanMessage(content="사람은 바로 서야 합니다."),
]

result = model.invoke(messages)

print(result)