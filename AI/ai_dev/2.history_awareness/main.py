from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import json


model = ChatOpenAI(model="gpt-4o-mini")


with open("./conversation.json", "r") as f:
    json_data = json.load(f)

messages = json_data["messages"]

chatbot_messages = []

for message in messages:
    for k in message.keys():
        key = k
        break
    val = message[key]

    if key == "ai":
        chatbot_messages.append(AIMessage(content = val))
    elif key == "client":
        chatbot_messages.append(HumanMessage(content = val))
    else:
        pass


chatbot_messages.append(
    HumanMessage(content="방금 나눈 대화들을 요약해줘.")
)


result = model.invoke(
    chatbot_messages
)

print(result)