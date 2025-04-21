import streamlit as st
import google.generativeai as genai
import json

# 🔐 Gemini API 키 설정
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# ✅ 페이지 설정
st.set_page_config(
    page_title="SNAPVIZ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "scenario_context" not in st.session_state:
    st.session_state.scenario_context = ""
if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False
if "current_menu" not in st.session_state:
    st.session_state.current_menu = "📖 성경 묵상"

# ✅ 사이드바 메뉴
with st.sidebar:
    st.markdown("## 🎛️ SNAPVIZ 기능 선택")
    selected_menu = st.radio(
        label="기능 선택",
        options=["🎬 시나리오 분석", "🗺️ 로케이션 추천", "📖 성경 묵상"],
        index=["🎬 시나리오 분석", "🗺️ 로케이션 추천", "📖 성경 묵상"].index(st.session_state.current_menu),
        key="menu_selector",
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.caption("© 2025 SNAPVIZ Studio")

    st.session_state.current_menu = selected_menu


# ✅ 시나리오 분석
if st.session_state.current_menu == "🎬 시나리오 분석":
    st.title("🎬 SNAPVIZ 시나리오 분석 챗봇")
    st.subheader("1️⃣ 먼저 시나리오 전체를 입력해주세요")
    scenario = st.text_area("✍️ 시나리오 입력", height=250)

    if st.button("✅ 분석 시작하기"):
        st.session_state.scenario_context = scenario
        st.session_state.chat_history = []
        st.success("시나리오가 등록되었습니다. 이제 자유롭게 질문해보세요!")

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
                with st.spinner("SNAPVIZ가 생각 중..."):
                    st.session_state.is_thinking = True
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
                    st.session_state.is_thinking = False

# ✅ 로케이션 추천
elif st.session_state.current_menu == "🗺️ 로케이션 추천":
    st.title("🗺️ SNAPVIZ 로케이션 추천")
    st.subheader("2️⃣ 장면 키워드 기반 추천 장소 찾기 (기능 개발 예정)")
    st.info("예: 지하철, 바닷가, 오래된 카페 같은 키워드 기반 장소 추천 기능이 여기에 들어올 예정입니다.")

# ✅ 성경 묵상
elif st.session_state.current_menu == "📖 성경 묵상":
    st.title("📖 성경 말씀과 묵상")
    st.subheader("3️⃣ 주제어로 말씀을 검색하고, 묵상을 받아보세요")

    # 성경 데이터 로딩 함수
    @st.cache_data
    def load_bible():
        with open("bible_db.json", "r", encoding="utf-8") as f:
            return json.load(f)

    bible_data = load_bible()

    def search_verses(keyword):
        return [v for v in bible_data if keyword in v["text"]][:3]

    def generate_meditation(verse):
        prompt = f"""
너는 천주교 영성가야. 아래 성경 구절에 대해 묵상 기도문을 작성해줘. 고요하고 은혜로운 말투로 써줘.

[성경 구절]
{verse['book']} {verse['chapter']}장 {verse['verse']}절
"{verse['text']}"

[기도문]
"""
        response = model.generate_content(prompt)
        return response.text

    keyword = st.text_input("🔍 주제어를 입력하세요 (예: 사랑, 고통, 희망 등)")
    if keyword:
        results = search_verses(keyword)
        if results:
            for verse in results:
                st.markdown(f"📖 **{verse['book']} {verse['chapter']}:{verse['verse']}**")
                st.markdown(f"> {verse['text']}")

                if st.button("🧎‍♂️ 이 말씀으로 묵상하기", key=verse["book"]+str(verse["verse"])):
                    with st.chat_message("assistant"):
                        with st.spinner("SNAPVIZ가 묵상 기도 중..."):
                            meditation = generate_meditation(verse)
                            st.markdown("🕊️ **묵상 기도문**")
                            st.markdown(meditation)
        else:
            st.warning("관련 성경 구절을 찾을 수 없습니다. 다른 단어를 입력해보세요.")