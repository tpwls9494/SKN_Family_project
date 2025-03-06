import os
import base64
import tempfile
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def stt(audio_file_path):
    """
    음성을 텍스트로 변환 (STT)
    
    Args:
        audio_file_path: 오디오 파일 경로
    
    Returns:
        변환된 텍스트
    """
    # OpenAI Whisper API 호출
    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="ko"
        )
    
    return transcript.text

def ask_angel_devil(query, temperature=0.7):
    """
    천사와 악마 각각의 응답을 생성하는 함수
    
    Args:
        query: 사용자 질문
        temperature: 창의성 조절 (0.0-1.0)
    
    Returns:
        (천사 응답, 악마 응답) 튜플
    """
    # 천사 프롬프트
    angel_system_prompt = """
    당신은 '천사' 역할을 맡은 AI 비서입니다. 사용자의 질문에 항상 긍정적이고, 도움이 되고, 윤리적인 관점에서 답변해야 합니다.
    
    당신의 성격과 답변 스타일:
    - 항상 친절하고 부드러운 어조를 유지하세요
    - 사용자의 삶과 건강에 도움이 되는 조언을 제공하세요
    - 장기적인 이익과 올바른 가치관을 중시하세요
    - 책임감 있고 현명한 결정을 장려하세요
    - 가끔 "우리 함께 좋은 선택을 해봐요"와 같은 격려의 문구를 사용하세요
    - 답변은 한국어로 제공하세요
    - 음성으로 출력될 것이므로 자연스러운 대화체로 간결하게 응답하세요
    
    중요: 당신은 선한 조언자이므로, 항상 사용자의 최선의 이익을 위한 답변을 제공하세요.
    """
    
    # 악마 프롬프트
    devil_system_prompt = """
    당신은 '악마' 역할을 맡은 AI 비서입니다. 사용자의 질문에 장난스럽고, 반항적이며, 때로는 일부러 반대 의견을 제시하는 방식으로 답변해야 합니다.
    
    당신의 성격과 답변 스타일:
    - 약간 냉소적이고 도발적인 어조를 사용하세요
    - 사용자가 기대하는 것과 반대되는 관점을 제시하세요
    - 근시안적 즐거움과 자유로운 선택을 강조하세요
    - "왜 그렇게 착하게 살아? 재미없잖아"와 같은 표현을 가끔 사용하세요
    - 위험하거나 해롭지 않은 선에서 장난스러운 제안을 하세요
    - 답변은 한국어로 제공하세요
    - 음성으로 출력될 것이므로 친근한 대화체로 반말을 사용하여 간결하게 응답하세요
    
    중요: 당신은 장난꾸러기이므로, 사용자에게 득이되지 않는 조언(불법적이거나 심각하게 위험한 행동을 빼고)을 제공하세요.
    사용자에게 반항적이고 장난스러운 답변을 제공하세요.
    """
    
    # 천사 응답 생성
    angel_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": angel_system_prompt},
            {"role": "user", "content": query}
        ],
        temperature=temperature
    )
    
    # 악마 응답 생성
    devil_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": devil_system_prompt},
            {"role": "user", "content": query}
        ],
        temperature=temperature + 0.2  # 약간 더 창의적인 응답을 위해
    )
    
    return (
        angel_response.choices[0].message.content,
        devil_response.choices[0].message.content
    )

def tts(text, voice="nova"):
    """
    텍스트를 음성으로 변환 (TTS)
    
    Args:
        text: 변환할 텍스트
        voice: 사용할 음성 (alloy, echo, fable, onyx, nova, shimmer, ash, sage, coral)
    
    Returns:
        HTML 오디오 태그
    """
    voice = voice.lower()
    
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    
    audio_data = response.content
    base64_encoded = base64.b64encode(audio_data).decode('utf-8')
    
    audio_tag = f"""
    <audio controls preload="auto">
        <source src="data:audio/mp3;base64,{base64_encoded}" type="audio/mp3" />
    </audio>
    """
        
    return audio_tag