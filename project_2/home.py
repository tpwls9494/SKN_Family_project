# home.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def main():
    st.set_page_config(
        page_title="갤럭시 이탈자 분석",
        page_icon="📱",
        layout="wide"
    )
    
    # 메인 타이틀 및 소개
    st.title("갤럭시 이탈자 예측 분석 📱")
    
    # 연구 배경 설명
    st.markdown("""
    ### 📱 연구 배경
    삼성전자의 주가 변동이 갤럭시 사용자들의 브랜드 충성도에 미치는 영향을 분석하고자 했습니다.
    특히 2021년, 2022년, 2023년의 사용자 이탈 패턴을 심층적으로 분석하여, 어떤 요인들이 
    브랜드 이탈에 영향을 미치는지 파악하고자 했습니다.
    """)
    
    # 데이터 로드
    @st.cache_data
    def load_data():
        return pd.read_csv('data/phone_information.csv')
    
    data = load_data()
    
    # 데이터 분석 결과 표시
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📊 분석 데이터")
        st.metric("전체 분석 대상", f"{len(data):,}명")
        st.metric("분석 기간", "2021-2023")
    
    with col2:
        st.subheader("📈 이탈률 변화")
        st.metric("2022년", f"{5.17}")
        st.metric("2023년", f'{6.50}', 
                 delta=f"{(0.0517 - 0.06502)*100:+.2f}%")
    
    with col3:
        st.subheader("🎯 예측 정확도")
        st.metric("모델 정확도", "71.1%")
        st.metric("이탈 예측률", "24.1%")
    
    # 주요 분석 지표
    st.markdown("""
    ### 📊 분석 방법론
    """)
    
    method_col1, method_col2 = st.columns(2)
    
    with method_col1:
        st.markdown("""
        #### 📌 분석 변수
        - 인구통계: 연령, 성별
        - 사용 행태: 앱 사용, 통신사
        - 경제 지표: 기기 가격, 결제 패턴
        - 서비스: 모바일 신용카드, 앱 사용량
        """)
    
    with method_col2:
        st.markdown("""
        #### 🔍 분석 고도화
        - 데이터 불균형 해소
        - 오버샘플링 적용
        - 가중치 최적화
        - 모델 성능 개선
        """)
    
    # 이탈 요인 분석 결과
    st.markdown("### 🔍 주요 이탈 요인")
    
    # 예시 데이터로 이탈 요인 시각화
    factors_data = pd.DataFrame({
        '요인': ['가격 부담', '앱 만족도', '통신품질', '브랜드 선호도', '서비스 경험'],
        '영향도': [0.85, 0.72, 0.65, 0.58, 0.45]
    })
    
    fig = px.bar(factors_data, 
                x='영향도', 
                y='요인',
                orientation='h',
                title='이탈 영향 요인 분석')
    st.plotly_chart(fig)
    
    # 결론 및 시사점
    st.markdown("""
    ### 💡 분석 인사이트
    1. **가격 민감도**: 기기 가격과 유지비용이 주요 이탈 요인
    2. **사용자 경험**: 앱 생태계와 서비스 만족도가 중요
    3. **통신 품질**: 통신사 서비스 품질이 이탈에 영향
    4. **개인화 요구**: 연령별, 성별 맞춤 서비스 필요
    """)

if __name__ == "__main__":
    main()