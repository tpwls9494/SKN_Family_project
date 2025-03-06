import streamlit as st
import time
import os
import tempfile
import pyaudio
import wave
import numpy as np
from openai_api import stt, ask_angel_devil, tts

st.set_page_config(page_title="천사와 악마 AI", page_icon="😇", layout="centered")
st.title("😇 천사와 악마 AI 😈")
st.subheader("질문에 천사와 악마가 함께 답변합니다")

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "angel_responses" not in st.session_state:
    st.session_state.angel_responses = {}
if "devil_responses" not in st.session_state:
    st.session_state.devil_responses = {}
if "recording" not in st.session_state:
    st.session_state.recording = False
if "frames" not in st.session_state:
    st.session_state.frames = []
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None

def start_recording():
    """녹음 세션 시작"""
    st.session_state.recording = True
    st.session_state.frames = []
    st.session_state.record_start_time = time.time()
    st.rerun()

def stop_recording():
    """녹음 중지 및 오디오 파일 저장"""
    st.session_state.recording = False
    
    if not st.session_state.frames:
        st.error("녹음된 내용이 없습니다. 다시 시도해주세요.")
        return
    
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    p = pyaudio.PyAudio()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_path = temp_file.name
        
        wf = wave.open(temp_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(st.session_state.frames))
        wf.close()
    
    p.terminate()
    
    st.session_state.audio_path = temp_path
    st.session_state.process_audio = True
    st.rerun()

def record_chunk():
    """현재 녹음 청크 기록"""
    if not st.session_state.recording:
        return
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    for _ in range(20):
        if not st.session_state.recording:
            break
        data = stream.read(CHUNK)
        st.session_state.frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()

def reset_recording_state():
    """녹음 관련 상태 초기화"""
    st.session_state.recording = False
    st.session_state.frames = []
    st.session_state.process_audio = False
    if "audio_path" in st.session_state and st.session_state.audio_path:
        if os.path.exists(st.session_state.audio_path):
            try:
                os.unlink(st.session_state.audio_path)
            except Exception:
                pass
        st.session_state.audio_path = None

if st.session_state.chat_history:
    st.subheader("💬 이전 대화")
    
    for i, (role, text, angel_response, devil_response) in enumerate(st.session_state.chat_history):
        if role == "user":
            st.markdown(f"👤 **나:** {text}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 😇 천사")
                # 천사 음성 재생 버튼 (바로 재생)
                angel_key = f"history_angel_{i}"
                if angel_key not in st.session_state.angel_responses:
                    st.session_state.angel_responses[angel_key] = tts(angel_response, voice="nova")
                
                # 직접 오디오 태그 표시 (버튼 필요 없음)
                st.markdown(f"[😇 천사 음성 듣기](javascript:void(0))", unsafe_allow_html=True)
                st.markdown(st.session_state.angel_responses[angel_key], unsafe_allow_html=True)
            
            with col2:
                st.markdown("### 😈 악마")
                # 악마 음성 재생 버튼 (바로 재생)
                devil_key = f"history_devil_{i}"
                if devil_key not in st.session_state.devil_responses:
                    st.session_state.devil_responses[devil_key] = tts(devil_response, voice="echo")
                
                # 직접 오디오 태그 표시 (버튼 필요 없음)
                st.markdown(f"[😈 악마 음성 듣기](javascript:void(0))", unsafe_allow_html=True)
                st.markdown(st.session_state.devil_responses[devil_key], unsafe_allow_html=True)
            
            st.divider()

st.subheader("🎤 음성으로 질문하기")

if st.session_state.recording:
    elapsed = time.time() - st.session_state.record_start_time
    st.info(f"녹음 중... (경과 시간: {elapsed:.1f}초)")
    
    if st.button("녹음 중지", use_container_width=True, key="stop_button"):
        stop_recording()
    
    record_chunk()
    
    time.sleep(0.1)
    st.rerun()
    
elif "process_audio" in st.session_state and st.session_state.process_audio:
    st.success("녹음 완료! 처리 중...")
    
    with st.status("AI가 처리 중입니다...") as status:
        status.update(label="음성을 텍스트로 변환 중...")
        transcribed_text = stt(st.session_state.audio_path)
        
        if not transcribed_text or transcribed_text is None or len(str(transcribed_text).strip()) == 0:
            status.update(label="음성을 인식할 수 없었습니다.", state="error")
            st.error("음성 인식에 실패했습니다. 다시 시도해주세요.")
        else:
            st.markdown(f"👤 **내 질문:** {transcribed_text}")
            
            # 2. GPT: 천사와 악마의 응답 생성
            status.update(label="천사와 악마가 답변을 생성 중...")
            angel_response, devil_response = ask_angel_devil(transcribed_text)
            
            st.session_state.chat_history.append(("user", transcribed_text, angel_response, devil_response))
            
            angel_col, devil_col = st.columns(2)
            
            status.update(label="음성으로 변환 중...")
            
            # 천사 음성 변환 및 바로 표시
            current_idx = len(st.session_state.chat_history) - 1
            angel_key = f"angel_audio_{current_idx}"
            st.session_state.angel_responses[angel_key] = tts(angel_response, voice="nova")
            
            devil_key = f"devil_audio_{current_idx}"
            st.session_state.devil_responses[devil_key] = tts(devil_response, voice="echo")
            
            # 천사 응답 표시 - 텍스트 없이 버튼만
            with angel_col:
                st.markdown("### 😇 천사")
                st.markdown(f"[😇 천사 음성 듣기](javascript:void(0))", unsafe_allow_html=True)
                st.markdown(st.session_state.angel_responses[angel_key], unsafe_allow_html=True)
            
            # 악마 응답 표시 - 텍스트 없이 버튼만
            with devil_col:
                st.markdown("### 😈 악마")
                st.markdown(f"[😈 악마 음성 듣기](javascript:void(0))", unsafe_allow_html=True)
                st.markdown(st.session_state.devil_responses[devil_key], unsafe_allow_html=True)
            
            status.update(label="처리가 완료되었습니다!", state="complete")
    
    # 임시 파일 삭제
    if os.path.exists(st.session_state.audio_path):
        os.unlink(st.session_state.audio_path)
    
    st.session_state.process_audio = False
    reset_recording_state()
    
    if st.button("새로운 질문하기", use_container_width=True, key="new_question"):
        st.rerun()
    
else:
    if st.button("마이크 켜고 질문하기", use_container_width=True, key="start_button"):
        start_recording()

st.divider()

st.subheader("📝 텍스트로도 질문할 수 있어요")
text_input = st.text_input("질문을 입력하세요:", placeholder="여기에 질문을 입력하세요...")

if st.button("질문하기", use_container_width=True) and text_input:
    with st.status("AI가 처리 중입니다...") as status:
        status.update(label="천사와 악마가 답변을 생성 중...")
        angel_response, devil_response = ask_angel_devil(text_input)
        
        st.session_state.chat_history.append(("user", text_input, angel_response, devil_response))
        current_idx = len(st.session_state.chat_history) - 1
        
        # 응답 표시를 위한 컬럼 생성
        angel_col, devil_col = st.columns(2)
        
        status.update(label="음성으로 변환 중...")
        
        # 천사 음성 변환
        angel_audio = tts(angel_response, voice="nova")  # 부드러운 목소리
        st.session_state.angel_responses[f"text_angel_audio_{current_idx}"] = angel_audio
        
        # 악마 음성 변환
        devil_audio = tts(devil_response, voice="echo")  # 낮고 강한 목소리
        st.session_state.devil_responses[f"text_devil_audio_{current_idx}"] = devil_audio
        
        # 천사 응답 표시 - 텍스트 없이 버튼만
        with angel_col:
            st.markdown("### 😇 천사")
            
            # 천사 음성 변환 및 바로 표시
            angel_key = f"text_angel_audio_{current_idx}"
            st.session_state.angel_responses[angel_key] = tts(angel_response, voice="nova")
            
            st.markdown(f"[😇 천사 음성 듣기](javascript:void(0))", unsafe_allow_html=True)
            st.markdown(st.session_state.angel_responses[angel_key], unsafe_allow_html=True)
        
        # 악마 응답 표시 - 텍스트 없이 버튼만
        with devil_col:
            st.markdown("### 😈 악마")
            
            # 악마 음성 변환 및 바로 표시
            devil_key = f"text_devil_audio_{current_idx}"
            st.session_state.devil_responses[devil_key] = tts(devil_response, voice="echo")
            
            st.markdown(f"[😈 악마 음성 듣기](javascript:void(0))", unsafe_allow_html=True)
            st.markdown(st.session_state.devil_responses[devil_key], unsafe_allow_html=True)
        
        status.update(label="처리가 완료되었습니다!", state="complete")

st.markdown("---")
st.caption("🔊 음성 인식: OpenAI Whisper | 🧠 AI 모델: GPT-4 | 🎤 음성 합성: OpenAI TTS")