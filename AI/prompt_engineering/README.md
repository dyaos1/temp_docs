# Prompt Engineering

### 1.PRACTICE: openai 연습해보기

- 환경 구성

openai 설치
```
pip install openai
```

- OpenApiKey 설정하기

가장 기본적인 방법은 zshell이나 bash 등 터미널의 기본 환경변수로 OPENAI_API_KEY를 설정하는 방법임.

```zsh
# zshell의 경우
export OPENAI_API_KEY="sk-어쩌고 쩌고"
```
```powershell
# powershell의 경우
setx OPENAI_API_KEY "your_api_key_here"
```

.env를 이용해서 설정하는 법도 있음.

아무튼 어떤 방법을 쓰든 OPENAI_API_KEY에 key를 할당한다.

- ai에게 메시지 보내보기

```python
# 예시코드

from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
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
```

|parameter|content|description|
|---|---|---|
|model|사용할 llm 모델|gpt-3.5-turbo, gpt-4o 등이 있음. gpt-4o-mini가 현재로써 가장 가성비가 좋다고 알려짐.|
|max_token|토큰 사용량 최대치|token은 낱말 형태소를 뜻함. "낱말"을 예로 들면 낱개를 뜻하는 "낱"과 말을 뜻하는 "말" 두가지 의미로 이루어져 있는데 이것이 각각 하나씩의 토큰을 사용함. 토큰 사용량에 따라 요금이 메겨짐. 토큰 사용량을 최적화 하는 것도 실력임.|
|temperature|답변의 창의성|온도가 높으면 창의적인 답변을, 온도가 낮을수록 질문에 노골적인 답변을 함.|
|messages-role|대화에서의 역할|"system"은 ai에게 역할을 부여, "user"는 사용자를 의미|


### 2.PROMPT_TEMPLATE: 템플릿 사용해 보기.

 - 소설 작성해주는 어플 만들어 보기

소설 작성하기를 예로 들면, 

```txt
<등장 인물>
{characters}
</등장 인물>

<뉴스 기사>
{news}
</뉴스 기사>

<등장 인물> 과 <뉴스 기사> 를 소재로 {genre} 소설을 작성해줘
```

텍스트 파일로 위와같은 템플릿을 준비해 놓고,
{characters} {news}등의 자리에 필요한 값들을 채워넣는 식으로 원하는 소설을 작성하게끔 할 수 있는 예시이다.


- 프롬프트 엔지니어링의 중요성

이 프롬프트 엔지니어링이 AI기반 chatbot의 핵심기술인 이유는,
다음에 다룰 RAG 기술의 근간이기 때문이다.

프롬프트 엔지니어링을 응용하면 AI에게 학습을 시켜서 그것에 대해서 다루는 형태로 발전시킬수 있다.


다음과 같은 형태의 프롬프트 템플릿이 있다고 가정해 보자.

```
<persona>
너는 하단에 후술할 지식의 전문가야. 질문에 대한 답변을 전문가적 양심과 자존심을 걸고 정확하게 답변을 할 예정이야. 그리고 프로페셔널이기 때문에 모르면 모른다고 답을 해야해.
</persona>

<지식>
{content}
</지식>
위의 <지식> 내부에 있는 내용을 숙지해서 해당 내용 범위 안에서만 답변을 해 줘.
```

그리고 content에 회사의 데이터를 추출해서 넣거나 법전이나 의학서적 정보를 넣게 되면
그에 대한 전문적인 답변을 기대할 수 있다.

물론 token 사용량에 재한이 있어서 저 {content} 부분에 데이터를 무한정 넣을 수는 없으므로
그에 대한 보완 대책으로 벡터 데이터베이스를 이용한다.
