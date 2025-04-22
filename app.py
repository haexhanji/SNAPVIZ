import streamlit as st
import datetime
import google.generativeai as genai

# ✅ Gemini API 키 설정
genai.configure(api_key="AIzaSyC5VbRN66OLvUzNtbicw4KwtIUWdK08lLA")
model = genai.GenerativeModel("models/gemini-1.5-pro")

# 🌐 앱 설정 및 사이드 메뉴 구성
st.set_page_config(page_title="Ora.AI – 천주교 AI 동반자", layout="wide")
st.sidebar.title("🙏 Ora.AI 메뉴")
menu = st.sidebar.radio("이동할 메뉴를 선택하세요", [
    "🏠 홈",
    "📅 전례력 캘린더",
    "📝 묵상 기도문",
    "🙋‍♂️ 성인 챗봇에게 질문하기",
    "👤 마이페이지"
])

# 🏠 홈 화면
if menu == "🏠 홈":
    st.title("Ora.AI ✨")
    st.markdown("천주교 신자들을 위한 **기도와 묵상, 성경, 전례력 안내**를 도와주는 AI 앱입니다.")

# 📅 전례력 캘린더
elif menu == "📅 전례력 캘린더":
    st.title("📅 오늘의 전례 안내")
    today = datetime.date.today()
    today_str = today.strftime('%Y년 %m월 %d일')

    with st.spinner("오늘의 전례 정보를 불러오는 중..."):
        prompt = f"""
        오늘은 {today_str}입니다. 천주교 전례력 기준으로 오늘은 무슨 전례일인가요?
        어떤 복음이 낭독되며, 기념하는 성인이나 전례색, 의미 등을 포함해서 요약해서 알려주세요.
        """
        response = model.generate_content(prompt)
        st.success(f"✅ {today_str} 전례 정보")
        st.markdown(response.text)

# 📝 묵상 기도문
elif menu == "📝 묵상 기도문":
    st.title("📝 맞춤 묵상 기도문 생성기")
    keyword = st.text_input("🙏 기도하고 싶은 주제(예: 두려움, 감사, 용서 등)를 입력하세요")

    if keyword:
        with st.spinner("기도문을 작성 중입니다..."):
            prompt = f"""
            사용자가 '{keyword}'라는 주제로 묵상 기도를 원합니다.
            진심이 담긴 천주교식 기도문을 5~6문장 이내로 작성해 주세요.
            """
            response = model.generate_content(prompt)
            st.subheader("📖 생성된 기도문")
            st.write(response.text)

# 🙋‍♂️ 성인 챗봇
elif menu == "🙋‍♂️ 성인 챗봇에게 질문하기":
    st.title("🙋‍♂️ 성인 챗봇에게 질문하기")
    user_question = st.text_area("💬 당신의 질문을 입력하세요")

    if st.button("🙏 성인의 지혜 듣기") and user_question:
        with st.spinner("성인의 말씀을 전하고 있습니다..."):
            prompt = f"""
            당신은 천주교의 지혜로운 성인입니다.
            사용자가 '{user_question}'이라는 질문을 했습니다.
            1. 먼저 따뜻한 인사로 시작하고,
            2. 성경에서 영감을 받은 위로와 조언을 주세요.
            3. 관련 성경 구절 1~2개를 포함하고,
            4. 마지막에 기도문으로 마무리해 주세요.
            답변은 신앙적으로 따뜻하고, 희망을 주는 어조로 작성해 주세요.
            """
            response = model.generate_content(prompt)
            st.markdown(response.text)

# 👤 마이페이지
elif menu == "👤 마이페이지":
    st.title("👤 마이페이지")
    st.write("사용자 설정 및 즐겨찾기 기능은 추후 제공될 예정입니다.")