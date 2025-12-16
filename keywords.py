from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import os
import dotenv


def get_keywords():
    dotenv.load_dotenv()

    model = ChatGoogleGenerativeAI(model="gemini-flash-latest",
                                   google_api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
    당신은 음악 추천을 위한 키워드 생성기입니다.

    입력으로 주어진 감정에 어울리는
    Spotify Search API(q 파라미터)에 바로 사용할 수 있는
    영어 검색 키워드 3개를 생성하세요.
    
    조건:
    - 키워드는 반드시 한글로 출력할 것
    - 각 키워드는 1~2단어의 짧은 표현
    - 장르, 분위기, 음악적 무드를 중심으로 선택
    - 설명이나 문장은 포함하지 말 것
    - 결과는 JSON 형식만 출력할 것
    """),

        ("human", "{emotion}"),
    ])

    chain = prompt | model

    resp = chain.invoke({"emotion": "슬픔"})

    return resp.content

if __name__ == "__main__":
    keywords = get_keywords()
    print("Generated Keywords JSON:", keywords)