import streamlit as st
import google.generativeai as genai

# ✅ Gemini API 키 설정
genai.configure(api_key="AIzaSyC5VbRN66OLvUzNtbicw4KwtIUWdK08lLA")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# ✅ 페이지 UI 설정
st.set_page_config(
    page_title="Ora.AI - 성경 묵상 동반자",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ 묵상 생성 함수
def generate_meditation(verse_text):
    prompt = f"""
너는 천주교 영성가야. 아래 성경 구절에 대한 묵상 기도문을 작성해줘. 고요하고 은혜로운 말투로 써줘.

[성경 구절]
{verse_text}

[기도문]
"""
    response = model.generate_content([prompt])
    return response.text

# ✅ 주제어 기반 성경 구절 추천 함수
def ai_recommend_verses(keyword):
    prompt = f"""
너는 천주교 성경 전문가야. '{keyword}'라는 주제와 관련된 대표적인 성경 구절 3개를 추천해줘.

각 구절은 다음 형식으로 정리해줘:

[책 이름] [장]:[절]
"본문"
"""
    response = model.generate_content([prompt])
    return response.text

# ✅ 앱 인터페이스
st.title("🙏 Ora.AI - 천주교 기반 성경 묵상")
st.subheader("주제어로 말씀을 추천받고, 묵상 기도문을 생성하세요 ✨")

# ✅ 주제어 입력
keyword = st.text_input("🔍 주제어를 입력하세요 (예: 용서, 고통, 사랑, 감사 등)")

if keyword:
    with st.spinner("📖 성경 구절 찾는 중..."):
        try:
            verses_text = ai_recommend_verses(keyword)
            st.markdown("🕯️ **추천 성경 구절**")
            st.markdown(verses_text)

            # 묵상 기도문 생성 버튼
            if st.button("🧎 묵상 기도문 생성하기"):
                with st.chat_message("assistant"):
                    with st.spinner("Ora.AI가 묵상 기도 작성 중..."):
                        meditation = generate_meditation(verses_text)
                        st.markdown("🕊️ **묵상 기도문**")
                        st.markdown(meditation)

                        # 텍스트 파일 저장 버튼
                        st.download_button(
                            label="📥 묵상 기도문 저장하기",
                            data=meditation,
                            file_name="meditation.txt",
                            mime="text/plain"
                        )
        except Exception as e:
            st.error("❗ 오류가 발생했습니다. API 키 또는 모델 상태를 확인해주세요.")
            st.exception(e)