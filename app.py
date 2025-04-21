import streamlit as st
import google.generativeai as genai
import json
import random

# 📌 Gemini API 키 설정
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("models/gemini-1.5-pro")

# 🔹 성경 DB 불러오기
@st.cache_data
def load_bible():
    with open("bible_db.json", "r", encoding="utf-8") as f:
        return json.load(f)

bible_data = load_bible()

# 🔍 키워드 기반 검색
def search_verses(keyword):
    matches = []
    for verse in bible_data:
        if keyword in verse["text"]:
            matches.append(verse)
    return matches[:3]  # 상위 3개만 표시

# 🧠 묵상 기도문 생성
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

# 🎯 UI 시작
st.set_page_config(page_title="기도 기반 성경 검색기", layout="centered")
st.title("🙏 성경 말씀과 묵상")

keyword = st.text_input("🔍 주제어를 입력하세요 (예: 사랑, 고통, 희망 등)")
if keyword:
    results = search_verses(keyword)
    if results:
        for verse in results:
            st.markdown(f"📖 **{verse['book']} {verse['chapter']}:{verse['verse']}**")
            st.markdown(f"> {verse['text']}")

            if st.button(f"🧎‍♂️ 이 말씀으로 묵상하기", key=verse["book"]+str(verse["verse"])):
                with st.spinner("SNAPVIZ가 묵상 기도 중..."):
                    meditation = generate_meditation(verse)
                    st.markdown("🕊️ **묵상 기도문**")
                    st.markdown(meditation)
    else:
        st.warning("관련 성경 구절을 찾을 수 없습니다. 다른 단어를 입력해보세요.")