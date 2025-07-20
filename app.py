import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# .env から環境変数を読み込み
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI LLM 設定
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo")

# -----------------------------
# LLMに問い合わせる関数
# -----------------------------
def get_expert_response(expert_type, user_input):
    # 専門家の種類ごとのシステムメッセージ
    expert_prompts = {
        "医師": "あなたは経験豊富な医師として、医学的見地からアドバイスしてください。",
        "経営コンサルタント": "あなたは敏腕経営コンサルタントとして、ビジネスの最適解を提案してください。",
        "歴史学者": "あなたは知識豊富な歴史学者として、歴史的な背景を踏まえて解説してください。"
    }

    system_message = expert_prompts.get(expert_type, "あなたは一般的なアドバイザーです。")

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_input)
    ]

    response = llm(messages)
    return response.content


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("専門家シミュレーター")
st.write("以下のフォームに質問内容を入力し、専門家の種類を選択して送信してください。")

# ラジオボタン（専門家の種類）
expert_type = st.radio(
    "相談したい専門家を選んでください：",
    ("医師", "経営コンサルタント", "歴史学者")
)

# テキスト入力
user_input = st.text_input("質問を入力してください：")

# 送信ボタン
if st.button("送信"):
    if user_input:
        with st.spinner('専門家が考え中...'):
            answer = get_expert_response(expert_type, user_input)
        st.success("専門家の回答：")
        st.write(answer)
    else:
        st.warning("質問内容を入力してください。")
