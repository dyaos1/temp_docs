from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    max_tokens= 1000,
    messages=[
        {
            "role": "system", 
            "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "이순신이 참여한 해전 중에 가장 유명한 것은 뭐야? 짧게 대답해줘."
        }
    ]
)

print(completion.choices[0].message)