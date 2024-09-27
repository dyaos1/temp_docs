import textwrap
from openai import OpenAI
from pydantic import BaseModel

class NovelIngredients(BaseModel):
    genre: str
    characters: list[dict[str, str]]
    news: str


def create_novel(prompt: str):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens= 1000,
        messages=[
            {
                "role": "system", 
                "content": "You are a promising novelist."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return completion.choices[0].message.content



def main():
    novel_ingredients = NovelIngredients(
        genre= "역사",
        characters=[
            {"홍길동": "재주가 비상한 주인공"},
            {"임꺽정": "거칠지만 심성은 착한 조연"},
            {"일지매": "아버지를 잃고 복수를 꿈꾸는 조연"}
        ],
        news=("""지상전 모의 훈련도 했다...이스라엘, 헤즈볼라 휴전 거부 배경은
이, 베이루트·가자지구 공습 이어가
양측 목표 뚜렷한 상황…휴전 난항
미국이 이스라엘과 레바논 무장정파 헤즈볼라 간 지상전을 막기 위해 임시 휴전안을 추진했지만 양측은 대규모 공습을 이어가며 오히려 전면전을 향해 치닫고 있다.
이스라엘은 심지어 지상전에 대비한 모의 훈련까지 실시했다. \
26일(현지시간) 뉴욕타임스(NYT)와 타임스오브이스라엘에 따르면 이스라엘은 레바논 동부 베카밸리, \
남부 접경지 등의 헤즈볼라 거점을 향해 대규모 폭격을 이어갔다.
특히 레바논 수도 베이루트 외곽 다히예 지역의 아파트 건물에 전투기로 미사일을 쏴 헤즈볼라의 \
무인기(드론) 지휘관 무함마드 후세인 사루르를 살해했다. \
레바논 보건부는 이스라엘의 공습으로 이날 하루에만 92명이 사망하고 150명이 부상당했다고 밝혔다.
같은 날 이스라엘은 팔레스타인 가자지구에도 폭격을 가했다. \
가자 북부 한 학교를 향해 미사일을 발사해 어린이를 포함해 사망자 15명이 발생했다. 팔레스타인 민방위 당국은 \
이스라엘 공습으로 학교 폭격을 포함해 해당 지역에 35명이 사망했다고 전했다.
헤즈볼라도 이스라엘 북부로 로켓 약 100기를 발사했다."""))


    with open('./prompt_template.txt', 'r') as f:
        template = f.read()

    prompt = template.format(
        genre=novel_ingredients.genre,
        characters=novel_ingredients.characters,
        news=novel_ingredients.news
    )

    novel = create_novel(prompt)
    print(novel)

main()