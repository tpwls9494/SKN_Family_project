import streamlit as st
import time
import os
import tempfile
import pyaudio
import wave
import numpy as np
from openai_api import stt, ask_angel_devil, tts

# Streamlit 페이지 설정
st.set_page_config(page_title="천사와 악마 AI", page_icon="😇", layout="centered")
st.title("😇 천사와 악마 AI 😈")
st.subheader("질문에 천사와 악마가 함께 답변합니다")

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 마이크로 녹음하는 함수
def record_audio(seconds):
    """
    마이크로 오디오를 녹음하는 함수
    
    Args:
        seconds: 녹음 시간 (초)
    
    Returns:
        임시 오디오 파일 경로
    """
    # 오디오 설정
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    
    # PyAudio 객체 생성
    p = pyaudio.PyAudio()
    
    # 진행 상태 표시
    status = st.empty()
    status.info(f"{seconds}초 동안 녹음합니다. 말씀해 주세요!")
    
    # 프로그레스 바
    progress_bar = st.progress(0)
    
    # 녹음 스트림 열기
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    # 녹음 시작
    frames = []
    for i in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
        
        # 진행률 업데이트
        elapsed = (i + 1) / (RATE / CHUNK * seconds)
        progress_bar.progress(elapsed)
        remaining = seconds * (1 - elapsed)
        status.info(f"녹음 중... {remaining:.1f}초 남았습니다.")
    
    # 녹음 종료
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    status.success("녹음 완료!")
    time.sleep(0.5)
    progress_bar.empty()
    status.empty()
    
    # 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_path = temp_file.name
        
        wf = wave.open(temp_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    
    return temp_path

# 이전 대화 내용 표시
if st.session_state.chat_history:
    st.subheader("💬 이전 대화")
    
    for i, (role, text, angel_response, devil_response) in enumerate(st.session_state.chat_history):
        if role == "user":
            st.markdown(f"👤 **나:** {text}")
            
            # 천사와 악마 응답을 표시할 컬럼 생성
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 😇 천사")
                st.markdown(f"{angel_response}")
                
                # 천사 음성 재생 버튼
                if st.button("😇 천사 음성 듣기", key=f"history_angel_{i}"):
                    angel_audio = tts(angel_response, voice="nova")
                    if angel_audio:
                        st.markdown(angel_audio, unsafe_allow_html=True)
            
            with col2:
                st.markdown("### 😈 악마")
                st.markdown(f"{devil_response}")
                
                # 악마 음성 재생 버튼
                if st.button("😈 악마 음성 듣기", key=f"history_devil_{i}"):
                    devil_audio = tts(devil_response, voice="echo")
                    if devil_audio:
                        st.markdown(devil_audio, unsafe_allow_html=True)
            
            st.divider()

# 녹음 버튼
if st.button("🎤 마이크 켜고 질문하기", use_container_width=True):
    try:
        # 녹음 시간 설정
        recording_seconds = 5  # 기본 5초로 설정
        
        # 마이크 녹음
        audio_path = record_audio(recording_seconds)
        
        # 처리 상태
        with st.status("AI가 처리 중입니다...") as status:
            try:
                # 1. STT: 음성을 텍스트로 변환
                status.update(label="음성을 텍스트로 변환 중...")
                transcribed_text = stt(audio_path)
                
                if not transcribed_text or transcribed_text is None or len(str(transcribed_text).strip()) == 0:
                    status.update(label="음성을 인식할 수 없었습니다.", state="error")
                    st.error("음성 인식에 실패했습니다. 다시 시도해주세요.")
                else:
                    # 인식된 텍스트 표시
                    st.markdown(f"👤 **내 질문:** {transcribed_text}")
                    
                    # 2. GPT: 천사와 악마의 응답 생성
                    status.update(label="천사와 악마가 답변을 생성 중...")
                    angel_response, devil_response = ask_angel_devil(transcribed_text)
                    
                    # 대화 기록에 사용자 질문과 응답 추가
                    st.session_state.chat_history.append(("user", transcribed_text, angel_response, devil_response))
                    
                    # 응답 표시를 위한 컬럼 생성
                    angel_col, devil_col = st.columns(2)
                    
                    # 3. TTS: 천사와 악마 텍스트를 음성으로 변환
                    status.update(label="음성으로 변환 중...")
                    
                    # 천사 음성 변환
                    angel_audio = tts(angel_response, voice="nova")  # 부드러운 목소리
                    
                    # 악마 음성 변환
                    devil_audio = tts(devil_response, voice="echo")  # 낮고 강한 목소리
                    
                    # 천사 응답 표시
                    with angel_col:
                        st.markdown("### 😇 천사")
                        st.markdown(f"{angel_response}")
                        
                        if angel_audio:
                            if st.button("😇 천사 음성 듣기", key=f"angel_audio_{len(st.session_state.chat_history)}"):
                                st.markdown(angel_audio, unsafe_allow_html=True)
                    
                    # 악마 응답 표시
                    with devil_col:
                        st.markdown("### 😈 악마")
                        st.markdown(f"{devil_response}")
                        
                        if devil_audio:
                            if st.button("😈 악마 음성 듣기", key=f"devil_audio_{len(st.session_state.chat_history)}"):
                                st.markdown(devil_audio, unsafe_allow_html=True)
                    
                    status.update(label="처리가 완료되었습니다!", state="complete")
            
            except Exception as e:
                status.update(label=f"오류가 발생했습니다: {str(e)}", state="error")
                st.error(f"처리 중 오류가 발생했습니다: {str(e)}")
        
        # 임시 파일 삭제
        if os.path.exists(audio_path):
            os.unlink(audio_path)
    
    except Exception as e:
        st.error(f"마이크 녹음 중 오류가 발생했습니다: {str(e)}")

# 구분선
st.divider()

# 텍스트 입력 옵션
st.subheader("📝 텍스트로도 질문할 수 있어요")
text_input = st.text_input("질문을 입력하세요:", placeholder="여기에 질문을 입력하세요...")

if st.button("질문하기", use_container_width=True) and text_input:
    # 처리 상태 표시
    with st.status("AI가 처리 중입니다...") as status:
        try:
            # GPT 응답 생성
            status.update(label="천사와 악마가 답변을 생성 중...")
            angel_response, devil_response = ask_angel_devil(text_input)
            
            # 대화 기록에 사용자 질문과 응답 추가
            st.session_state.chat_history.append(("user", text_input, angel_response, devil_response))
            
            # 응답 표시를 위한 컬럼 생성
            angel_col, devil_col = st.columns(2)
            
            # TTS: 천사와 악마 텍스트를 음성으로 변환
            status.update(label="음성으로 변환 중...")
            
            # 천사 음성 변환
            angel_audio = tts(angel_response, voice="nova")  # 부드러운 목소리
            
            # 악마 음성 변환
            devil_audio = tts(devil_response, voice="echo")  # 낮고 강한 목소리
            
            # 천사 응답 표시
            with angel_col:
                st.markdown("### 😇 천사")
                st.markdown(f"{angel_response}")
                
                if angel_audio:
                    if st.button("😇 천사 음성 듣기", key=f"text_angel_audio_{len(st.session_state.chat_history)}"):
                        st.markdown(angel_audio, unsafe_allow_html=True)
            
            # 악마 응답 표시
            with devil_col:
                st.markdown("### 😈 악마")
                st.markdown(f"{devil_response}")
                
                if devil_audio:
                    if st.button("😈 악마 음성 듣기", key=f"text_devil_audio_{len(st.session_state.chat_history)}"):
                        st.markdown(devil_audio, unsafe_allow_html=True)
            
            status.update(label="처리가 완료되었습니다!", state="complete")
        
        except Exception as e:
            status.update(label=f"오류가 발생했습니다: {str(e)}", state="error")
            st.error(f"처리 중 오류가 발생했습니다: {str(e)}")

# 푸터
st.markdown("---")
st.caption("🔊 음성 인식: OpenAI Whisper | 🧠 AI 모델: GPT-4 | 🎤 음성 합성: OpenAI TTS")