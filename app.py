import streamlit as st
import google.generativeai as genai
import json

# ✅ Gemini API 설정
genai.configure(api_key="AIzaSyC5VbRN66OLvUzNtbicw4KwtIUWdK08lLA")
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# ✅ 성경 데이터 로딩 함수
@st.cache_data
def load_bible():
    with open("bible_db.json", "r", encoding="utf-8") as f:
        return json.load(f)

bible_data = load_bible()

# ✅ 성경 구절 추천 함수
def ai_recommend_verses(keyword):
    prompt = f"""
    너는 천주교 성경 전문가야. '{keyword}'라는 주제에 어울리는 성경 구절 3개를 추천해줘.
    각 구절에는 간단한 해설도 덧붙여줘.
    """
    response = model.generate_content(prompt)
    return response.text

# ✅ 상단 메뉴 선택
selected_menu = st.radio(
    "메뉴 선택",
    ["📅 전례력 캘린더", "🙏 묵상기도문", "🏠 홈", "💬 챗봇대화", "🙋‍♂️ 마이페이지"],
    horizontal=True
)

# ✅ 메뉴별 페이지 구성
if selected_menu == "📅 전례력 캘린더":
    st.title("📅 전례력 캘린더")
    st.info("전례 일정에 따라 축일 및 성경 구절을 안내할 기능입니다.")

elif selected_menu == "🙏 묵상기도문":
    st.title("🙏 오늘의 묵상 기도문")
    keyword = st.text_input("🙏 주제어를 입력해주세요 (예: 감사, 용서, 고통, 사랑 등)")
    if st.button("📖 성경 구절 추천받기"):
        with st.spinner("기도문을 추천 중입니다..."):
            verses_text = ai_recommend_verses(keyword)
            st.subheader("📖 추천 성경 구절")
            st.write(verses_text)

            # 텍스트 저장
            st.download_button("💾 묵상 저장하기", data=verses_text, file_name="묵상기도.txt")

elif selected_menu == "🏠 홈":
    st.title("🏠 Ora.AI 홈")
    st.markdown("""
    ### 환영합니다 🙏
    Ora.AI는 당신의 영적 여정을 도와주는 천주교 기반 AI 동반자입니다.
    오늘의 기도와 말씀을 통해 평안을 얻어보세요.
    """)

elif selected_menu == "💬 챗봇대화":
    st.title("💬 성인 챗봇 대화")
    st.info("성 프란치스코, 성녀 데레사와 대화할 수 있는 AI 챗봇 기능은 곧 추가될 예정입니다.")

elif selected_menu == "🙋‍♂️ 마이페이지":
    st.title("🙋‍♂️ 마이페이지")
    st.write("묵상 기록, 즐겨찾기, 계정 정보 기능이 여기에 들어갈 예정입니다.")
