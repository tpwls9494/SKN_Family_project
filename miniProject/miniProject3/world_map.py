import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="세계 나라 맞추기 게임",
    page_icon="🌎",
    layout="centered"
)

# 세션 상태 초기화
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
if 'current_country' not in st.session_state:
    st.session_state.current_country = None
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'max_attempts' not in st.session_state:
    st.session_state.max_attempts = 5
if 'guessed_countries' not in st.session_state:
    st.session_state.guessed_countries = []
if 'hint_level' not in st.session_state:
    st.session_state.hint_level = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'country_data' not in st.session_state:

       st.session_state.country_data = {
        "대한민국": {
            "힌트1": "아시아에 위치한 나라입니다.",
            "힌트2": "수도는 서울입니다.",
            "힌트3": "김치, 비빔밥 등의 음식 문화가 유명합니다.",
            "힌트4": "삼성, 현대, LG와 같은 대기업이 있습니다.",
            "설명": "대한민국은 동아시아에 위치한 나라로, 북쪽으로는 북한과 맞닿아 있습니다. K-pop, 한류 등 문화 콘텐츠가 전 세계적으로 인기를 끌고 있습니다."
        },
        "일본": {
            "힌트1": "아시아 동쪽에 위치한 섬나라입니다.",
            "힌트2": "수도는 도쿄입니다.",
            "힌트3": "스시, 라멘 등의 음식이 유명합니다.",
            "힌트4": "벚꽃과 후지산이 상징적입니다.",
            "설명": "일본은 동아시아에 위치한 섬나라로, 첨단 기술과 전통 문화가 공존하는 나라입니다. 애니메이션, 게임 산업이 발달했으며 독특한 문화를 가지고 있습니다."
        },
        "미국": {
            "힌트1": "북아메리카에 위치한 나라입니다.",
            "힌트2": "수도는 워싱턴 D.C.입니다.",
            "힌트3": "세계 최대 경제 대국입니다.",
            "힌트4": "할리우드, 자유의 여신상이 유명합니다.",
            "설명": "미국은 50개의 주로 이루어진 연방 공화국으로, 세계적인 경제, 문화, 군사 강국입니다. 다양한 인종과 문화가 공존하는 다문화 사회입니다."
        },
        "중국": {
            "힌트1": "아시아에서 가장 큰 나라 중 하나입니다.",
            "힌트2": "수도는 베이징입니다.",
            "힌트3": "만리장성이 유명합니다.",
            "힌트4": "세계에서 인구가 가장 많은 나라입니다.",
            "설명": "중국은 동아시아에 위치한 세계에서 인구가 가장 많은 나라입니다. 5천 년이 넘는 역사를 가진 고대 문명국이며, 세계 경제 대국으로 성장했습니다."
        },
        "프랑스": {
            "힌트1": "유럽 서부에 위치한 나라입니다.",
            "힌트2": "수도는 파리입니다.",
            "힌트3": "에펠탑이 유명한 관광지입니다.",
            "힌트4": "와인, 치즈, 패션으로 유명합니다.",
            "설명": "프랑스는 서유럽에 위치한 나라로, 예술, 문화, 요리로 유명합니다. 루브르 박물관, 베르사유 궁전 등 많은 문화유산이 있습니다."
        },
        "영국": {
            "힌트1": "유럽 북서부에 위치한 섬나라입니다.",
            "힌트2": "수도는 런던입니다.",
            "힌트3": "빅벤, 버킹엄 궁전이 유명합니다.",
            "힌트4": "여왕/국왕을 모시는 입헌군주제 국가입니다.",
            "설명": "영국은 잉글랜드, 스코틀랜드, 웨일스, 북아일랜드로 구성된 연합왕국입니다. 산업혁명의 발상지이며 셰익스피어, 비틀즈 등 문화적 영향력이 큰 나라입니다."
        },
        "독일": {
            "힌트1": "유럽 중부에 위치한 나라입니다.",
            "힌트2": "수도는 베를린입니다.",
            "힌트3": "맥주 축제인 옥토버페스트가 유명합니다.",
            "힌트4": "자동차 산업이 발달한 나라입니다.",
            "설명": "독일은 중부 유럽에 위치한 나라로, 강력한 경제력을 바탕으로 유럽 연합에서 중요한 역할을 하고 있습니다. 정밀 기계, 자동차 산업이 발달했습니다."
        },
        "브라질": {
            "힌트1": "남아메리카에서 가장 큰 나라입니다.",
            "힌트2": "수도는 브라질리아입니다.",
            "힌트3": "축구와 삼바로 유명합니다.",
            "힌트4": "아마존 열대우림의 대부분이 이 나라에 있습니다.",
            "설명": "브라질은 남아메리카 최대의 국가로, 포르투갈어를 공용어로 사용합니다. 매년 리우 카니발이 열리며, 세계적인 축구 강국입니다."
        },
        "인도": {
            "힌트1": "남아시아에 위치한 나라입니다.",
            "힌트2": "수도는 뉴델리입니다.",
            "힌트3": "타지마할이 유명한 관광지입니다.",
            "힌트4": "중국 다음으로 인구가 많은 나라입니다.",
            "설명": "인도는 남아시아에 위치한 세계에서 두 번째로 인구가 많은 나라입니다. 다양한 언어와 종교, 문화가 공존하며 IT 산업이 발달했습니다."
        },
        "호주": {
            "힌트1": "오세아니아에 위치한 섬 대륙입니다.",
            "힌트2": "수도는 캔버라입니다.",
            "힌트3": "캥거루, 코알라가 상징적인 동물입니다.",
            "힌트4": "시드니 오페라 하우스가 유명합니다.",
            "설명": "호주는 세계에서 유일하게 대륙 전체가 하나의 국가인 나라입니다. 독특한 생태계와 동물들이 있으며, 광활한 자연환경이 특징입니다."
        }
    }
       
@st.cache_resource
def load_model():
    '''DeepSeek-R1 모델과 토크나이저를 로드합니다'''
    try:
        tokenizer = AutoTokenizer.from_pretrained('deepseek-ai/DeepSeek-R1')
        model = AutoModel.from_pretrained('deepseek-ai/DeepSeek-R1')
        return tokenizer, model
    except Exception as e:
        st.error(f"모델 로딩 중 오류: {e}")
        return None, None
    
def get_embedding(text, tokenizer, model):
    """텍스트에서 임베딩을 추출합니다."""
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    # 마지막 히든 스테이트의 평균을 임베딩으로 사용
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings

def calculate_similarity(input_text, country_name, tokenizer, model):
    """입력 텍스트와 국가 이름 간의 의미적 유사성을 계산합니다."""
    input_emb = get_embedding(input_text, tokenizer, model)
    country_emb = get_embedding(country_name, tokenizer, model)
    
    # 코사인 유사도 계산
    similarity = cosine_similarity(input_emb.numpy(), country_emb.numpy())[0][0]
    return similarity

def start_new_game():
    """새 게임을 시작합니다."""
    countries = list(st.session_state.country_data.keys())
    st.session_state.current_country = random.choice(countries)
    st.session_state.attempts = 0
    st.session_state.guessed_countries = []
    st.session_state.hint_level = 0
    st.session_state.game_active = True

def check_guess(guess):
    """사용자의 추측을 확인합니다."""
    # 대소문자 구분 없이 정확히 일치하는지 확인
    if guess.lower() == st.session_state.current_country.lower():
        return True
    
    # 모델이 로드되었을 경우 의미적 유사성 확인
    if st.session_state.model_loaded:
        similarity = calculate_similarity(guess, st.session_state.current_country, 
                                         st.session_state.tokenizer, st.session_state.model)
        if similarity > 0.85:  # 임계값 설정 (필요에 따라 조정)
            return True
    
    return False

def get_hint():
    """현재 힌트 레벨에 해당하는 힌트를 반환합니다."""
    hint_key = f"힌트{st.session_state.hint_level + 1}"
    return st.session_state.country_data[st.session_state.current_country].get(hint_key, "더 이상 힌트가 없습니다.")

# 메인 앱 레이아웃
st.title("🌎 세계 나라 맞추기 게임")
st.write("힌트를 보고 어떤 나라인지 맞춰보세요!")

# 모델 로딩 상태 표시
with st.sidebar:
    st.header("게임 설정")
    model_loading = st.checkbox("DeepSeek-R1 모델 사용 (유사 답변 허용)", value=False)
    
    if model_loading and not st.session_state.model_loaded:
        with st.spinner("DeepSeek-R1 모델을 로딩 중입니다... (처음 로딩 시 시간이 걸릴 수 있습니다)"):
            st.session_state.tokenizer, st.session_state.model = load_model()
            if st.session_state.tokenizer is not None and st.session_state.model is not None:
                st.session_state.model_loaded = True
                st.success("모델 로딩 완료!")
            else:
                st.error("모델 로딩에 실패했습니다. 정확한 나라 이름만 인정됩니다.")
    
    st.markdown("---")
    st.write(f"현재 점수: {st.session_state.score}")
    
    if st.button("새 게임 시작"):
        start_new_game()

# 게임 화면
if st.session_state.game_active:
    # 힌트 표시
    hint_container = st.container()
    with hint_container:
        st.subheader("🔍 힌트")
        for i in range(1, st.session_state.hint_level + 1):
            hint_key = f"힌트{i}"
            st.info(st.session_state.country_data[st.session_state.current_country][hint_key])
    
    # 사용자 입력
    user_guess = st.text_input("나라 이름을 입력하세요:", key="guess_input")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("확인"):
            if user_guess:
                st.session_state.attempts += 1
                st.session_state.guessed_countries.append(user_guess)
                
                if check_guess(user_guess):
                    st.success(f"🎉 정답입니다! '{st.session_state.current_country}'를 맞추셨습니다!")
                    st.session_state.score += max(1, st.session_state.max_attempts - st.session_state.attempts + 1)
                    st.write(st.session_state.country_data[st.session_state.current_country]["설명"])
                    st.session_state.game_active = False
                else:
                    if st.session_state.attempts >= st.session_state.max_attempts:
                        st.error(f"게임 오버! 정답은 '{st.session_state.current_country}'입니다.")
                        st.write(st.session_state.country_data[st.session_state.current_country]["설명"])
                        st.session_state.game_active = False
                    else:
                        st.warning(f"틀렸습니다! 남은 기회: {st.session_state.max_attempts - st.session_state.attempts}")
    
    with col2:
        if st.button("힌트 보기") and st.session_state.hint_level < 4:
            st.session_state.hint_level += 1
            st.experimental_rerun()
    
    # 이전 추측 기록
    if st.session_state.guessed_countries:
        st.subheader("이전 추측:")
        for idx, country in enumerate(st.session_state.guessed_countries):
            st.write(f"{idx+1}. {country}")
else:
    st.info("새 게임을 시작하려면 사이드바의 '새 게임 시작' 버튼을 클릭하세요.")
    if st.session_state.current_country:
        st.success(f"마지막 게임의 정답은 '{st.session_state.current_country}'였습니다.")

# 게임 규칙 설명
with st.expander("게임 규칙"):
    st.write("""
    1. 시스템이 무작위로 선택한 나라를 맞추는 게임입니다.
    2. 총 5번의 기회가 있으며, 각 시도마다 힌트를 볼 수 있습니다.
    3. 정확한 나라 이름을 입력해야 합니다.
    4. DeepSeek-R1 모델을 활성화하면 유사한 답변도 인정됩니다.
    5. 빨리 맞출수록 더 많은 점수를 얻습니다.
    """)
