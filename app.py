import streamlit as st
import google.generativeai as genai
import json

# ✅ 페이지 설정
st.set_page_config(
    page_title="Ora.AI - 가톨릭 기도 도우미",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔐 Gemini API 키
genai.configure(api_key="AIzaSyC5VbRN66OLvUzNtbicw4KwtIUWdK08lLA")
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# ✅ 성경 데이터 로드
@st.cache_data
def load_bible():
    with open("bible_db.json", "r", encoding="utf-8") as f:
        return json.load(f)

bible_data = load_bible()

# ✅ 메뉴 고정
st.markdown(
    """
    <style>
    div[data-testid="stHeader"] {
        position: sticky;
        top: 0;
        z-index: 999;
        background-color: white;
        border-bottom: 1px solid #eaeaea;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ 상단 메뉴
menu = st.radio(
    "메뉴",
    ["🏠 홈", "📖 전례력 캘린더", "🕯️ 묵상기도문", "🤖 챗봇대화", "👤 마이페이지"],
    horizontal=True,
    label_visibility="collapsed",
    key="main_menu"
)

# ✅ 홈
if menu == "🏠 홈":
    st.title("🏠 Ora.AI")
    st.markdown("신앙 여정을 함께하는 AI 동반자 💒")

# ✅ 묵상 기도문
elif menu == "🕯️ 묵상기도문":
    st.title("🕯️ 감정 기반 묵상 기도문 추천")
    keyword = st.text_input("당신의 감정이나 상황을 입력해보세요 🙏", placeholder="ex. 외로움, 감사, 시험, 희망")

    def ai_recommend_verses(keyword):
        prompt = f"""너는 가톨릭 신학에 밝은 AI야. '{keyword}'라는 감정이나 상황에 적절한 성경 구절 3개를 한국어로 추천해줘.
구절은 다음 포맷을 따라:

1. [책 이름] [장]:[절] - [내용]
2. ...
3. ...

반드시 이 형식을 지켜줘."""
        response = model.generate_content(prompt)
        return response.text

    if st.button("기도문 추천 받기") and keyword:
        with st.spinner("기도문을 준비 중입니다..."):
            verses_text = ai_recommend_verses(keyword)
            st.markdown(verses_text)
            st.download_button(
                label="📝 묵상 텍스트 다운로드",
                data=verses_text,
                file_name="meditation.txt",
                mime="text/plain"
            )

# ✅ 전례력 캘린더
elif menu == "📖 전례력 캘린더":
    st.title("📖 전례력 기반 캘린더")
    st.info("전례력 캘린더는 추후 업데이트 예정입니다.")

# ✅ 챗봇 대화
elif menu == "🤖 챗봇대화":
    st.title("🤖 Ora.AI 챗봇")
    st.info("성인 챗봇 및 교리 Q&A 기능은 추후 추가될 예정입니다.")

# ✅ 마이페이지
elif menu == "👤 마이페이지":
    st.title("👤 마이페이지")
    st.info("회원 기능은 추후 도입될 예정입니다.")
