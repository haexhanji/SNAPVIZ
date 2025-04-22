import streamlit as st
import google.generativeai as genai

# ✅ Gemini API 키
genai.configure(api_key="AIzaSyC5VbRN66OLvUzNtbicw4KwtIUWdK08lLA")
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# ✅ 앱 레이아웃 설정
st.set_page_config(page_title="Ora.AI", layout="wide")

# ✅ 메뉴 선택
menu = st.sidebar.radio(
    "📖 메뉴를 선택하세요",
    ["홈", "전례력 캘린더", "묵상기도문", "성인 챗봇에게 질문하기", "마이페이지"]
)

# ✅ 홈
if menu == "홈":
    st.title("✨ Ora.AI에 오신 걸 환영합니다!")
    st.write("기도하고 묵상하는 AI 동반자")

# ✅ 전례력 캘린더
elif menu == "전례력 캘린더":
    st.title("📅 전례력 캘린더")
    st.info("이곳에 전례력 기반 달력을 연동할 예정입니다.")

# ✅ 묵상기도문
elif menu == "묵상기도문":
    st.title("🕊️ 묵상 기도문 생성기")
    keyword = st.text_input("🙏 묵상할 주제 (예: 용서, 평화, 사랑 등)", max_chars=30)

    if st.button("📝 기도문 생성"):
        with st.spinner("기도문을 생성 중입니다..."):
            prompt = f"""
너는 신앙 깊은 가톨릭 신자야. '{keyword}'라는 주제에 맞는 아래 형식의 묵상 기도문을 작성해줘.

[형식]
하늘에 계신 하나님,  
...

주 예수 그리스도의 이름으로 기도 드립니다. 아멘
"""
            response = model.generate_content(prompt)
            st.subheader("🕯️ 생성된 기도문")
            st.markdown(response.text)

# ✅ 성인 챗봇
elif menu == "성인 챗봇에게 질문하기":
    st.title("🙏 성인 챗봇에게 질문하기")
    st.write("성인의 말투로 위로와 성경 해석, 기도문을 전해주는 챗봇입니다.")

    user_question = st.text_area("💬 나의 질문", height=180)

    if st.button("✨ 질문하기"):
        with st.chat_message("assistant"):
            with st.spinner("성인의 말씀을 준비 중입니다..."):
                prompt = f"""
너는 가톨릭 성인 챗봇이야. 아래와 같은 형식으로 응답해줘.

[질문]
{user_question}

[생명의 말씀]
(성인의 말투로 위로의 말)

[성경 해설]
(1~2개 관련 성경구절 + 간단한 해설)

[기도문]
(짧은 묵상 기도)
"""
                response = model.generate_content(prompt)
                st.markdown(response.text)

# ✅ 마이페이지
elif menu == "마이페이지":
    st.title("👤 마이페이지")
    st.write("사용자 맞춤 설정, 저장된 기도문 등을 추후 여기에 구성할 예정입니다.")