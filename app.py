import streamlit as st
import google.generativeai as genai
import json

# 🔐 Gemini API 키 설정
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# ✅ 페이지 설정
st.set_page_config(
    page_title="Ora.AI - 천주교 묵상 도우미",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ 성경 데이터 로딩 함수
@st.cache_data
def load_bible():
    with open("bible_db.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ✅ 검색 함수
def search_verses(keyword):
    return [v for v in bible_data if keyword in v["text"]][:3]

# ✅ 묵상 생성 함수
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

# ✅ 성경 데이터 로딩
try:
    bible_data = load_bible()
except FileNotFoundError:
    st.error("❗ bible_db.json 파일이 없습니다. 업로드해주세요.")
    st.stop()

# ✅ 앱 타이틀
st.title("🙏 Ora.AI - 천주교 기반 성경 묵상")
st.subheader("주제어로 말씀을 검색하고, 은혜로운 묵상을 받아보세요")

# ✅ 키워드 입력
keyword = st.text_input("🔍 주제어를 입력하세요 (예: 사랑, 고통, 희망 등)")
if keyword:
    results = search_verses(keyword)
    if results:
        for verse in results:
            st.markdown(f"📖 **{verse['book']} {verse['chapter']}:{verse['verse']}**")
            st.markdown(f"> {verse['text']}")

            if st.button("🧎‍♂️ 이 말씀으로 묵상하기", key=verse["book"]+str(verse["verse"])):
                with st.chat_message("assistant"):
                    with st.spinner("Ora.AI가 묵상 기도 중..."):
                        meditation = generate_meditation(verse)
                        st.markdown("🕊️ **묵상 기도문**")
                        st.markdown(meditation)
    else:
        st.warning("관련 성경 구절을 찾을 수 없습니다. 다른 단어를 입력해보세요.")
