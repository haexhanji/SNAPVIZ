import streamlit as st
import google.generativeai as genai

# 🔐 해찬이 Gemini API 키
genai.configure(api_key="AIzaSyDX_xmE8icIKQDURcDxe4136lHE8M4yvrI")
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# ✅ 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "scenario_context" not in st.session_state:
    st.session_state.scenario_context = ""

# 📌 시나리오 입력창
st.title("🎬 SNAPVIZ 시나리오 분석 챗봇")
st.subheader("1️⃣ 먼저 시나리오 전체를 입력해주세요")
scenario = st.text_area("✍️ 시나리오 입력", height=250)

if st.button("✅ 분석 시작하기"):
    st.session_state.scenario_context = scenario
    st.session_state.chat_history = []
    st.success("시나리오가 등록되었습니다. 이제 자유롭게 질문해보세요!")

# 💬 대화형 인터페이스
if st.session_state.scenario_context:
    st.divider()
    st.subheader("💬 시나리오 관련 질문하기")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("시나리오 관련 질문을 입력하세요!")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Gemini가 생각 중..."):
                full_prompt = f"""너는 시나리오 전문가야. 아래 시나리오를 참고해서 유저의 질문에 구체적으로 조언해줘.

[시나리오]
{st.session_state.scenario_context}

[유저 질문]
{user_input}

[답변]
"""
                response = model.generate_content(full_prompt)
                output = response.text
                st.markdown(output)
                st.session_state.chat_history.append({"role": "assistant", "content": output})