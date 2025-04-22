import streamlit as st
import google.generativeai as genai

# ✅ 페이지 설정
st.set_page_config(page_title="Ora.AI - 가톨릭 AI 동반자", layout="wide")

# 🔐 Gemini API 키 설정
genai.configure(api_key="AIzaSyC5VbRN66OLvUzNtbicw4KwtIUWdK08lLA")
model = genai.GenerativeModel("models/gemini-1.5-pro")

# ✅ 메뉴 구성
menu = st.selectbox(
    "📌 메뉴 선택",
    ["🏠 홈", "🙏 묵상 기도문", "📅 전례력 캘린더", "💬 성인 챗봇", "👤 마이페이지"],
    key="main_menu",
    index=0,
)

st.markdown("---")

# 🏠 홈
if menu == "🏠 홈":
    st.title("🙏 Ora.AI")
    st.subheader("기도하고 묵상하는 AI 동반자")
    st.markdown("가톨릭 정신에 따라 당신의 신앙 여정을 돕는 앱입니다.")

# 🙏 묵상 기도문
elif menu == "🙏 묵상 기도문":
    st.title("🙏 묵상 기도문 생성")
    keyword = st.text_input("📝 묵상하고 싶은 주제 (예: 용서, 감사, 고통, 희망 등)")

    def ai_recommend_verses(prompt):
        full_prompt = f"""
        너는 가톨릭 신자에게 깊은 위로가 되는 성경 구절을 추천하는 AI야.
        주어진 키워드에 어울리는 성경 말씀 3~5개를 뽑아서, 구절과 출처를 함께 알려줘.
        구절은 천주교 성경 번역본을 기준으로 해줘.

        [키워드]
        {prompt}

        [응답 예시]
        1. "구절 내용" - (책 이름 장:절)
        ...
        """
        response = model.generate_content(full_prompt)
        return response.text

    if st.button("📖 성경 구절 추천받기"):
        with st.spinner("묵상할 말씀을 찾는 중입니다..."):
            verses = ai_recommend_verses(keyword)
            st.markdown(verses)

# 📅 전례력 캘린더 (기능 예정)
elif menu == "📅 전례력 캘린더":
    st.title("📅 전례력 기반 안내")
    st.info("전례력 캘린더 기능은 추후 업데이트될 예정입니다.")

# 💬 성인 챗봇
elif menu == "💬 성인 챗봇":
    st.title("💬 성인 챗봇과 대화하기")

    saint = st.selectbox("👼 대화할 성인을 선택하세요", ["성 프란치스코", "성녀 데레사", "성 아우구스티누스"])
    user_question = st.text_input("✉️ 질문을 입력하세요")

    if user_question:
        with st.spinner("성인께 여쭤보는 중입니다..."):
            prompt = f"""
            너는 {saint}야. 지금 너에게 가톨릭 신자가 질문을 하고 있어.
            {saint} 특유의 말투와 가치관, 영성에 맞춰 답변해줘. 신앙적인 위로와 조언이 되도록 해.

            [질문]
            {user_question}

            [답변]
            """
            response = model.generate_content(prompt)
            st.markdown(response.text)

# 👤 마이페이지
elif menu == "👤 마이페이지":
    st.title("👤 마이페이지")
    st.info("사용자 정보, 저장된 기도문 등은 여기에 표시될 예정입니다.")