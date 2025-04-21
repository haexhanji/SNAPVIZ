import streamlit as st
import google.generativeai as genai

# 🔐 Gemini API 키 설정
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# ✅ 페이지 설정
st.set_page_config(
    page_title="Ora.AI - 천주교 묵상 도우미",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ 묵상 생성 함수
def generate_meditation(verse_text):
    prompt = f"""
너는 천주교 영성가야. 아래 성경 구절에 대해 묵상 기도문을 작성해줘. 고요하고 은혜로운 말투로 써줘.

[성경 구절]
{verse_text}

[기도문]
"""
    response = model.generate_content(prompt)
    return response.text

# ✅ 주제어 기반 구절 추천 함수
def ai_recommend_verses(keyword):
    prompt = f"""
너는 천주교 성경 전문가야. '{keyword}'라는 주제와 관련된 대표적인 성경 구절 3개를 추천해줘.

각 구절은 다음 형식으로 정리해줘:

[책 이름] [장]:[절]
"본문"
"""
    response = model.generate_content(prompt)
    return response.text

# ✅ 앱 타이틀
st.title("🙏 Ora.AI - 천주교 기반 성경 묵상")
st.subheader("주제어로 관련 말씀을 추천받고, 묵상 기도문을 생성하세요")

# ✅ 키워드 입력
keyword = st.text_input("🔍 주제어를 입력하세요 (예: 사랑, 고통, 희망 등)")
if keyword:
    with st.spinner("Ora.AI가 성경 구절을 찾는 중..."):
        verses_text = ai_recommend_verses(keyword)
        st.markdown("🕯️ **추천 성경 구절**")
        st.markdown(verses_text)

        if st.button("🧎 묵상 기도문 생성하기"):
            with st.chat_message("assistant"):
                with st.spinner("Ora.AI가 묵상 기도 중..."):
                    meditation = generate_meditation(verses_text)
                    st.markdown("🕊️ **묵상 기도문**")
                    st.markdown(meditation)

                    st.download_button(
                        label="📥 묵상 기도문 저장하기",
                        data=meditation,
                        file_name="meditation.txt",
                        mime="text/plain"
                    )
