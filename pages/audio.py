import streamlit as st
import numpy as np
import base64
import io

# 페이지 설정
st.set_page_config(layout='wide', page_title='EthicApp')

# 사이드바 메뉴 선택
# 만약에 딥페이크 음성말고 다른 라디오 버튼 추가하고 싶으시면 menu = st.sidebar.radio("Menu", ["딥페이크 음성", "추가하고 싶은 것"]) 이렇게 넣으시면 됩니다.
# 그리고 추가하신다면 69번 줄로 내려오세요.
menu = st.sidebar.radio("Menu", ["딥페이크 음성"])

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
# 위에 10번처럼 "추가하고 싶은 것" 있다면 elif 쓰셔야 합니다. ex) elif meenu == "추가하고 싶은 것": 72번 참고해서 사용하시면 됩니다.
if menu == "딥페이크 음성":
    run_deepfake_demo()

# elif menu == "추가하고 싶은 것":
#     st.write("추가하고 싶은 곳 섹션입니다. 관련 문서 넣어주세요.")