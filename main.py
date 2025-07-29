import streamlit as st
import numpy as np
import base64
import io

# 페이지 설정
st.set_page_config(layout='wide', page_title='EthicApp')

# 사이드바 메뉴 선택
menu = st.sidebar.radio("Menu", ["홈", "AI 윤리 개요", "딥페이크 음성", "참고 자료"])

# YouTube 영상 링크
url = 'https://www.youtube.com/watch?v=XyEOEBsa8I4'

# 간단한 음성 생성 함수 (진짜 vs 가짜)
def generate_synthetic_audio(is_real=True, duration=3, sr=22050):
    t = np.linspace(0, duration, int(sr * duration))
    if is_real:
        freq = 200 + 100 * np.sin(2 * np.pi * 0.1 * t)
        audio = 0.5 * np.sin(2 * np.pi * freq * t)
    else:
        freq = 200 + 50 * np.sin(2 * np.pi * 0.2 * t)
        audio = 0.5 * np.sin(2 * np.pi * freq * t) + 0.1 * np.random.randn(len(t))
    return audio, sr

# 오디오 재생용 플레이어 (파일 저장 없이 base64로 임베드)
def get_audio_player(audio, sr):
    try:
        import soundfile as sf  # optional: 제거해도 됨
        buffer = io.BytesIO()
        sf.write(buffer, audio, sr, format='WAV')
        audio_base64 = base64.b64encode(buffer.getvalue()).decode()
        return f'<audio controls><source src="data:audio/wav;base64,{audio_base64}" type="audio/wav"></audio>'
    except:
        return "⚠️ 오디오 플레이어를 지원하지 않습니다."

# 딥페이크 음성 탐지 체험 화면 (간단 기능만)
def run_deepfake_demo():
    st.title("🎙️ 딥페이크 음성 탐지 웹앱 (간단 체험)")
    st.markdown("""
    이 앱은 진짜 음성과 딥페이크 음성을 구별하는 과정을 체험할 수 있도록 제작되었습니다.
    
    음성을 생성하고 직접 들어보세요!
    """)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("진짜 음성 생성"):
            audio, sr = generate_synthetic_audio(is_real=True)
            st.markdown("✔️ 진짜 음성 샘플 생성됨")
            st.markdown(get_audio_player(audio, sr), unsafe_allow_html=True)

    with col2:
        if st.button("가짜 음성 생성"):
            audio, sr = generate_synthetic_audio(is_real=False)
            st.markdown("✔️ 가짜 음성 샘플 생성됨")
            st.markdown(get_audio_player(audio, sr), unsafe_allow_html=True)

    st.markdown("또는 직접 WAV 파일을 업로드해보세요.")
    uploaded_file = st.file_uploader("WAV 파일 업로드", type=["wav"])
    if uploaded_file:
        st.markdown("✔️ 파일 업로드 완료 (재생 기능은 생략됨)")

# 메뉴 라우팅
if menu == "홈":
    st.title('Ethic is good for us')
    content_col, tips_col = st.columns([4, 1])

    with content_col:
        st.subheader("AI Ethics and Responsibility")
        st.video(url)
        st.write("""
        인공지능(AI)은 현대 사회를 변화시키는 핵심 기술입니다.  
        그러나 AI의 사용에는 윤리적 고려가 반드시 따라야 하며, 우리는 다음과 같은 원칙을 따라야 합니다:
        - **공정성 (Fairness)**  
        - **책임성 (Accountability)**  
        - **투명성 (Transparency)**  
        - **프라이버시 보호 (Privacy Protection)**
        """)

        user_opinion = st.text_area("여러분의 의견을 남겨주세요:")
        if st.button("제출"):
            if user_opinion:
                with open("data.txt", "a") as file:
                    file.write(f"{user_opinion}\n")
                st.success("의견이 성공적으로 제출되었습니다.")
            else:
                st.warning("의견을 입력해주세요.")

    with tips_col:
        st.subheader("AI 윤리 개요")
        st.markdown("""
        1. **공정성**: AI가 편향된 결정을 내리지 않도록 해야 합니다.  
        2. **책임성**: AI의 결정에 인간이 책임을 져야 합니다.  
        3. **투명성**: AI가 어떻게 작동하는지 이해 가능해야 합니다.  
        4. **프라이버시 보호**: 개인정보를 안전하게 보호해야 합니다.  
        """)

elif menu == "AI 윤리 개요":
    st.header("AI 윤리 원칙에 대해 더 알아보기")
    st.write("좌측 설명을 참고해 주세요.")

elif menu == "딥페이크 음성":
    run_deepfake_demo()

elif menu == "참고 자료":
    st.write("참고 자료 섹션입니다. 관련 문서 및 링크를 제공합니다.")
