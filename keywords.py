from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os
import dotenv
from emotion_explanation import get_emotion_explanation
import json

def get_keywords(emotions: json):
    dotenv.load_dotenv()

    model = ChatGoogleGenerativeAI(model="gemini-flash-latest",
                                   google_api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
            당신은 Spotify Search API(q 파라미터)를 위한 음악 검색 키워드 생성 전문가입니다.

            **입력**: 감정 분석 결과 JSON (dominant_emotion, emotion_summary, recommended_actions 포함)
            
            **생성 규칙**:
            1. **세 가지 정보 모두 종합 분석**
               - dominant_emotion: 핵심 감정 파악
               - emotion_summary: 현재 심리 상태 이해
               - recommended_actions: 음악의 역할 도출 (위로/안정/휴식/기분전환/힐링 등)
            
            2. **키워드 형식**
               - 정확히 3개의 한글 키워드
               - 쉼표(,)로 구분된 한 줄 문자열
               - Spotify 검색에 최적화된 형태
            
            3. **키워드 구성 요소** (자유 조합)
               - 분위기: 잔잔한, 차분한, 감성적인, 따뜻한, 경쾌한, 밝은
               - 감정: 위로, 힐링, 평온, 설렘, 행복, 신남
               - 장르: 발라드, 인디, 어쿠스틱, 재즈, 팝, 댄스
               - 템포/스타일: 느린, 경쾌한, 부드러운, 신나는
            
            4. **플레이리스트 제목**
               - 사용자의 감정 상태와 음악의 역할을 반영한 제목
               - 간결하고 공감 가능한 한글 제목 (10자 내외)
               - 예: "마음을 다독이는 시간", "조용한 위로"
            
            5. **금지 사항**
               - 완전한 문장, 가사 형태
               - 조사(은/는/이/가) 사용
               - 아티스트명, 곡 제목
               - 따옴표, JSON, 추가 설명 텍스트
            
            **출력 형식**:
            키워드: [키워드1, 키워드2, 키워드3]
            제목: [플레이리스트 제목]
            
            **입력 예시**:
            {{
              "dominant_emotion": "기쁨",
              "emotion_summary": "기분이 좋고 에너지가 넘치는 상태입니다.",
              "recommended_actions": ["활기찬 활동하기", "친구들과 시간 보내기", "신나는 음악 듣기"]
            }}
            
            **출력 예시**:
            키워드: 신나는 팝, 경쾌한 댄스, 행복 인디
            제목: 기분 좋은 하루

    """),

        ("human", "{emotions}"),
    ])

    chain = prompt | model

    resp = chain.invoke({"emotions": emotions})

    return resp.content

if __name__ == "__main__":
    emotion=get_emotion_explanation()
    print("Emotion Explanation JSON:", emotion)
    keywords = get_keywords(emotion)
    print("Generated Keywords JSON:", keywords)