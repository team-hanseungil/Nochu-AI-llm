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
        
    """),

        ("human", "{emotion}"),
    ])

    chain = prompt | model

    resp = chain.invoke({"emotion": "슬픔"})

    return resp.content


if __name__ == "__main__":
    keywords = get_keywords()
    print("Generated Keywords JSON:", keywords)